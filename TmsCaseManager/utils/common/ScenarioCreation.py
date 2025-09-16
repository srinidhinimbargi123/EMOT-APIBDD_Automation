import requests
import os

class ScenarioCreation:

    def __init__(self, base_url: str):
        base_url=base_url.lower().strip()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "environmentURL.txt"))    
        file = open(file_path, "r")
        lines=file.readlines()
        for line in lines:
            if base_url in line:
                self.url = line.split("=")[1].strip()
                break
        file.close()


    
    def senario_Creation(self,payload, token):
        url = f"{self.url}/api/v1/qa/atoms/scenario_manager/scenarios/"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, json=payload, headers=headers)

    
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    
        return response.json()
    

    def metric_Setter(self,payload, token,Scenario_id) :
        Scenario_id=str(Scenario_id)
        url = f"{self.url}/api/v1/qa/atoms/scenario_manager/scenarios/threshold/"+Scenario_id
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, json=payload, headers=headers)

    
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    
        return response.json()
    

    def activate_Scenario(self,payload, token,Scenario_id) :
        Scenario_id=str(Scenario_id)
        url = f"{self.url}/api/v1/qa/atoms/scenario_manager/scenarios/"+Scenario_id
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.patch(url, json=payload, headers=headers)

    
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    
        return response.json() 
    
    def scenario_Delete(self, token, scenario_id):
        url = f"{self.url}/api/v1/qa/atoms/scenario_manager/scenarios/"
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
        }
        payload = {
        "ids": [scenario_id]
        }

        response = requests.delete(url, json=payload, headers=headers)

    # Assert only status code
        assert response.status_code in [200, 204], f"Expected 200/204, got {response.status_code}"

        return response
