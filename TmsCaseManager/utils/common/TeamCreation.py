import requests
import os

class TeamCreation:

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


    def get_team(self,token):
        url = f"{self.url}/api/v1/qa/atoms/team_management/teams/?page=1&page_size=5&search=Atomation+of+API"
    
        headers = {
        # Add Authorization if required, e.g.:
        "Authorization": f"Bearer {token}"
        }
    
        response = requests.get(url, headers=headers)
    
    # Handle errors gracefully
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status {response.status_code}: {response.text}")
            return None


    def role_Create(self,payload, token):
        url = f"{self.url}/api/v1/qa/atoms/team_management/roles/"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, json=payload, headers=headers)

    
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    
        return response.json()

    def role_Assign(self,payload, token):
        url = f"{self.url}/api/v1/qa/atoms/team_management/user-roles/"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, json=payload, headers=headers)

    
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    
        return response.json()

    
    def role_Delete(self,token, team_id):
        team_id=str(team_id)
        url = f"{self.url}/api/v1/qa/atoms/team_management/roles/?role_id="+team_id
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.delete(url, headers=headers)

        # Assert only status code
        assert response.status_code in [200, 204], f"Expected 200/204, got {response.status_code}"


    def team_Create(self,payload, token):
        url = f"{self.url}/api/v1/qa/atoms/team_management/teams/"
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, json=payload, headers=headers)

    
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    
        return response.json()

        

    
    def team_Delete(self,token, team_id):
        team_id=str(team_id)
        url = f"{self.url}/api/v1/qa/atoms/team_management/teams/?team_id="+team_id
        headers = {
            'Content-Type': 'application/json',
            "Authorization": f"Bearer {token}"
        }
        response = requests.delete(url, headers=headers)

        # Assert only status code
        assert response.status_code in [200, 204], f"Expected 200/204, got {response.status_code}"



    def get_roleid(self,token, role_name):
        url = f"{self.url}/api/v1/qa/atoms/team_management/teams/roles/"
        params = {
        "page": 1,
        "page_size": 5,   # increase if you expect many roles
        "search": role_name
    }
        headers = {
        # Add Authorization if required, e.g.:
        "Authorization": f"Bearer {token}"
        }
    
        response = requests.get(url,params=params,headers=headers)
    
    # Handle errors gracefully
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status {response.status_code}: {response.text}")
            return None