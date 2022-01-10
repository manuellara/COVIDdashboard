# COVID Dashboard sync tool for TUSD

#### <b>System Requirements:
- Docker
- Windows enviornment </b>

## Summary
This tool will: 
1. Grab student data from the <b>Responses COVID-19 Form</b> (Dashboard Data tab) Excel sheet (via Microsoft Graph API) on a private Sharepoint site 
2. Grab staff data from the <b>Responses COVID-19 Form</b> (Dashboard Data tab) Excel sheet (via Microsoft Graph API) on a private Sharepoint site
3. Update the <b>Positive/Confirmed COVID Cases Students and Staff</b> (Current Enrollment Staff/Students tab) Google sheet.

## Directions:
First, navigate into the project folder 
```
cd COVID Dashboard
```

Then run the 'automate' Powershell script (not included in this repo)
```
.\automate.ps1
```

If the 'COVID' Docker image is already on your system, the script will run fine. If not, the script will build the image first, then attempt to run

#### <b>Please note that the .env file for the Dockerfile is not included in this repo</b> 

## Result
If the process runs successfully, a MS Teams webhook should be sent to a private channel


