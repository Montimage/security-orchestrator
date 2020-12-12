import requests
import yaml
import json
import subprocess
import os
import time
import sys
#from flask import Flask, jsonify, request
#from flask_cors import CORS
#app = Flask(__name__)

#CORS(app)

#@app.route('/api/stt', methods=['GET'])
def proxypost():
    _ip="10.0.1.11"
    #_ip=request.args.get('ip')
    #nsd_name=request.args.get('_ip')
    token_request = requests.post('https://%s:9999/osm/admin/v1/tokens' % _ip,data={'username': 'admin', 'password': 'admin'}, verify=False)
    token = yaml.safe_load(token_request.text)["id"]
    r = requests.get('https://'+_ip+':9999/osm/vnfpkgm/v1/vnf_packages',headers ={'Authorization': 'Bearer %s' % token}, verify= False)
    vnfds=(yaml.safe_load(r.text))
    print(vnfds)
    r = requests.get('https://'+_ip+':9999/osm/nsd/v1/ns_descriptors',headers ={'Authorization': 'Bearer %s' % token}, verify= False)
    nsd=(yaml.safe_load(r.text))
    print(nsd)
    count=0
    for ns in nsd:
        if(sys.argv[1]==ns["name"]):
            print(ns)
            nfs=[]
            f = open("sid", "r")
            sid=int(f.readline().replace("\n",""))
            f.close()
            for vnf in ns["constituent-vnfd"]:      
                    count=count+1          
                    print(vnf["member-vnf-index"])
                    print(vnf["vnfd-id-ref"])
                    for v in vnfds:
                        if(v["name"]==vnf["vnfd-id-ref"]):
                            #print(v["vdu"][0]["vdu-configuration"]["initial-config-primitive"][0]["parameter"][0]["value"])
                            cmd=v["vdu"][0]["vdu-configuration"]["initial-config-primitive"][0]["parameter"][0]["value"]
                            isFailed=True
                            while(isFailed):
                                result = subprocess.run(['docker','exec','mn.dc1_'+sys.argv[2]+'-'+vnf["member-vnf-index"]+'-'+v["name"]+'-1','ps','-eaf'], stdout=subprocess.PIPE)
                                output=str(result.stdout.decode('utf-8')).split('\n')
                                for o in output:
                                    if("openNetVM" in o):
                                        isFailed=False
                                        break
                                if(isFailed):
                                    print(">>>> START OpenNetVM NF "+v["name"])
                                    if(ns["name"]=="2flows_ns"):
                                        if(v["name"]=="flow_forward"):
                                            os.system('docker exec mn.dc1_'+sys.argv[2]+'-'+vnf["member-vnf-index"]+'-'+v["name"]+'-1 sh -c "'+cmd.replace("<SID>",str(sid+1)).replace("<DID>",str(sid+2))+'" &')
                                        elif(v["name"]=="firewall"):
                                            os.system('docker exec mn.dc1_'+sys.argv[2]+'-'+vnf["member-vnf-index"]+'-'+v["name"]+'-1 sh -c "'+cmd.replace("<SID>",str(sid+2)).replace("<DID>",str(sid+4))+'" &')
                                        elif(v["name"]=="simple_forward"):
                                            os.system('docker exec mn.dc1_'+sys.argv[2]+'-'+vnf["member-vnf-index"]+'-'+v["name"]+'-1 sh -c "'+cmd.replace("<SID>",str(sid+3)).replace("<DID>",str(sid+4))+'" &')
                                        elif(v["name"]=="speed_tester"):
                                            os.system('docker exec mn.dc1_'+sys.argv[2]+'-'+vnf["member-vnf-index"]+'-'+v["name"]+'-1 sh -c "'+cmd.replace("<SID>",str(sid+4)).replace("<DID>",str(sid+1))+'" &')
                                    elif(ns["name"]=="simple_2vnf_ns"):
                                        if(v["name"]=="simple_forward"):
                                            os.system('docker exec mn.dc1_'+sys.argv[2]+'-'+vnf["member-vnf-index"]+'-'+v["name"]+'-1 sh -c "'+cmd.replace("<SID>",str(sid+1)).replace("<DID>",str(sid+2))+'" &')
                                        elif(v["name"]=="speed_tester"):
                                            os.system('docker exec mn.dc1_'+sys.argv[2]+'-'+vnf["member-vnf-index"]+'-'+v["name"]+'-1 sh -c "'+cmd.replace("<SID>",str(sid+2)).replace("<DID>",str(sid+1))+'" &')
                                    time.sleep(5)
                                
            f = open("sid", "w")            
            f.write(str(sid+count))
            f.close()
            
    
proxypost()
    #return jsonify({"status":"OK"})
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True,port=5000)

"""
_ip="10.0.1.24"
token_request = requests.post('https://%s:9999/osm/admin/v1/tokens' % _ip,data={'username': 'admin', 'password': 'admin'}, verify=False)
token = yaml.safe_load(token_request.text)["id"]
#r = requests.get('https://10.0.1.24:9999/osm/vnfpkgm/v1/vnf_packages',headers ={'Authorization': 'Bearer %s' % token}, verify= False)
yaml_object=yaml.load("examples/vnfs/simple_forward_vnfd/simple_forward_vnfd.yaml")
json_out=json.dumps(yaml_object)
r = requests.post('https://10.0.1.24:9999/osm/vnfpkgm/v1/vnf_packages' ,data = json_out,headers ={'Authorization': 'Bearer %s' % token,'Content-Type':  'application/json','Accept':  'application/json'}, verify= False)
#vnfds=(yaml.safe_load(r.text))
#for v in vnfds:
#    print(v["vdu"][0]["vdu-configuration"]["initial-config-primitive"][0]["parameter"][0]["value"])
"""