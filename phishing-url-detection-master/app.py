#importing required libraries
import smtplib
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction
import time 

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        url = request.form["url"]
        # //exection time 
        start_time = time.time()
        obj = FeatureExtraction(url)
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time with multithreading :", execution_time, "seconds")

        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred =gbc.predict(x)[0]
                
                #CSV file 
        if y_pred == -1:
            df = pd.DataFrame({'Links':[url]})
            df.to_csv('listOfSites.csv', mode='a', index=False, header=False)
            # Uncomment to send mail or report website via mail
            #send_mail()

        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html',xx =round(y_pro_non_phishing,2),url=url )

        
    return render_template("index.html", xx =-1)



def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # with open('password.txt', 'r') as x:
    #   password = x.read()
    url = request.form["url"]
    #sample example of email and password 
    server.login('rohaney1992@gmail.com', 'vnxkmdxaxldfytqw')

    subject = "phishing please investigate "
    body = f"website that we found phising in our analysis {url}"
    #with open('body.txt', 'r') as n:
    #    body = n.read()
   
    msg = f"subject: {subject} \n\n {body}"

    server.sendmail(
        
        'rohaney1992@gmail.com',
        'shinderohan1011@gmail.com',
        #'reportphishing@apwg.org',
        msg
    )
    print('Message is sent succesfully!')


if __name__ == "__main__":
    app.run(debug=True)
    
    