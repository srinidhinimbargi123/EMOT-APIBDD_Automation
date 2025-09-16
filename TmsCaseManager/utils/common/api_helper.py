import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))   # need to fix this
import json
from typing import Any, Optional
import requests
from typing import Any
from TmsCaseManager.utils.endpoints_Location.endPointsLocation import EndPointsCaseManager, EndPointsTMS
import json 
 

class ApiHelper:
    URL = ""
    endPoint = ""
    payload = None

    def __init__(self, base_url: str):
        base_url=base_url.lower().strip()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "environmentURL.txt"))    
        file = open(file_path, "r")
        lines=file.readlines()
        for line in lines:
            if base_url in line:
                self.URL = line.split("=")[1].strip()
                break
        file.close()


    
    def TestApi(self,apiMethod, BearerToken, endPoint, payload: Optional[dict] = None,files=None):
        apiMethod=apiMethod.lower().strip()
        content_type = None if files else "application/json"
        headers = self.create_headers(BearerToken, content_type=content_type, files=files)

        if apiMethod == "get":

           return requests.get(
                self.URL + endPoint, headers=headers
            )


        elif apiMethod == "post":
            if files:
                
                return requests.post(self.URL + endPoint, headers=headers, files=files, data=payload)
            return requests.post(
                self.URL + endPoint,
                headers=headers,
                json=payload,
            )


        elif apiMethod == "put":
            if files:
                return requests.put(
                self.URL + endPoint,
                headers=headers,
                files=files,
                data=payload
            )
            return requests.put(
                self.URL + endPoint,
                headers=headers,
                json=payload,
            )
            

        elif apiMethod == "delete":
            return requests.delete(
                self.URL + endPoint, headers=headers
            ) 
            

    def update_key_in_payload(self,payload: Any, target_key: str, new_value: Any):
        if isinstance(payload, dict):
         for key, value in payload.items():
            if key == target_key:
                payload[key] = new_value
            else:
                self.update_key_in_payload(value, target_key, new_value)
        elif isinstance(payload, list):
            for item in payload:
                self.update_key_in_payload(item, target_key, new_value)
        return payload



    def update_Endpoint(self, endpointName, oldValue, newValue):
        endpointName=endpointName.lower().strip()
        if endpointName in EndPointsCaseManager:
            endpoint_path = EndPointsCaseManager[endpointName]
            updated_path = endpoint_path.replace(oldValue, newValue)
        return updated_path


    @staticmethod
    def validateStatusCode(response, status_code):
        assert response.status_code == status_code, (
        f"Expected status {status_code} but got {response.status_code}. "
    )

    @staticmethod
    def print_response(response):
         print("response : ",response.json())
         return response.json()
       

    @staticmethod
    def extract_data(json,key):
        if isinstance(json,dict):
            for k,v in json.items():
                if k == key:
                    return v
                result = ApiHelper.extract_data(v,key)
                if result is not None:
                    return result
        elif isinstance(json,list):
            for item in json:
                result=ApiHelper.extract_data(item,key)
                if result is not None:
                    return result
        return None


    @staticmethod
    def extract_data_from_response(response,key):
        return ApiHelper.extract_data(response,key)

    
    @staticmethod
    def get_EndPoints(Module,endPoint):
        Module = Module.lower().strip()
        endPoint = endPoint.lower().strip()
        if Module == "casemanager" and endPoint in EndPointsCaseManager:
            endPoint = EndPointsCaseManager[endPoint]
            return endPoint

        elif Module == "tms" and endPoint in EndPointsTMS:
            endPoint = EndPointsTMS[endPoint]
            return endPoint
    

    @staticmethod
    def create_headers(token: str, content_type: Optional[str] = "application/json", files=None) -> dict: # not using
        headers = {"Authorization": f"Bearer {token}"}
        if not files and content_type:
            headers["Content-Type"] = content_type


        if files is not None and "Content-Type" in headers:
            headers.pop("Content-Type")

        return headers



    @staticmethod
    def get_Payload(Module, payloadName):
        payload = None
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        
        if Module.lower() == "casemanager":
            file_path = os.path.join(base_path,"data", "case_payloads.json")
        elif Module.lower() == "tms":
            file_path = os.path.join(base_path,"data", "tms_payloads.json")
        else:
            print(f"[ERROR] Unknown module: {Module}")
            return None

        try:
            with open(file_path, "r") as f:
                all_payloads = json.load(f)
                payload = all_payloads.get(payloadName)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in: {file_path}")

        return payload

    @staticmethod
    def upload_case_document(filename: str):     # not using
        try:
            file_path = os.path.join("data", filename)
            files = {
                "document": (filename, open(file_path, "rb"),"application/pdf")
            }
            return files
        except FileNotFoundError:
            print(f"[ERROR] File not found: {file_path}")
            return None


   

    @staticmethod
    def output_Payload_Assert(response, value):
        import json

        def recursive_search(data, key):
            """Recursively search for a key in nested dict/list"""
            if isinstance(data, dict):
                if key in data:
                    return True
                return any(recursive_search(v, key) for v in data.values())

            elif isinstance(data, list):
                return any(recursive_search(item, key) for item in data)

            return False

        json_data = response.json()
        found = recursive_search(json_data, value)

        assert found, f" Key '{value}' not found anywhere in response:\n{json.dumps(json_data, indent=2)}"
        print(f" Key '{value}' found somewhere in the response.")

    @staticmethod
    def _load_env_name() -> str:
        try:
            env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "environmentURLWrite.txt"))  # need to fix this
            with open(env_path, "r", encoding="utf-8") as f:
                print(f.read().strip())
                return f.read().strip()
        except Exception:
            return "dev"  


 









