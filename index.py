from flask import Flask, redirect
import pandas as pd
import requests
import datetime
import traceback
import pygsheets

app = Flask(__name__)

global counter
counter = 1

global html_store
html_store = ""

global html_store1
html_store1 = ""

global store1_running
store1_running = False

def df2gsheet(secret_json, dataframe, destination_workbook, destination_sheet_name):
    # import pygsheets
    client = pygsheets.authorize(service_file=secret_json)
    wb = client.open(destination_workbook) #wb = client.open_by_key(destination_workbook) if want to open by key

    no_of_cols = len(dataframe.columns)
    no_of_rows = max(len(dataframe), 10000) #maximum no of rows. Increase the value as per your need. (Max limit 50,00,000 cells)
    if destination_sheet_name not in str(wb.worksheets()):
        wb.add_worksheet(destination_sheet_name,rows=no_of_rows,cols=no_of_cols)
    sheet = wb.worksheet_by_title(destination_sheet_name)
    sheet.clear()
    sheet.set_dataframe(dataframe, 'A1')

@app.route('/nepse/')
def nepse():
    global counter
    counter = counter + 1
    return str(counter)+' This is the time on the server '+str(datetime.datetime.now()) + '<br> This service is hosted on <a href="https://vercel.com/htdanil"> https://vercel.com/htdanil</a>'

@app.route('/nepse/store')
def store():
    # global headers
    global html_store
    try:
        html_store = requests.get("http://www.nepalstock.com/stocklive",timeout=60).text
        df = pd.read_html(html_store)[0]
        df['date_time'] = html_store.split('>As of')[1].split('</div>')[0].replace('&nbsp;','').replace('   ', ' ').strip()

        df2gsheet('my_secret_key.json', df, 'NEPSE_Analysis(new)','A')
        print("Success")
        return "Success"
    except:
        html_store = ""
        df2gsheet('my_secret_key.json', pd.read_html('<table><tr><th>BLANK</th></tr></table>')[0], 'NEPSE_Analysis(new)','A')
        print(traceback.format_exc())
        return "Fail"   

@app.route('/nepse/live_price')
def live_price():
    global html_store
    return html_store

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


#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug = False, port = 8844, threaded = False)
