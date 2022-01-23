from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import re
import pickle
from flask_mysqldb import MySQL
import MySQLdb.cursors
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os 
from datetime import date
from werkzeug.utils import secure_filename
import pandas as pd
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import load_model


model1 = load_model('model1.h5')
model2 = load_model('model2.h5')

import re
from googlesearch import search
import warnings
warnings.filterwarnings("ignore")
import requests
from bs4 import BeautifulSoup





UPLOAD_FOLDER = 'C:/Users/Isha Patel/OneDrive/Desktop/PROJECTS/Evathon/evathon/static/img/uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER     

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bloom'

mysql = MySQL(app)
app.secret_key = 'key12'

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/UserRegister", methods=['GET', 'POST'])
def UserRegister():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'FullName' in request.form and 'Password' in request.form and 'Weight' in request.form and 'Gender' in request.form and 'Height' in request.form and 'Address' in request.form and 'Contact' in request.form :
        # Create variables for easy access
        Username = request.form['Username']
        FullName = request.form['FullName']
        Password = request.form['Password']
        Weight = request.form['Weight']
        Gender = request.form['Gender']
        Height = request.form['Height']
        Address = request.form['Address']
        Contact = request.form['Contact']
        Allergies = request.form['Allergies']
        MedConditions = request.form['MedConditions']
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE Username = %s AND Password=%s', [Username, Password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            
    
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'Username must contain only characters and numbers!'
            
        elif not Username or not Password:
            msg = 'Please fill out the form!'
            
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', [Username,FullName, Password,Weight, Gender, Height,Address,Contact,Allergies,MedConditions])
            mysql.connection.commit()
            msg = 'Successfully registered! Please Log-In'
            
            return redirect(url_for('login'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template("UserRegister.html", msg=msg)

@app.route("/DoctorRegister", methods=['GET', 'POST'])
def DoctorRegister():
    msg=''
    if request.method == 'POST' and 'Username' in request.form and 'FullName' in request.form and 'Password' in request.form and 'Specialization' in request.form and 'Gender' in request.form and 'WExp' in request.form and 'Contact' in request.form :
        # Create variables for easy access
        Username = request.form['Username']
        Password = request.form['Password']
        FullName = request.form['FullName']
        Specialization = request.form['Specialization']
        Gender = request.form['Gender']
        WExp = request.form['WExp']        
        Hospital = request.form['Hospital']
        HospAdd = request.form['HospAdd']
        HospContact = request.form['HospContact']
        Contact = request.form['Contact']
        Day = request.form['Day']
        Whrs = request.form['Whrs']
        
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM doc_details WHERE Username = %s AND Password=%s', [Username, Password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'      
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'Username must contain only characters and numbers!'            
        elif not Username or not Password:
            msg = 'Please fill out the form!'            
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM hospitals WHERE hosp_name=%s', [Hospital])
            hospt = cursor.fetchone()
            
            if hospt:
                cursor.execute('SELECT hosp_id FROM hospitals WHERE hosp_name=%s', [Hospital])
                hospt_id = cursor.fetchone()
                print(hospt_id)
                cursor.execute('INSERT INTO doctors (hosp_id,Doctor) VALUES(%s,%s)', (hospt_id['hosp_id'], FullName))
                mysql.connection.commit()
            else:
                cursor.execute('INSERT INTO hospitals (hosp_name) VALUES(%s)', [Hospital])
                mysql.connection.commit()
                cursor.execute('SELECT hosp_id FROM hospitals WHERE hosp_name=%s', [Hospital])
                hospt_id = cursor.fetchone()
                cursor.execute('INSERT INTO doctors (hosp_id,Doctor) VALUES(%s,%s)', (hospt_id['hosp_id'], FullName))
                mysql.connection.commit()

            cursor.execute('INSERT INTO doc_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (Username, FullName,Password,Specialization,Gender,WExp,Contact,Hospital,HospAdd,HospContact,Day,Whrs))
            mysql.connection.commit()
            msg = 'Successfully registered! Please Log-In'

            
            
            return redirect(url_for('login'))
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template("DoctorRegister.html", msg=msg)

@app.route("/login", methods=['GET', 'POST'])
def login():
    msg=''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        print('111111111')
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE Username=%s AND Password=%s',[Username, Password])
        user = cursor.fetchone()
        cursor.execute('SELECT * FROM doc_details WHERE Username=%s AND Password=%s', [Username, Password])
        # Fetch one record and return result
        doc = cursor.fetchone()
        print(doc, user)
            # print("gg")
        # Create variables for easy access
        
       
        # If account exists in accounts table in out database
        if user==None and doc==None:
            msg = 'Incorrect Username or Password'
            # return redirect(url_for('login',msg=msg))   
        elif user!=None and doc==None:
            session['loggedin'] = True
            session['Username'] = user['Username']
            return redirect(url_for('UserHome'))
        elif doc!=None and user==None:
            session['loggedin'] = True
            session['Username'] = doc['Username']
            session['FullName'] = doc['FullName']
            return redirect(url_for('DocHome'))

    
    return render_template('login.html', msg=msg)   


@app.route("/UserHome", methods=['GET', 'POST'])
def UserHome():
    return render_template("UserHome.html")

@app.route("/UserProfile", methods=['GET', 'POST'])
def UserProfile():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user_details WHERE Username=%s ',[session['Username']])
    user = cursor.fetchone()
    return render_template("UserProfile.html",user=user)

@app.route("/UpdateUserProfile", methods=['GET', 'POST'])
def UpdateUserProfile():
    if request.method == 'POST':
        Weight = request.form['Weight']
        Height = request.form['Height']
        Address = request.form['Address']
        Contact = request.form['Contact']
        Allergies = request.form['Allergies']
        MedConditions = request.form['MedConditions']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        if Weight:
            cursor.execute('UPDATE user_details SET Weight = %s WHERE Username=%s', (Weight,session['Username']))
            mysql.connection.commit()
        if Height:
            cursor.execute('UPDATE user_details SET Height = %s WHERE Username=%s', (Height,session['Username']))
            mysql.connection.commit()
        if Address:
            cursor.execute('UPDATE user_details SET Address = %s WHERE Username=%s', (Address,session['Username']))
            mysql.connection.commit()
        if Contact:
            cursor.execute('UPDATE user_details SET Contact = %s WHERE Username=%s', (Contact,session['Username']))
            mysql.connection.commit()
        if Allergies:
            cursor.execute('UPDATE user_details SET Allergies = %s WHERE Username=%s', (Allergies,session['Username']))
            mysql.connection.commit()
        if MedConditions:
            cursor.execute('UPDATE user_details SET MedConditions = %s WHERE Username=%s', (MedConditions,session['Username']))
            mysql.connection.commit()

    return render_template("UpdateUserProfile.html")

@app.route("/Diagnosis", methods=['GET', 'POST'])
def Diagnosis():
    name = ''
    obj_name=''
    link=''
    text=''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            msg= 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            msg= 'No selected file'
        if file and allowed_file(file.filename):

            if request.form['Submit']:
                name=session['Username']
            filename = secure_filename(file.filename)
            sess = session['Username']
            path1 = UPLOAD_FOLDER + '/' + name + sess
            if os.path.isdir(path1):
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                os.mkdir(path1)
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                dir_list= []
            dir_list = os.listdir(path1)
            print(dir_list)
            print(path1+'11111111111')

            image_name = dir_list[-1]
            dir_list = []
            image1 = load_img(path1+'/'+image_name, target_size=(224, 224))
            image1 = img_to_array(image1)
            # reshape data for the model
            print(image1.shape)
            image1 = image1.reshape((1, image1.shape[0], image1.shape[1], image1.shape[2]))
            print(image1.shape)

            # prepare the image for the VGG model
            image1 = preprocess_input(image1)

            yhat = model1.predict(image1, verbose=0)[0]
            print(yhat)
            print(yhat.max())
            imp = ''
            
            if yhat[0] == yhat.max():
                obj_name = 'You are likely to have acne scars'
                link= 'https://www.aad.org/public/diseases/acne/diy/back-acne'
            elif yhat[1] == yhat.max():
                obj_name = 'You are likely to be suffering from alopecia areata'
                link= 'https://www.aad.org/public/diseases/hair-loss/types/alopecia/self-care'
            elif yhat[2] == yhat.max():
                obj_name = 'You are likely to be suffering from melasma'
                link= 'https://styledwanderlust.com/'
            elif yhat[3] == yhat.max():
                obj_name = 'You are likely to be suffering from vitiligo'
                link= 'https://www.aad.org/public/diseases/a-z/vitiligo-self-care'
            elif yhat[4] == yhat.max():
                obj_name = 'You are likely to be suffering from warts'
                link= 'https://www.aad.org/public/diseases/a-z/warts-self-care'
            elif yhat[5] == yhat.max():
                obj_name = 'You are likely to be suffering from acanthosis nigricans'
                link= 'https://www.aad.org/public/diseases/a-z/acanthosis-nigricans-self-care'
            elif yhat[6] == yhat.max():
                obj_name = 'You are likely to have acne'      
                link= 'https://www.aad.org/public/diseases/acne/skin-care/tips'             
            print(obj_name)
            text='Here is a skin care routine for you!'
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    
    
    return render_template("Diagnosis.html", obj_name=obj_name, link=link, text=text)


@app.route('/BookAppointment', methods=['POST', 'GET'])
def BookAppointment():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM hospitals ORDER BY hosp_id")
    carbrands = cur.fetchall()
    print(carbrands)
    if request.method == 'POST' and 'Mode' in request.form and 'Doctor' in request.form and 'Date' in request.form and 'Time' in request.form and 'Hospital' in request.form:        
        
        Mode = request.form['Mode']
        Doctor = request.form['Doctor']
        Date = request.form['Date']
        Time = request.form['Time']
        Patient = session['Username']
        Hospital = request.form['Hospital']
        print(Doctor)
        hosp_name=''
        dc_name=''
        if Mode=='Online':
            
            PATH = "C:\Program Files (x86)\chromedriver.exe"
            driver = webdriver.Chrome(PATH)
            driver.get("https://talky.io/")
            button = driver.find_element_by_class_name("create-room-form-button")
            button.click()
            link=driver.current_url
            driver.quit()
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('SELECT Doctor FROM doctors WHERE dc_id=%s', [Doctor])
            var = cursor.fetchone()
            cursor.execute('SELECT hosp_name FROM hospitals WHERE hosp_id=%s', [Hospital])
            hvar = cursor.fetchone()

            cursor.execute('INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[Patient, Mode, Doctor, Hospital, hvar['hosp_name'], var['Doctor'], Date, Time,link])
            mysql.connection.commit()
            
            
            
        else:
            link=''
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT Doctor FROM doctors WHERE dc_id=%s', [Doctor])
            var = cursor.fetchone()
            cursor.execute('SELECT hosp_name FROM hospitals WHERE hosp_id=%s', [Hospital])
            hvar = cursor.fetchone()
            # print(var, hvar)
            cursor.execute('INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[Patient, Mode, Doctor, Hospital, hvar['hosp_name'], var['Doctor'], Date, Time,link])
            mysql.connection.commit()     
                   
    return render_template('BookAppointment.html', carbrands=carbrands)
 
@app.route("/carbrand",methods=["POST","GET"])
def carbrand():  
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        category_id = request.form['category_id'] 
        
        result = cur.execute("SELECT * FROM doctors WHERE hosp_id = %s ORDER BY Doctor ASC", [category_id] )
        carmodel = cur.fetchall()  
        OutputArray = []
        for row in carmodel:
            outputObj = {
                'id': row['hosp_id'],
                'name': row['Doctor'],
                'dc_id':row['dc_id']}
            OutputArray.append(outputObj)
    
    return jsonify(OutputArray)

@app.route("/BookedAppointments", methods=['GET', 'POST'])
def BookedAppointments():
    # print(session['Username'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE Patient=%s', [session['Username']])
    user = cursor.fetchall()
    print(user)  
    
    return render_template("BookedAppointments.html", user=user)

@app.route("/Prescriptions", methods=['GET', 'POST'])
def Prescriptions():  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE Patient=%s AND Mode="Online"', [session['Username']])
    user = cursor.fetchall() 
    path1 = UPLOAD_FOLDER + '/' + session['Username']
    var = os.listdir(path1)
    print(var)
    name=session['Username']
    return render_template('Prescriptions.html', users=zip(user,var), name=name)

@app.route("/NearbyClinics", methods=['GET', 'POST'])
def NearbyHospitals():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM doc_details ')
    details = cursor.fetchall()
    return render_template("NearbyHospitals.html",details=details)

# @app.route("/Diagnosis/UserHome", methods=['GET', 'POST'])
# def DHome():
#     return render_template("UserHome.html")

@app.route("/SkinType", methods=['GET', 'POST'])
def SkinType():
    name = ''
    obj_name=''
    link=''
    text=''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            msg= 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            msg= 'No selected file'
        if file and allowed_file(file.filename):

            if request.form['Submit']:
                name=session['Username']
            filename = secure_filename(file.filename)
            sess = session['Username']
            path1 = UPLOAD_FOLDER + '/' + name + sess
            if os.path.isdir(path1):
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                os.mkdir(path1)
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                dir_list= []
            dir_list = os.listdir(path1)
            print(dir_list)
            print(path1+'11111111111')

            image_name = dir_list[-1]
            dir_list = []
            image1 = load_img(path1+'/'+image_name, target_size=(224, 224))
            image1 = img_to_array(image1)
            # reshape data for the model
            print(image1.shape)
            image1 = image1.reshape((1, image1.shape[0], image1.shape[1], image1.shape[2]))
            print(image1.shape)

            # prepare the image for the VGG model
            image1 = preprocess_input(image1)

            yhat = model2.predict(image1, verbose=0)[0]
            print(yhat)
            print(yhat.max())
            print(yhat[0])
            print(yhat[1])
            imp = ''
            
            if yhat[0] == yhat.max():
                obj_name = 'You are likely to have DRY SKIN'
                link = 'https://www.aad.org/public/everyday-care/skin-care-basics/dry/dry-skin-relief'
            elif yhat[1] == yhat.max():
                obj_name = 'You are likely to have OILY SKIN'
                link = 'https://www.aad.org/public/everyday-care/skin-care-basics/dry/oily-skin'
            text='Here is a skin care routine for your type!'          
            print('ppppppppp' + obj_name)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return render_template("SkinType.html", obj_name=obj_name, link=link, text=text)

@app.route("/Diagnosis2", methods=['GET', 'POST'])
def Diagnosis2():

    return render_template("Diagnosis2.html")

# @app.route("/NearbyClinics", methods=['GET', 'POST'])
# def NearbyHospitals():
    
#     return render_template("NearbyHospitals.html",details=details)

# DOCTOR------------------------------------------

@app.route("/DocHome", methods=['GET', 'POST'])
def DocHome():
    return render_template("DocHome.html")

@app.route("/DocProfile", methods=['GET', 'POST'])
def DocProfile():
    return render_template("DocProfile.html")

@app.route("/DocsSchedule", methods=['GET', 'POST'])
def DocsSchedule():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE dc_name=%s',[session['Username']])
    sch = cursor.fetchall()
    # cursor.execute('SELECT Doctor FROM doctors WHERE dc_id IN %s',[sch['Doctor']])
    # dc = cursor.fetchall()
    
        
    return render_template("DocsSchedule.html",sch=sch)

@app.route("/GivePrescription", methods=['GET', 'POST'])
def GivePrescription():
    msg=''
    print(session['Username'])
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM appointments WHERE dc_name=%s AND Mode="Online"',[session['Username']])
    details = cursor.fetchall()
    print(details)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            msg= 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            msg= 'No selected file'
        if file and allowed_file(file.filename):
            if request.form['Submit']:
                name=request.form.get('Submit')
            filename = secure_filename(file.filename)
            path1 = UPLOAD_FOLDER + '/' + name
            if os.path.isdir(path1):
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                os.mkdir(path1)
                app.config['UPLOAD_FOLDER'] = path1
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dir_list = os.listdir(path1)
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            d1=d1.split('/')
            d1='-'.join(d1)
            os.rename(path1+'/'+dir_list[-1], path1+'/'+d1+"."+filename.split('.')[-1])
            msg='Done'
    
    return render_template("GivePrescription.html", details=details, msg=msg)



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('Username', None)
    return redirect(url_for('index'))

if __name__ =="__main__":
    app.run(debug=True)