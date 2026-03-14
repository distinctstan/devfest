import secrets,os, requests,json
from flask import render_template,abort, request, redirect,flash, url_for,session
from werkzeug.security import generate_password_hash, check_password_hash

from pkg import app, devforms
from pkg.devmodels import db, User,Conversation,Track, Session as FestivalSession,Ticket,Order,Payment

@app.errorhandler(404)
def NotFound(error):
    return render_template("user/404.html",error=error),404

@app.after_request
def after_request(response):
    response.headers["Cache-Control"]="no-cache, no-store,must-revalidate"
    return response 

@app.route("/")
def index():
    try:
        header= {"Content-Type":"application/json"}
        username=app.config['API_USERNAME']
        password =app.config["API_PASSWORD"]
        response = requests.get("http://127.0.0.1:8087/api/v1/listall", auth=(username,password), verify=False,headers=header)
        properties = response.json()#json.loads(response.text)
    except:
        properties = None

    return render_template("user/home.html",properties=properties)

@app.route("/register/", methods=['POST','GET'])
def user_register():
    regform = devforms.RegistrationForm()
    if request.method =="GET":
        return render_template('user/register.html', regform=regform) 
    else:
        if regform.validate_on_submit():
            #retrieve form data
            firstname= request.form.get("firstname")
            lastname = request.form.get("lastname")#regform.lastname.data
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = generate_password_hash(password)
            #save into db
            user = User(usr_firstname=firstname,usr_lastname=lastname,usr_email=email,usr_password_hash=hashed_password)
            if User.is_email_used(email):
                flash("You have registered before, Please login.",category='danger')
            else:                
                db.session.add(user)
                db.session.commit()
                flash("Registration successful",category='success')
            return redirect(url_for("user_login"))            
        else:
            return render_template("user/register.html", regform=regform)

@app.route("/login/",methods=['POST',"GET"])
def user_login():
    form = devforms.LoginForm()
    if request.method =='GET':
        return render_template("user/login.html",form=form)
    else:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            userdeets = User.query.filter(User.usr_email==email).first()
            if userdeets:#the email exists, check if password is correct
                stored_password = userdeets.usr_password_hash
                check = check_password_hash(stored_password,password)
                if check ==True:#password is correct
                    session['useronline'] = userdeets.usr_firstname
                    session['userid'] = userdeets.usr_id
                    return redirect(url_for('dashboard'))
                else:
                    flash("Invalid credentials",category="danger")
                    return redirect(url_for('user_login'))
            else:#the email is invalid
                flash("Invalid credentials", category="danger")
                return redirect(url_for('user_login'))
        else:
            return render_template("user/login.html", form=form)
        
@app.route("/dashboard/")
def dashboard():
    if session.get("useronline") and session.get("userid"):
        return render_template("user/dashboard.html")
    else:
        flash("Please login here to continue", category="danger")
        return redirect(url_for("user_login"))

@app.get("/logout/")
def logout():
    if session.get("useronline") and session.get("userid"):
        session.pop("useronline",None)
        session.pop('userid',None)
        session.clear()
    return redirect(url_for('user_login'))

@app.route("/conversations/")
def conversations():
    convo = Conversation.query.all()#db.session.query(Conversation).all()
    return render_template("user/conversations.html",convo=convo)
    
    
@app.route('/create/topic/',methods=["POST","GET"])
def create_topic():
    convform = devforms.ConversationForm()
    if session.get("useronline") and session.get("userid"):
        if request.method=="GET":
            return render_template("user/create-topic.html",convform=convform)
        else:
            if convform.validate_on_submit():
                title = convform.title.data
                content = convform.content.data
                
                converse = Conversation(con_title=title,con_content =content,con_created_by=session['userid'])

                converse.save()#our helper method created within Conersation class in our model
                flash(f"Conversation - {title} posted ",category="success")
                return redirect(url_for('conversations'))
            else:
                return render_template("user/create-topic.html",convform=convform)
    else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login'))

@app.route("/profile/", methods=["POST","GET"])
def profile():
    prof = devforms.ProfileForm() 
    photoform = devforms.PhotoForm()
    tracks = db.session.query(Track).all()
    if session.get('useronline') and session.get("userid"):
        #fetch the user's details from session + db
        userdeets= User.query.get(session['userid'])
            
        if request.method=='GET':
            prof.summary.data = userdeets.usr_summary   
            return render_template("user/profile.html",prof=prof,userdeets=userdeets,tracks=tracks,photoform=photoform)        
        else:#form submission will come here
            if prof.validate_on_submit():
                #update the db (User Model)
                userdeets.usr_firstname = prof.firstname.data
                userdeets.usr_lastname =  prof.lastname.data
                userdeets.usr_track_id  = request.form.get('category')
                userdeets.usr_summary = request.form.get("summary")
                db.session.commit()
                session['useronline'] = prof.firstname.data
                flash("Profile successfully updated",category='success')
                return redirect(url_for('profile'))
            else:
                prof.summary.data = userdeets.usr_summary  
                return render_template("user/profile.html",prof=prof,userdeets=userdeets,tracks=tracks,photoform=photoform)
    else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login'))
    


@app.route("/profile/picture/",methods=["POST","GET"])
def profile_picture():
    photoform = devforms.PhotoForm()
    if session.get('userid') and session.get('useronline'):
        if request.method =="POST" and photoform.validate_on_submit():
            #retrieve formdata and upload
            photo_obj = photoform.photo.data
            dfilename =photo_obj.filename
            name,extension = os.path.splitext(dfilename)
            newname = secrets.token_hex(10)+ extension  
            photo_obj.save("pkg/static/uploads/"+ newname)
            #save in db 
            user = User.query.get(session['userid'])
            user.usr_image = newname
            db.session.commit()
            flash("Photo uploaded", category="success")
            return redirect(url_for('profile'))
        else:
            flash("Filetype not allowed",category="danger")
            return redirect(url_for('profile'))
    else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login')) 
    

@app.route("/mysessions/", methods=["GET","POST"])
def user_sessions():
    if session.get("useronline") and session.get("userid"):
        gentracks = Track.query.filter(Track.trk_level=="general").first()
        userdeets = User.query.get(session['userid'])
        loggedin_user_trackid = userdeets.usr_track_id 

        mytracks = Track.query.filter(Track.trk_id==loggedin_user_trackid, Track.trk_level != "general").first()

        if request.method =="GET":
            return render_template("user/sessions.html",gentracks=gentracks,mytracks=mytracks,userdeets=userdeets)
        else:
            return "Form submitted here"
    else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login')) 
    

@app.route("/view/tickets/", methods=['POST',"GET"])
def view_tickets():
    if session.get('useronline') and session.get('userid'):
        tickets = db.session.query(Ticket).all()
        if request.method=="GET":
            return render_template("user/view_tickets.html",tickets=tickets)
        else:
            ticketid = request.form.get('ticketType')
            ticket_deets = db.session.query(Ticket).get(ticketid)
            if ticketid and ticket_deets:
                ref = secrets.token_hex(10)
                new_order = Order(
                    ord_user_id=session['userid'],
                    ord_ticket_id=ticketid,
                    ord_order_ref=ref,
                    ord_total_amount=ticket_deets.tkt_price,
                    ord_status="pending"
                    )
                db.session.add(new_order)
                db.session.commit()
                session['payref'] = ref
                return redirect(url_for('order_confirmation'))
            else:
                flash("You must choose a ticket type", category='danger')
                return redirect(url_for('view_tickets'))
    else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login')) 

@app.route("/order/confirm/")
def order_confirmation():
     if session.get('useronline') and session.get('userid'):
        ref= session.get('payref')
        if ref:#means order has been created
            ords = db.session.query(Order).filter(Order.ord_order_ref==ref).first()
            return render_template("user/order_confirm.html",ords=ords)
        else:
            flash("You need to select a ticket", category='danger')
     else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login')) 


@app.route("/conversation/<id>/")
def conversation_detail(id):
    deets = Conversation.query.get(id)
    return render_template("user/conversation-detail.html",deets=deets)#within the template, display: deets.con_title etc

@app.route("/start/paystack/")
def start_paystack():
    #insert the details into payment table, then
    #connect to paystack by POST
    if session.get('useronline') and session.get('userid'):
        ref= session.get('payref')
        if ref:#means order has been created
            ords = db.session.query(Order).filter(Order.ord_order_ref==ref).first()
            pay = Payment(
                pay_order_id=ords.ord_id,
                pay_payment_ref=ref,
                pay_amount=ords.ord_total_amount,
                pay_status='pending')
            db.session.add(pay)
            db.session.commit()
            #connect to paystack
            url = "https://api.paystack.co/transaction/initialize"
            headers={"Cotent-Type":"application/json","Authorization":"Bearer sk_test_65ee8fc86def546325848bef406cc22823441934"}
            amount = int(ords.ord_total_amount)*100
            data = {'amount':amount,'email':ords.user.usr_email,'reference':ref,'callback_url':"http://127.0.0.1:8081/paystack/"}
            response = requests.post(url,headers=headers,data=json.dumps(data))
            rsp = response.json()
            if rsp and rsp['status'] ==True:
                auth_url = rsp['data']['authorization_url']
                return redirect(auth_url)
            else:
                flash('API Error'+rsp['message'],category='danger')
                return redirect(url_for('view_tickets'))
        else:
            flash("You need to select a ticket", category='danger')
    else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login')) 

@app.route("/paystack/")
def paystack_verify():
    if session.get('useronline') and session.get('userid'):
        ref= session.get('payref')
        url ="https://api.paystack.co/transaction/verify/"+ref
        headers={"Cotent-Type":"application/json","Authorization":"Bearer sk_test_65ee8fc86def546325848bef406cc22823441934"}
        response = requests.get(url,headers=headers)
        rsp = response.json()
        if rsp and rsp['status']==True:
            savedb = rsp['data']
            status = 'successful'
            ordstatus='paid'
        else:
            savedb = rsp['data']
            status='failed'
        pay = db.session.query(Payment).filter(Payment.pay_payment_ref==ref).first()
        
        pay.pay_status=status
        pay.pay_data= savedb

        order = db.session.query(Order).filter(Order.ord_order_ref==ref).first()
        order.ord_status=ordstatus

        db.session.commit()
        #update your db and redirect user to dashboard
        flash("Transaction completed with status: "+status)
        return redirect(url_for('dashboard'))
    else:
        flash("Please login to continue",category="danger")
        return redirect(url_for('user_login')) 