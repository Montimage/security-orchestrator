import requests
import json
print(">>> SDNC <<< Get list of Hosts")
url = 'http://192.168.0.16:8181/onos/v1/hosts'
headers={"authorization":"Basic b25vczpyb2Nrcw=="}
response = requests.get(url, headers=headers)
port="4"
for h in response.json()["hosts"]:
    print(">>> SDNC <<< MAC "+h["mac"]+" - IP "+h["ipAddresses"][0]+" - Port "+h["locations"][0]["port"])
    if(int(h["ipAddresses"][0].split('.')[3])>5):
        port=h["locations"][0]["port"]

url = 'http://192.168.0.16:8181/onos/v1/flows/of:00000000000003e9'
data={"priority": "40000","timeout": "0","isPermanent": True,"deviceId": "of:00000000000003e9","treatment": {"instructions": [{"type": "OUTPUT","port": "4"}]},"selector": {"criteria": [{"type": "ETH_SRC","mac": macs[int(sys.argv[2])-1]}]}}
headers={'Content-Type': 'application/json',"authorization":"Basic b25vczpyb2Nrcw=="}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(">>> SDNC <<<  ADD RULE FORWARD PING FROM ETH_SRC "+macs[int(sys.argv[2])-1]+" TO PORT"+port)
