
import requests
class AlertGeneration:
    @staticmethod
    def generate_Alerts(payload):
        url = "https://tms-client-routes-dev.solyticspartners.com/auth/v1/api-keys"   # replace <host> with actual host

        payload1 = {
            "username": "user_tms",
            "password": "user_tms",
            "org_name": "ATOMS",
            "expire_date": "2029-09-03"
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload1, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"[OK] API Key generated: {data['api_key']}")
            
        else:
            print(f"[FAIL] Status {response.status_code}: {response.text}")

        
        url_txn = "https://tms-client-routes-dev.solyticspartners.com/core/v1/transaction-screenings"

        txn_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "HTTPBearer": "Bearer "+data['api_key']   # feed the same key here
        }

        response_txn = requests.post(url_txn, json=payload, headers=txn_headers)

        if response_txn.status_code in (200, 201):
            print("[OK] Transaction screening submitted successfully")
            print(response_txn.json())
        else:
            print(f"[FAIL] Status {response_txn.status_code}: {response_txn.text}")