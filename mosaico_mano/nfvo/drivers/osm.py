import sys
import os
import copy
import time
import subprocess
import yaml
import docker
client = docker.from_env()
class OSM(object):

    def __init__(self,vim_driver):
        self.vim = vim_driver

    def deploy_vim(self):      
        try:
            if(client.containers.get(self.vim).status=="exited") :
                p1=subprocess.run(["docker", "start", self.vim], stdout=subprocess.PIPE)            
        except:                                
            p1=subprocess.run(["docker", "run", "--name", self.vim, "-t", "-d", "--rm", "--privileged", "--pid=host", "--network=netosm", "-v", "/var/run/docker.sock:/var/run/docker.sock", "vim-emu-img", "python3","vim/drivers/"+self.vim+"/examples/openstack_single_dc.py"], stdout=subprocess.PIPE)        
        ip_vim=client.containers.get(self.vim).attrs['NetworkSettings']['Networks']['netosm']['IPAMConfig']['IPv4Address']
        print("VIM IP: "+ip_vim)
        p3=subprocess.run(["osm", "vim-create", "--name", "emu-vim1", "--user", "username", "--password", "password", "--auth_url", "http://"+ip_vim+":6001/v2.0", "--tenant", "tenantName", "--account_type", "openstack"], stdout=subprocess.PIPE)


    def onboard_ns(self, nsd):
        subprocess.run(['osm', 'nsd-create',nsd], stdout=subprocess.PIPE)

    def onboard_vnf(self, vnfd):
        subprocess.run(['osm', 'vnfd-create',vnfd], stdout=subprocess.PIPE)

    def deploy_ns_instance(self,ns):
        cmd=['osm', 'ns-create']
        for key,value in ns.items():
            cmd.append("--"+key)
            cmd.append(value)
        subprocess.run(cmd, stdout=subprocess.PIPE)

    def setup_policies(self, tosca_policies):
        pass

    def get_vnf_from_id(self, id):
        return

    def list_vnfd(self):
        result = subprocess.run(['osm', 'vnfd-list'], stdout=subprocess.PIPE)
        output=str(result.stdout.decode('ascii')).split('\n')
        return output

    def list_nsd(self):
        result = subprocess.run(['osm', 'nsd-list'], stdout=subprocess.PIPE)
        output=str(result.stdout.decode('ascii')).split('\n')
        return output
    
    def list_ns(self):
        result = subprocess.run(['osm', 'ns-list'], stdout=subprocess.PIPE)
        output=str(result.stdout.decode('ascii')).split('\n')
        return output

    def deploy_security_ns(self,path):
        with open(path) as f:
            #TOSCA PARSER & SYSTEM MODEL
            sys_model = yaml.load_all(f, Loader=yaml.FullLoader)
            #print(sys_model)
            for doc in sys_model:
                #print(doc)
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
                            print(">>> NFVO <<< Deploy NS: "+ ns["ns_name"])                            
                            self.deploy_ns_instance(ns)
