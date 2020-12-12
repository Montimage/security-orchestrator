import sys
import os
import copy
import time
import subprocess
import requests
import json
import time
import sys
import yaml

class OSM(object):

    def __init__(self):
        self.vim = None
        self.vnfm = None

    def deploy_vim(self):
        pass

    def onboard_ns(self, ns_path):
        subprocess.run(['osm', 'nsd-create',ns_path], stdout=subprocess.PIPE)

    def onboard_vnf(self, vnfd):
        subprocess.run(['osm', 'vnfd-create',vnfd], stdout=subprocess.PIPE)

    def create_vnf_instance(self, graph, vnf_name):
        pass

    def create_ns_instance(self):
        pass

    def setup_policies(self, tosca_policies):
        pass

    def get_vnf_from_id(self, id):
        pass

    def deploy_security_network(self,path):
        with open(path) as f:
            docs = yaml.load_all(f, Loader=yaml.FullLoader)
            print(docs)
            for doc in docs:
                print(doc)
                for k, v in doc.items():
                    if(k=="vnfd"):
                        for vnfd in v:
                            print(">>> NFVO <<< Onboarding VNFD: "+ vnfd)
                            self.onboard_vnf(vnfd)
                    elif(k=="nsd"):
                        for nsd in v:
                            print(">>> NFVO <<< Onboarding NSD: "+ nsd)
                            self.onboard_ns(nsd)
                    elif(k=="ns"):
                        for ns in v:
                            cmd=['osm', 'ns-create']
                            for key,value in ns.items():
                                cmd.append("--"+key)
                                cmd.append(value)
                            print(">>> NFVO <<< Deploy NS: "+ ns["ns_name"])
                            result = subprocess.run(cmd, stdout=subprocess.PIPE)
