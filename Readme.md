# COVID Dashboard sync tool

#### <b>System Requirements:
- Docker
- Windows enviornment </b>

## Summary
This tool will grab the data from the <b>Responses COVID-19 Form</b> (Dashboard Data tab) Excel sheet (via Microsoft Graph API) on a private Sharepoint site and update the <b>Positive/Confirmed COVID Cases Students and Staff</b> (Current Enrollment Staff/Students tab) Google sheet.

## Step 1:
First, navigate into the project folder 
```
cd COVID Dashboard
```

Then run the 'automate' Powershell script
```
.\automate.ps1
```

If the 'COVID' Docker image is already on your system, the script will run fine. If not, the script will build the image first, then attempt to run as intended

#### <b>Please note that you must set the Windows env variables for the process to work</b> 

## Result
If the process runs successfully, a MS Teams webhook should be sent to the 'Automate' channel


