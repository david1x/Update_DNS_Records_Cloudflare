from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

API_TOKEN=os.getenv("API_TOKEN")
ZONE_ID=os.getenv("ZONE_ID")
DOMAIN=os.getenv("DOMAIN")
RECORDS=os.getenv("RECORDS")

# Cloudflare API token and zone_id
api_token = API_TOKEN
zone_id = ZONE_ID

cloud_api_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"


domain = DOMAIN
dns_records = os.getenv("RECORDS").split(" ") 
# use split if there are multiple records | exp. in .env - 'RECORD=contact about' | split output 'records = ['contact', 'about']'


def get_public_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        return response.json()["ip"]
    raise Exception(f"Request to get public ip has failed. status code {response.status_code}")

def ip_changed(public_ip):
    with open("ip.txt", "r") as ip_file:
        previous_ip = ip_file.readline()
        print(f"Previous public IP address: {previous_ip}")
        
        if previous_ip == public_ip:
            return False
        return True

def get_record_id(record_name: str) -> list:
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    params = {
        "name": f"{record_name}.{domain}",
        "type": "A",
    }

    response = requests.get(cloud_api_url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()["result"]
        if result:
            return result[0]["id"]
        else:
            raise Exception(f"No matching DNS record found for {record_name}.{domain}")
    else:
        raise Exception(f"Error fetching DNS records. Status code: {response.status_code}")


def update_dns_record(record_id, ip, record_name):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    data = {
        "type": "A",
        "name": f"{record_name}.{domain}",
        "content": ip,
        "ttl": 1,
        "proxied": True, 
    }

    response = requests.put(f"{cloud_api_url}/{record_id}", headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"DNS record [{record_name}] with ID {record_id} updated successfully.")
    else:
        print(f"Error updating DNS record. Status code: {response.status_code}")
        exit(1)


if __name__ == "__main__":
    try:
        public_ip = get_public_ip()
        print(f"Current public IP address: {public_ip}")
        
        if ip_changed(public_ip):
            
            with open("ip.txt", "w") as ip_file:
                ip_file.write(public_ip)
                
            for record in dns_records:
                record_id = get_record_id(record)
                print(f"Found record with the name: {record}")

                update_dns_record(record_id, public_ip, record)
        else:
            print(f'Public ip ({public_ip}) has not changed, No update required.\nexit(0)')
            exit(0)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit(1)
