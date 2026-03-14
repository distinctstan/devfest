from flask import render_template,abort,session,request,url_for,flash,redirect
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app, devforms
from pkg.devmodels import Admin

@app.after_request
def after_request(response):
    response.headers["Cache-Control"]="no-cache, no-store,must-revalidate"
    return response 


@app.route("/admin/",methods=['POST','GET'])
def admin_home():
    if session.get('adminonline') and session.get('adminid'):
        return redirect(url_for('admin_dashboard'))
    else:
        flash("You must be logged in as an admin",category='danger')
        return redirect(url_for('admin_login'))

@app.route("/admin/dashboard/")
def admin_dashboard():
    if session.get('adminonline') and session.get('adminid'):
         return render_template("admin/dashboard.html")
    else:
        flash("You must be logged in as an admin",category='danger')
        return redirect(url_for('admin_login'))

@app.route("/admin/login/", methods=['POST','GET'])
def admin_login():
    logform = devforms.LoginForm()
    if request.method =='GET':
        return render_template('admin/login.html',logform=logform)
    else:
        if logform.validate_on_submit():
                email = logform.email.data
                password = logform.password.data
                admin = Admin.query.filter(Admin.adm_email==email).first()
                if admin:#email is correct
                     stored_pass= admin.adm_password_hash
                     chk = check_password_hash(stored_pass,password)
                     if chk:
                          session['adminonline'] = admin.adm_full_name
                          session['adminid']= admin.adm_id
                          return redirect(url_for('admin_dashboard'))
                else:
                     flash("Invalid Email", category="danger")
                     return redirect(url_for('admin_login'))
        else:
             return render_template("admin/login.html", logform=logform)

@app.route("/admin/logout/")
def admin_logout():
    if session.get("adminonline") and session.get("adminid"):
        session.pop("adminonline",None)
        session.pop('adminid',None)
        session.clear()
    return redirect(url_for('admin_login'))