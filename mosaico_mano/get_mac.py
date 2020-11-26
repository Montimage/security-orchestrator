import subprocess
import requests
import json
import time
import sys
import yaml


from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin






app = Flask(__name__)
CORS(app)

@app.route('/api/alert', methods=['POST'])
def post_api():
    data=request.json
    #print(data["id"])
    id_vnf=data["id"]
    result = subprocess.run(['osm', 'ns-list'], stdout=subprocess.PIPE)
    output=str(result.stdout.decode('ascii')).split('\n')
    isFoundFirewall=False
    for o in output:
        if("firewall" in o):
            print(">>> NFVO <<< Firewall FOUND :"+o.split('|')[1].split(' ')[1])
            print(">>> POLICY <<< Activate Trigger update_firewall")
            isFoundFirewall=True
    if(not isFoundFirewall):
        print(">>> NFVO <<< Firewall NOT FOUND")
        print(">>> POLICY <<< Activate Trigger deploy_firewall")
        print(">>> NFVO <<< Deploy Firewall NS")
        ts = time.time()
        result = subprocess.run(['osm', 'ns-create', '--nsd_name', 'firewall', '--ns_name' ,'firewall_'+str(ts), '--vim_account', 'emu-vim1'], stdout=subprocess.PIPE)
        output=str(result.stdout.decode('ascii')).split('\n')
        isFirewallUp=False
        while(not isFirewallUp):
            time.sleep(10)
            try:            

                result = subprocess.run([ 'docker', 'ps'], stdout=subprocess.PIPE)
                output=str(result.stdout.decode('utf-8')).split('\n')
                for o in output:
                    if('mn.dc1_firewall_'+str(ts)+'-1-ubuntu-1' in o):
                        isFirewallUp=True                    
                        result = subprocess.run([ 'docker', 'exec', 'mn.dc1_firewall_'+str(ts)+'-1-ubuntu-1', 'ping', '192.168.100.2', '-c', '5'], stdout=subprocess.PIPE)
                        output=str(result.stdout.decode('utf-8')).split('\n')
                        break
                print(">>> NFVO <<< Firewall is not ready")
            except:
                print(">>> NFVO <<< Firewall is not ready")
                pass


    result = subprocess.run(['osm', 'ns-list'], stdout=subprocess.PIPE)
    output=str(result.stdout.decode('ascii')).split('\n')
    nsid=""
    for o in output:
        if(data["ns"] in o):
            nsid=o.split('|')[2].split(' ')[1]
            print(">>> NFVO <<< Network Service name "+data["ns"]+" - ID: "+nsid)
    result = subprocess.run(['osm', 'vnf-list'], stdout=subprocess.PIPE)
    output=str(result.stdout.decode('ascii')).split('\n')
    vnfs=[]
    for o in output:
        if(nsid in o):
            print(">>> NFVO <<< VNF "+o.split("| ")[4].split(" ")[0]+" - ID: "+o.split("| ")[1])
            vnfs.append(o.split("| ")[1].split(" ")[0])    
    macs=[]
    for v in vnfs:
        result = subprocess.run(['osm', 'vnf-show',v], stdout=subprocess.PIPE)
        output=str(result.stdout.decode('ascii')).split('\n')
        for o in output:
            if("mac" in o):
                print(">>> NFVO <<< VNF "+v+" - MAC: "+o.split('"')[3])
                macs.append(o.split('"')[3])



    print(">>> SDNC <<< Get list of Hosts")
    url = 'http://192.168.0.16:8181/onos/v1/hosts'
    headers={"authorization":"Basic b25vczpyb2Nrcw=="}
    response = requests.get(url, headers=headers)
    port="4"
    max_ip=2
    for h in response.json()["hosts"]:
        print(">>> SDNC <<< MAC "+h["mac"]+" - IP "+h["ipAddresses"][0]+" - Port "+h["locations"][0]["port"])
        if(int(h["ipAddresses"][0].split('.')[3])>max_ip):
            max_ip=int(h["ipAddresses"][0].split('.')[3])
            port=h["locations"][0]["port"]
    #print(macs)
    url = 'http://192.168.0.16:8181/onos/v1/flows/of:00000000000003e9'
    data={"priority": "40000","timeout": "0","isPermanent": True,"deviceId": "of:00000000000003e9","treatment": {"instructions": [{"type": "OUTPUT","port": str(port)}]},"selector": {"criteria": [{"type": "ETH_SRC","mac": macs[int(id_vnf)-1]}]}}
    headers={'Content-Type': 'application/json',"authorization":"Basic b25vczpyb2Nrcw=="}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(">>> SDNC <<< ADD RULE FORWARD PING FROM ETH_SRC "+macs[int(id_vnf)-1]+" TO PORT "+port)

    return {"status":"ok"}

@app.route('/api/deploy', methods=['POST'])
def post_api_deploy():
    data=request.json
    #print(data["tosca"])
    with open(data["tosca"]) as f:
    
        docs = yaml.load_all(f, Loader=yaml.FullLoader)

        for doc in docs:
            
            for k, v in doc.items():
                if(k=="vnfd"):
                    for vnfd in v:
                        print(">>> NFVO <<< Onboarding VNFD: "+ vnfd)
                        result = subprocess.run(['osm', 'vnfd-create',vnfd], stdout=subprocess.PIPE)
                elif(k=="nsd"):
                    for nsd in v:
                        print(">>> NFVO <<< Onboarding NSD: "+ nsd)
                        result = subprocess.run(['osm', 'nsd-create',nsd], stdout=subprocess.PIPE)
                elif(k=="ns"):
                    for ns in v:
                        cmd=['osm', 'ns-create']
                        for key,value in ns.items():
                            cmd.append("--"+key)
                            if(key=="ns_name"):
                                ts = time.time()
                                cmd.append(value+str(ts))
                            else:
                                cmd.append(value)
                        print(">>> NFVO <<< Deploy NS: "+ ns["ns_name"])
                        result = subprocess.run(cmd, stdout=subprocess.PIPE)
                        isRoutersUp=False
                        while(not isRoutersUp):
                            time.sleep(10)
                            try:            

                                result = subprocess.run([ 'docker', 'ps'], stdout=subprocess.PIPE)
                                output=str(result.stdout.decode('utf-8')).split('\n')
                                for o in output:
                                    if('mn.dc1_router'+str(ts)+'-3-ubuntu-1' in o):
                                        isRoutersUp=True                    
                                        result = subprocess.run([ 'docker', 'exec', 'mn.dc1_router'+str(ts)+'-3-ubuntu-1', 'ifconfig'], stdout=subprocess.PIPE)
                                        output=str(result.stdout.decode('utf-8')).split('\n')
                                        for o in output:
                                            if ("192.168.100." in o):
                                                ip=o.split()[1]
                                                #print(o.split())
                                                break
                                        
                                        result = subprocess.run([ 'docker', 'exec', 'mn.dc1_router'+str(ts)+'-1-ubuntu-1', 'ping', ip, '-c', '5000'], stdout=subprocess.PIPE)
                                        output=str(result.stdout.decode('utf-8')).split('\n')
                                        result = subprocess.run([ 'docker', 'exec', 'mn.dc1_router'+str(ts)+'-2-ubuntu-1', 'ping', ip, '-c', '5000'], stdout=subprocess.PIPE)
                                        output=str(result.stdout.decode('utf-8')).split('\n')
                                        break
                                print(">>> NFVO <<< Routers are not ready")
                            except:
                                print(">>> NFVO <<< Routers are not ready")
                                pass

    return {"status":"ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600,debug=True)
