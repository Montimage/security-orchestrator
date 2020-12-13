import requests
import json

class ONOS(object):
    #TODO
    def __init__(self,api,token):
        self.api=api #"http://192.168.0.16:8181/onos/v1/"
        self.token=token #"Basic b25vczpyb2Nrcw=="

    def get_list_host(self):
        print(">>> SDNC <<< Get list of Hosts")
        url = self.api+'hosts'
        headers={"authorization":self.token}
        response = requests.get(url, headers=headers)
        return response.json()["hosts"]

    def add_rule(self,deviceId,macVnf,port):
        print(">>> SDNC <<< ADD RULE FORWARD PING FROM ETH_SRC "+macVnf+" TO PORT "+port)
        url = self.api+'flows/'+deviceId
        data={"priority": "40000","timeout": "0","isPermanent": True,"deviceId": deviceId,"treatment": {"instructions": [{"type": "OUTPUT","port": str(port)}]},"selector": {"criteria": [{"type": "ETH_SRC","mac": macVnf}]}}
        headers={'Content-Type': 'application/json',"authorization":self.token}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return