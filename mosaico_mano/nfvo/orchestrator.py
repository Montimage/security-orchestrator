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
from nfvo.drivers.osm import OSM
from sdnc.drivers.onos import ONOS

class Orchestrator(object):

    def __init__(self,nfvo_driver,vim_driver,sdnc_driver):
        self.vim = vim_driver
        if(nfvo_driver=="osm"):
            self.nfvo = OSM()
        else:
            self.nfvo = None
        if(nfvo_driver=="onos"):
            self.sdnc=ONOS("http://192.168.0.16:8181/onos/v1/","Basic b25vczpyb2Nrcw==")
        else:
            self.sdnc = None
        self.deploy_vim()

    def deploy_vim(self):
        self.nfvo.deploy_vim()

    def onboard_ns(self, ns_path):
        self.nfvo.onboard_ns(ns_path)

    def onboard_vnf(self, vnf_path):
        self.nfvo.onboard_vnf(vnf_path)

    def create_vnf_instance(self, vnf_name):
        self.nfvo.create_vnf_instance(vnf_name)

    def deploy_ns_instance(self, ns_name):
        self.nfvo.deploy_ns_instance(ns_name)

    def setup_policies(self, tosca_policies):
        self.nfvo.setup_policies(tosca_policies)

    def get_vnf_from_id(self, id):
        return self.nfvo.get_vnf_from_id(id)
    
    def list_vnfd(self):
        return self.nfvo.list_vnfd(id)

    def list_nsd(self):
        return self.nfvo.list_nsd(id)

    def list_ns(self):
        return self.nfvo.list_ns(id)

    def deploy_security_ns(self,f):
        self.nfvo.deploy_security_ns(f)
