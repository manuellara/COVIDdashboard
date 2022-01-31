import gspread
import datetime
from msgraph import msgraphapi
import requests
import pymsteams
import os


def msapi():
    # initialize msgraphapi object
    connector = msgraphapi()

    # get Access Token
    connector.getAccessToken()

    # get students result
    connector.getAction("student")
    stuLst = connector.makeRequest()

    # get staff result
    connector.getAction("staff")
    stfLst = connector.makeRequest()

    # get total result
    connector.getAction("total")
    stuTot = connector.makeRequest()

    # returns list of lists and counts
    return stuLst["values"], len(stuLst["values"]), stfLst["values"], len(stfLst["values"]), stuTot["values"], len(stuTot["values"])

def gspreadtogsheets(stuLst, stuCnt, stfLst, stfCnt, stuTot, stuTotCnt):
    try:
        # get service account creds
        gc = gspread.service_account(filename='service_account.json')

        # must share to service acccount beforehand
        # open google sheet
        sh = gc.open('Positive/Confirmed COVID Cases Students and Staff')

        # get 3rd tab (Copy of Current Enrollment Staff/Students)
        # or get wksht by index (e.g. worksheet = sh.get_worksheet(0))
        worksheet = sh.worksheet('Current Enrollment Staff/Students')

        # update Google sheet cells based on student list of lists
        worksheet.update(f'G2:G{stuCnt + 1}', stuLst)

        # update Google sheet cells based on staff list of lists
        worksheet.update(f'I2:I{stfCnt + 1}', stfLst)

        # update Google sheet cells based on student total list of lists
        worksheet.update(f'E2:E{stuTotCnt + 1}', stuTot)

        # returns date in MM/dd/yyy format
        current_day = getCurrentDate()

        # update Google sheet cell C34 with last modified date (mm/dd/yyyy)
        worksheet.update('C34', current_day)

        ## send MS Teams webhook
        successMsWebhook(stuLst[-1][0], stfLst[-1][0])
    except Exception as e:
        # send MS Teams failed webhook
        failedMsWebhook(e)

def successMsWebhook(stu, stf):
    # create connector card
    myTeamsMessage = pymsteams.connectorcard(os.environ["webhookURL"])

    # set title
    myTeamsMessage.title("COVID Dashboard update")

    # add link to Google Sheet
    myTeamsMessage.addLinkButton("Positive/Confirmed cases Google Sheet ", "https://docs.google.com/spreadsheets/d/1z_Nvr6D4Ouv8hq2ChHxEEP_c-MawV-RiAVuwRZu_i1Q/edit?usp=sharing")

    # set body
    myTeamsMessage.text(f'''
    Summary:
        Student count: {stu}
        Staff count: {stf}
    ''')

    # send the webhook
    myTeamsMessage.send()

def failedMsWebhook(e):
    # create connector card
    myTeamsMessage = pymsteams.connectorcard(os.environ["webhookURL"])

    # set title
    myTeamsMessage.title("COVID Dashboard update: FAILED")

    # add link to Google Sheet
    myTeamsMessage.addLinkButton("Positive/Confirmed cases Google Sheet ", "https://docs.google.com/spreadsheets/d/1z_Nvr6D4Ouv8hq2ChHxEEP_c-MawV-RiAVuwRZu_i1Q/edit?usp=sharing")

    # set body
    myTeamsMessage.text(f"There was an issue with the COVID Dashboard sync...\n{e}")

    # send the webhook
    myTeamsMessage.send()

def getCurrentDate():
    ## get today's date 
    # datetime endpoint
    URL = "http://worldclockapi.com/api/json/pst/now"

    # make request
    r = requests.get(url = URL)

    # convert request to json
    data = r.json()

    # get currentDateTime attribute in weird format
    dt = data['currentDateTime']

    # split currentDateTime on T
    date = dt.split('T')

    # convert date string to datetime object
    date_time = datetime.datetime.strptime(date[0], '%Y-%m-%d')

    # format datetime object to mm/dd/yyy
    current_day = datetime.date.strftime(date_time.date(), "%m/%d/%Y")

    return current_day

# Create list of lists
stuLst, stuCnt, stfLst, stfCnt, stuTot, stuTotCnt = msapi()

# upload to Google sheets
gspreadtogsheets(stuLst, stuCnt, stfLst, stfCnt, stuTot, stuTotCnt)
