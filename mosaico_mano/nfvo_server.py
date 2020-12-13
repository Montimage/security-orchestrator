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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5600,debug=True)
