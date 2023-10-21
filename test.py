import requests

customer_email = "inwardsynctest1@test.com"

response = requests.get(f"http://127.0.0.1:8080/get_id/{customer_email}", headers={'Content-Type': 'application/json'})

print(response.status_code)
print(response.json())