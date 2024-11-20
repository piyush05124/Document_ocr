from configparser import ConfigParser
config_object = ConfigParser()
config_object.read("./processing_modules/config.ini")
config = config_object['STATIC_IMAGE_PATHS']
home_page  = config["homepage_background_image"]
other_page = config["otherpage_background_image"]
image_html = config["image_html_placeholder_icon"]



from flask import Flask, render_template, redirect, url_for, session, flash,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from processing_modules.databse import dbconn, db_insert,db_fetch,db_fetch_content
from processing_modules.encrypt_decrypt_data import encrypt,decrypt
from processing_modules.pdfextract import pdftext
from processing_modules.adharcard_long import adhar, QRcode
from processing_modules.image_to_text import simple_image_extract
from processing_modules.QRreader import Decode

import cv2,os,sys,json
import pandas as pd

app = Flask(__name__)

app.secret_key = 'only one'

class RegisterForm(FlaskForm):
    name = StringField("Name")
    password = PasswordField("Password")
    submit = SubmitField("Register")
    def validate_email(self,field):
        cursor = dbconn()
        cursor.execute("SELECT * FROM login_credetials where client_id = %s",(field.data))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")
    

def create_dataframe(d):
    try:
        df = pd.DataFrame(d)
    except:
        max_length = max(len(d[key]) for key in d)
        normalized_data = {key: d[key] + [None] * (max_length - len(d[key])) for key in d}
        df = pd.DataFrame(normalized_data)
    return df



@app.route('/')
def index():
    return redirect(url_for('home'))


#====================================================================================================================
@app.route('/home' ,methods=['GET','POST']) # page 2
def home():
        return render_template('homepage.html',img_path = home_page)
#==================================================================================================================
#====================================================================================================================
@app.route('/home_user' ,methods=['GET','POST']) # page 2
def home_user():
        login_name = list(session.keys())
        if (len(login_name)>0) and ('user_id' in login_name):
            login_name = session['user_id']
        else:
            login_name = 'Login'
        # if request.method == 'POST':

        
        # if session['user_id'] != None:
        #     return redirect(url_for('dashboard'))
        return render_template('homepage_user.html',img_path = home_page,login_name = login_name)
#==================================================================================================================



@app.route('/login_dashboard',methods = ["POST"])
def login_dashboard():
    return redirect(url_for('dashboard'))
#==========================================================================================================================
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        hashed_password = encrypt(password) 
        x = "INSERT INTO login_credetials (client_id ,s_password) VALUES (%s,%s)"%(repr(name),repr(hashed_password))
        try:
            db_insert(x)
            flash("Account Created successfully !")
        except:
            flash("Account  Exist. \n Please register !")
      
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

#====================================================================================================================
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        querry = "SELECT client_id ,s_password FROM login_credetials WHERE client_id =%s"%(repr(email))
        db_ouptput = db_fetch(querry)
        if db_ouptput != None :
            user , s_password = db_ouptput
            if decrypt(s_password)    == password:
                session['user_id']    = user
                session['s_password'] = s_password
                return redirect(url_for('home_user'))
            else:
                flash("Login failed. Please check your email and password")
                return redirect(url_for('login'))
        else:
            flash("Account does not Exist. \n Please register !")
        if session['user_id'] != None:
            return redirect(url_for('dashboard'))
    return render_template('login.html',form=form)

#=================================================================================================================
@app.route('/getimagefiles',methods = ['POST'])#                                                      
def getimagefiles():#  
    print('inside getimg_files')
         
    impath  = 'static/image_icon.png'                                                                  
    return render_template('imgtext.html',img_path = other_page, impath= impath)#<---|      
#     


@app.route('/upload_image',methods=['POST'])
def upload_image():
    
    if request.method=='POST':
       f = request.files['img']
       
    if not f:
        return "<p align='center'><h1>please upload a file</h1></p>"
    fname=f.filename
    ch=request.form['Document type']
    if ch=='non document':
       f.save(os.path.join('static','plainimg',fname))
       fpath=os.path.join('static','plainimg',fname)
       text=simple_image_extract(fpath)
       return render_template('imgtext.html',img_path = other_page,impath=fpath,extext=text)
    elif ch=='Adhar card':
        f.save(os.path.join('static','adhar',fname))
        fpath=os.path.join('static','adhar',fname)
        text=QRcode(fpath)
        return render_template('imgtext.html',img_path = other_page,impath=fpath,extext=text)
    else:
        return render_template('imgtext.html',img_path = other_page)









@app.route('/qrcode')#                                                      
def qrcode():#                                                                        
    return render_template('qcode.html',img_path = other_page)            
                   
@app.route('/qr',methods=['POST'])           
def QR():#                                                                                
    if request.method=='POST':#                                           
        return redirect(url_for('qrcode'))
    

@app.route('/PDF',methods=['POST'])
def PDF():
    if request.method=='POST':
        return render_template('pdftext.html',img_path = other_page)
    


@app.route('/pdf',methods=['POST'])
def pdf():
    if request.method=='POST':
        pf = request.files['pdf']
        if not pf:
            return "<h1>please upload PDF file</h1>"
        fname=pf.filename
        pf.save(os.path.join('static','pdfiles',fname))
        pfpath=os.path.join('static','pdfiles',fname)
        pn=request.form['pgno']
        if not pn:
            render_template('pdftext.html',img_path= other_page,ptext=text)
            return ("""<!DOCTYPE html>
                        <html>
                            <script >
                            alert("please upload pgno")	
                            </script>
                        <body>
                        </body>
                        </html>     
                        """)    
        text = pdftext(pfpath,int(pn))
        
        return render_template('pdftext.html',img_path= other_page,ptext=text)



@app.route('/down', methods=['POST'])  
def down(): 
    print(request )  
    if request.method=='POST' :
        f=request.files['img']
        fname=f.filename
        print(fname)
        if not fname:
            return """<html>
                            <script >
                            alert("please upload pgno")	
                            </script>
                        <body>
                        </body>

                        </html>     """
        f.save(os.path.join('static','QRCODE',fname))
        fpath=os.path.join('static','QRCODE',fname)
        imh=cv2.imread(fpath)
        h,w,_=imh.shape
        imh=cv2.resize(imh,(h-30,w-30))
        cv2.imwrite(fpath,imh)
        qtext=Decode(fpath)
        
        return render_template('qcode.html',img_path=other_page ,qtext=qtext)
##            

#============================================================================================
@app.route('/dashboard')
def dashboard():
    from processing_modules.query import saved_data_fetch
    if 'user_id' in session:
        user_id = session['user_id']
        query = "SELECT * FROM login_credetials where client_id='%s';"%(user_id)
        user,s_pass  = db_fetch(query)
        if user:
            content = db_fetch_content(saved_data_fetch %(user_id))
            print(content)
            if len(content)>0:

                try:
                    content = json.loads(content[0][-1])
                except:
                    content = content[0][-1]
                df = create_dataframe(content)
                return render_template('dashboard.html',iconpath = '/static/hacker.png',img_path = home_page,user=user,content = df)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=3000,debug=True)