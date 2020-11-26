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
            if(k=="policies"):
                tmp_action=v[0]["policy"]["actions"]["action_type"]
                tmp_data=v[0]["policy"]["actions"]["object"]

with open(sys.argv[1]) as f:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    tmp_doc = {}
    for doc in docs:        
        for k, v in doc.items():            
            if(k!="policies"):
                if(k=="resources"):
                    v["vfw_0"]["properties"]["user_data"]["str_replace"]["template"]=v["vfw_0"]["properties"]["user_data"]["str_replace"]["template"]+"\n./update_firewall.sh "+tmp_action+" __"+tmp_data+"__"
                tmp=v
                tmp_doc[k]=tmp
    with open(sys.argv[2], 'w') as file:
        yaml.dump(tmp_doc, file)