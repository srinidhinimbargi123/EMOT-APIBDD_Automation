import requests
import os

class loginHelper:

    @staticmethod
    def TMS_CaseManagerLogin() -> str:
        url = "https://keycloak.nonprod.solytics.us/realms/ATOMS/protocol/openid-connect/token"
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "credentialsWrite.txt"))   # need to fix this


        file = open(file_path, "r")
        lines=file.readlines()
        username=""
        password=""
        for line in lines:
            if "Username" in line:
                username = line.split("=")[1].strip()
                
            elif "Password" in line:
                password=line.split("=")[1].strip()

        file.close()
        
        payload = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": "EMOT",
            "redirect_uri": "https://tms-dev.solyticspartners.com/scenario-manager",
            "code_verifier": "Jx6wyRLRAJkHeKetV8ky1WVEgCkjrqc3EipLY6ozN9mCjk2Fd7gV8Y362S4A6VdbzvhS3Oi24kDhzUXU0XGpVBWEt2s8zNu6",
            "code": "14fcb792-9599-44cf-9bd6-4b633c6acd36.e6a562c9-1367-4085-830a-846067d3a420.451d3379-64de-4c2b-a92d-f5d78f51f4d0"
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception(f"Login failed: {response.status_code} - {response.text}")


    @staticmethod
    def TMS_CaseManagerLoginforGui():
        url = "https://keycloak.nonprod.solytics.us/realms/ATOMS/protocol/openid-connect/token"
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "credentialsWrite.txt"))   # need to fix this


        file = open(file_path, "r")
        lines=file.readlines()
        username=""
        password=""
        for line in lines:
            if "Username" in line:
                username = line.split("=")[1].strip()
                
            elif "Password" in line:
                password=line.split("=")[1].strip()

        file.close()
        
        payload = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": "EMOT"
            # "redirect_uri": "https://tms-dev.solyticspartners.com/scenario-manager"
            # "code_verifier": "Jx6wyRLRAJkHeKetV8ky1WVEgCkjrqc3EipLY6ozN9mCjk2Fd7gV8Y362S4A6VdbzvhS3Oi24kDhzUXU0XGpVBWEt2s8zNu6",
            # "code": "14fcb792-9599-44cf-9bd6-4b633c6acd36.e6a562c9-1367-4085-830a-846067d3a420.451d3379-64de-4c2b-a92d-f5d78f51f4d0"
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            return None