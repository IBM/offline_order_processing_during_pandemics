from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import numpy as np
import json
import os
import requests
from word2number import w2n 
import re
from werkzeug import secure_filename
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import SpeechToTextV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions
try:
    import ibm_db
except:
    pass
import ibm_boto3
import speech_recognition as sr
from googletrans import Translator


app = Flask(__name__)

app.config["UPLOAD_DIR"] = 'static/raw/'
apikey = ''
url = ''
assistantid = ''
sessionid = ''

# Initialize WKS Model Credentials

apikey = 'Up-GkTdHRFPL9C6ZAzWOn6VT9U2A11DhqtNVnCNfg9g7'
nlu_url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1233c082-8af9-4546-b7d7-9f4bdea1a793'
wks_model_id = '47fe6f4d-3a23-4014-8ef0-ce8fa5175213'

with open('credentials1.json', 'r') as credentialsFile:
    credentials1 = json.loads(credentialsFile.read())

dsn_driver = "IBM DB2 ODBC DRIVER"
dsn_database = credentials1['db'] 
dsn_hostname = credentials1['host']
dsn_port = "50000"                
dsn_uid = credentials1['username']      
dsn_pwd = credentials1['password']

dsn = (
    "DRIVER={{IBM DB2 ODBC DRIVER}};"
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "PROTOCOL=TCPIP;"
    "UID={3};"
    "PWD={4};").format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)

try:
    conn = ibm_db.connect(dsn, "", "")
except:
    pass


# Constants for Speech-To-Text values
STT_API_KEY_ID = ""
STT_URL = ""
language_customization_id = ""
acoustic_customization_id = ""

''' Methods for IBM Watson Speech-To-Text '''

with open('credentials.json', 'r') as credentialsFile:
    credentials = json.loads(credentialsFile.read())

STT_API_KEY_ID = credentials.get('apikey')
STT_URL = credentials.get('url')

authenticator = IAMAuthenticator(STT_API_KEY_ID)
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)
speech_to_text.set_service_url(STT_URL)


''' Method to handle POST upload '''


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    try:
        if request.method == 'POST':
            l = request.form
            lang = json.loads(l['SttLang'])
            f = request.files["audio"]
            filename_converted = f.filename.replace(
                " ", "-").replace("'", "").lower()
            # cmd = 'rm -r static/raw/*'
            # os.system(cmd)
            f.save(os.path.join(
                app.config["UPLOAD_DIR"], secure_filename(filename_converted)))
            print("\n##DEBUG##\n")
            print('Input: '+ filename_converted, 'Language: '+lang["language"])
            return transcribeAudio(filename_converted, lang["language"])
        
    except Exception as e:
        print("Unable {0}".format(e))
        myResponse = {"message": str(e)}
    except OSError as err:
        print("Unable {0}".format(e))
        myResponse = {"message": str(e)}

    return json.dumps(myResponse, indent=2)

''' Method to handle Transcription '''

def transcribeAudio(filename, lang):
    
    if lang == 'Hi':    
        r = sr.Recognizer()
        with sr.AudioFile(app.config["UPLOAD_DIR"]+filename) as source:
            audio = r.record(source)
        x = r.recognize_google(audio, language = "hi-IN")
        translator = Translator()
        y = translator.translate(x)
        print('Transcript: '+y.text)
        respo = { "transcript": filename.split('.')[0]+': ‬'+y.text,
                    "filepath" : app.config["UPLOAD_DIR"]+filename }

        return extractEntities(respo)
    
    elif lang == 'En':
        
        with open(app.config["UPLOAD_DIR"]+filename, 'rb') as audioSource:
            speech_recognition_results = speech_to_text.recognize(
            audio=audioSource,
            content_type='audio/wav',
            timestamps=True,
            model='en-US_BroadbandModel',
            word_alternatives_threshold=0.9
            ).get_result()
            
            transcript = ''
            for chunks in speech_recognition_results['results']:
                if 'alternatives' in chunks.keys():
                    alternatives = chunks['alternatives'][0]
                    if 'transcript' in alternatives:
                        transcript = transcript + alternatives['transcript']
            
            text = transcript.replace('%HESITATION', '')
            res = ""
            words = text.split()
            for word in words:
                try:
                    res = res + str(w2n.word_to_num(word)) + " "
                except:
                    res = res + word + " "
            val = 0
            text = ""
            res = res.split()
            count = 0
            for r in res:
                temp = re.findall(r'\d+', r)
                if len(temp) == 0:
                    count = 0
                    if val != 0:
                        x = str(val) + " " + r + " "
                        text = text + x
                        val = 0
                    else:
                        text = text + r +" "
                else:
                    count = count + 1
                    if count == 1:
                        if int(r) >= 100:
                            val = val + int(r)
                        elif int(r) < 100:
                            val = val + int(r)
                    if count == 2:
                        if val < 10 and int(r)<100:
                            val = (val*100) + int(r)
                        elif int(r) >= 100:
                            val = val*int(r)
                        elif int(r) < 100:
                            val = val + int(r)
       
            print('Transcript: '+text)
            respo = { "transcript": filename.split('.')[0]+': ‬'+text,
                        "filepath" : app.config["UPLOAD_DIR"]+filename }

            return extractEntities(respo)
    

def extractEntities(transcriptText):
    
    authenticator = IAMAuthenticator(apikey)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version = '2019-07-12',
        authenticator = authenticator
    )
    
    natural_language_understanding.set_service_url(nlu_url)
    
    response = natural_language_understanding.analyze(
        text=transcriptText.get("transcript"),
        features=Features(entities=EntitiesOptions(model=wks_model_id))).get_result()
    
    name = ''
    address = ''
    phone = ''
    orders = ''
    
    for entity in response['entities']:
        if entity['type'] == "ADDRESS":
            address = entity['text']
        
        if entity['type'] == "CUSTOMER_NAME":
            name = entity['text']
        
        if entity['type'] == "ORDER_ITEMS":
            orders = entity['text']
        
        if entity['type'] == "CUSTOMER_PHONE":
            phone = entity['text']
   
    response.update({'filepath': transcriptText.get('filepath')})
    print('WKS ENTITIES DETECTED: ')
    print('(NAME): '+name, ('(PHONE): ')+phone, ('(ORDERS): ')+orders, ('(ADDRESS): ')+address, sep="\n")
    
    try:
        ids = getIDs() + 1
    except:
        pass
    
    a="\'"
    n = a+name+a
    o = a+orders+a
    p = a+phone+a
    add = a+address+a
    insert = 'INSERT INTO RVB49192.ORDERS VALUES(%d, %s, %s, %s, %s)' %(ids, n, p, o, add)
    try:
        ibm_db.exec_immediate(conn, insert)
    except:
        pass
    
    return jsonify(response)

@app.route('/deleteRecord/<int:ID>')
def deleteRecord(ID):
    delete_statement= 'DELETE FROM RVB49192.ORDERS WHERE "ID" = {0};'.format(ID)
    try:
        ibm_db.exec_immediate(conn, delete_statement)
        return {'flag': 'success'}
    except:
        return {'flag': 'failed'}


@app.route('/getDatabaseContents')
def getDatabaseContentsJson():
    select_statement = 'SELECT * FROM RVB49192.ORDERS ORDER BY ID desc;'
    try:
        res = ibm_db.exec_immediate(conn, select_statement)
        
        result = ibm_db.fetch_both(res)
        resultDict = []
        while(result):
            returnDictBuffer = {'ID': result['ID'],
                            'NAME': result['NAME'],
                            'PHONE': result['PHONE'],
                            'ORDERS': result['ORDERS'],
                            'ADDRESS': result['ADDRESS']}
            resultDict.append(returnDictBuffer)
            result = ibm_db.fetch_both(res)
            
        return jsonify(resultDict)
    except:
        resultDict = []
        returnDictBuffer = {'ID': 0,
                            'NAME': 'db2 not connected!',
                            'PHONE': '',
                            'ORDERS': '',
                            'ADDRESS': ''}
        resultDict.append(returnDictBuffer)
        return jsonify(resultDict)

def getIDs():
    select_statement = 'SELECT ID FROM RVB49192.ORDERS ORDER BY ID desc;'
    try:
        stmt = ibm_db.exec_immediate(conn, select_statement)
        finalID = 0
        result = ibm_db.fetch_both(stmt)
        finalID = int(result['ID'])
        return finalID
    except:
        return 0


@app.route('/')
def index():
    
    return render_template('index.html')

port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)
