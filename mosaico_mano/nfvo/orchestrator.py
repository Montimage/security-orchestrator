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

class Orchestrator(object):

    def __init__(self,nfvo_driver,vim_driver):
        self.vim = None
        if(nfvo_driver=="osm"):
            self.nfvo = OSM()

    def deploy_vim(self):
        self.nfvo.deploy_vim()

    def onboard_ns(self, ns_path):
        self.nfvo.onboard_ns(ns_path)

    def onboard_vnf(self, vnf_path):
        self.nfvo.onboard_vnf(vnf_path)

    def create_vnf_instance(self, vnf_name):
        self.nfvo.create_vnf_instance(vnf_name)

    def create_ns_instance(self, ns_name):
        self.nfvo.create_ns_instance(ns_name)

    def setup_policies(self, tosca_policies):
        self.nfvo.setup_policies(tosca_policies)

    def get_vnf_from_id(self, id):
        self.nfvo.get_vnf_from_id(id)

    def deploy_security_network(self,f):
        self.nfvo.deploy_security_network(f)
