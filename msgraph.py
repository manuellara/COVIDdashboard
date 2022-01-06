
import requests
import msal
import json
import logging
import os
# from dotenv import dotenv_values # change os.environ => config 


# loads .env file, returns dict of values
# os.environ = dotenv_values(".env")


class msgraphapi:
    result = None

    def getAccessToken(self):
        # initialize app 
        app = msal.ConfidentialClientApplication(
            os.environ["client_id"],
            authority=os.environ["authority"],
            client_credential=os.environ["secret"],)

        # attempts to aquire token
        msgraphapi.result = app.acquire_token_silent([os.environ["scope"]], account=None)

        # if token does not esits, print error message
        if not msgraphapi.result:
            logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
            msgraphapi.result = app.acquire_token_for_client(scopes=[os.environ["scope"]])

    def getAction(self, action):
        # which data to grab (e.g. Staff or Students)
        self.action = action
    
    def makeRequest(self):
        # determine which endpoint to hit
        if (self.action == "student"):
            endpoint = os.environ["stu_endpoint"]
        if (self.action == "staff"):
            endpoint = os.environ["stf_endpoint"]
        if (self.action == "total"):
            endpoint = os.environ["tot_endpoint"] 

        # if access token exists
        if "access_token" in msgraphapi.result:
            # Call Graph API using the access token
            graph_data = requests.get(
                endpoint,
                headers={'Authorization': 'Bearer ' + msgraphapi.result['access_token']}, ).json()

            # print(f'Graph API call result for {self.action}: ')
            
            # converts JSON obj to string
            result = json.dumps(graph_data)
            # converts JSON str to dict (python readable version of JSON)
            data = json.loads(result)

            return data
        else:
            print(msgraphapi.result.get("error"))
            print(msgraphapi.result.get("error_description"))
            print(msgraphapi.result.get("correlation_id"))  # You may need this when reporting a bug

