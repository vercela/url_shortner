from flask import Flask, redirect
import pandas as pd
app = Flask(__name__)

@app.route('/')
def index():
   return '''This is a URL shortner service. <br> 
   <a href="https://docs.google.com/spreadsheets/d/1SgEqDUFMDjY0J28OiYsLgA_HUNAmtj9pnt-SyPGUYGA/edit"> Click here to update url-shortner database</a> <br>
   <br>
   This service is hosted on <a href="https://vercel.com/htdanil"> https://vercel.com/htdanil</a> and 
   git code to deploy is available on <a href="https://github.com/vercela/url_shortner">https://github.com/vercela/url_shortner</a>

   '''

@app.route('/<string:x>')
def redirect_link(x):
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTCIyvEmIH8UGd3T7L8dLHl5Gl4aA7LnSdd1OuS_sx0OFq_8WLd9gXfv-a80aKr6KDvGDoMt6LVQLBb/pub?gid=0&single=true&output=csv'
    df = pd.read_csv(url)
    try:
        url_to_return = df[df.end_point == x].iat[0,1]
        if 'http:' not in url_to_return and 'https:' not in url_to_return:
            url_to_return = 'http://{}'.format(url_to_return)
    except:
        url_to_return = 'https://docs.google.com/spreadsheets/d/1SgEqDUFMDjY0J28OiYsLgA_HUNAmtj9pnt-SyPGUYGA/edit'
    return redirect(url_to_return)
