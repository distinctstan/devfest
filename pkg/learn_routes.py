import secrets,os
from flask import render_template,abort, request, redirect,flash, url_for,session
from pkg import app, devforms
from pkg.devmodels import db

@app.route("/learn/flaskform/", methods=['POST','GET'])
def upload_flask_form():
    '''File upload using flask form'''
    photoform = devforms.PhotoForm()
    if request.method =="GET":
        return render_template("learn/flask_upload_form.html",photoform=photoform)
    else:
        if photoform.validate_on_submit():
            fileobj = photoform.photo.data
            dfilename =fileobj.filename
            name,extension = os.path.splitext(dfilename)
            newname = secrets.token_hex(10)+ extension  
            fileobj.save("pkg/static/uploads/"+ newname)
            #save newname to db
            flash("Photo saved", category="success")
            return redirect("/learn/show_photos/")
        else:
            return render_template("learn/flask_upload_form.html", photoform=photoform)
    


@app.route("/learn/form/", methods=['POST','GET'])
def upload_form():
    '''File upload without flask form'''
    if request.method =='GET':
        return render_template("learn/upload_form.html")
    else:
        caption = request.form.get('caption')
        photo_obj = request.files.get('photo') #instance of FileStorage
        dfilename = photo_obj.filename
        name,extension = os.path.splitext(dfilename)
        #validation
        if caption =="" or dfilename =="":
            flash("The filename and caption can not be empty",category="danger")
            return redirect("upload_form")
        else:
            #generate a random name
            allowed = [".jpg",".png",".jpeg",".gif"]
            if extension.lower() in allowed:
                newname = secrets.token_hex(10)+ extension    
                photo_obj.save("pkg/static/uploads/"+ newname)
                #insert into database - save newname
                flash("Photo saved", category="success")
                return redirect("/learn/show_photos/")
            else:
                flash("Extension not allowed",category="danger")
                return redirect(url_for("upload_form"))

@app.route('/learn/show_photos/', methods=['POST','GET'])
def show_photo():
    return "We will display pictures here"