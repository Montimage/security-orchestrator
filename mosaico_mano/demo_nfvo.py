import subprocess
import requests
import json
import time
import sys
import yaml

with open(sys.argv[1]) as f:
    
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
                        cmd.append(value)
                    print(">>> NFVO <<< Deploy NS: "+ ns["ns_name"])
                    result = subprocess.run(cmd, stdout=subprocess.PIPE)
