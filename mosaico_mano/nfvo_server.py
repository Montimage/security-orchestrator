import subprocess
import requests
import json
import time
import sys
import yaml
from nfvo.orchestrator import Orchestrator
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin

nfvo=Orchestrator("osm","vim-emu",None)

app = Flask(__name__)
CORS(app)
@app.route('/api/deploy', methods=['POST'])
def post_api_deploy():
    data=request.json        
    nfvo.deploy_security_ns(data["tosca"])
    return {"status":"ok"}

@app.route('/api/alert', methods=['POST'])
def post_api_alert():
    data=request.json        
    condition_json={}
    if(data["alert"]=="ddos"):    
        condition_json["metric"]="alert_ddos"
        condition_json["value"]=1
    condition_json["triggred_by"]=data["trigger"]
    print(nfvo.policies)
    print(condition_json)
    for policy in nfvo.policies:
        if(policy.isPolicyTriggered(condition_json)):
            policy.triggerPolicy()
    return {"status":"ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600,debug=True)
