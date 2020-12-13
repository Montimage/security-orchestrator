import requests
import json

class Policy(object):
    def __init__(self,policy_json,nfvo,sdnc):
        self.policy=policy_json
        self.nfvo=nfvo
        self.sdnc=sdnc
    
    def isPolicyTriggered(condition_json):
        isTriggered=False
        if(self.policy['condition']["triggred_by"]==condition_json["triggred_by"] and self.policy['condition']["metric"]==condition_json["metric"] and self.policy['condition']["value"]==condition_json["value"]):
            isTriggered=True
        return isTriggered

    def triggerPolicy():        
        if(self.policy["target"]=="nfvo"):
            nfvoAction(self.policy['action'])
        elif(self.policy["target"]=="sdnc"):
            sdncAction(self.policy['action'])
        

    def nfvoAction():        
        if(self.policy['action']["type"]=="deploy_ns_instance"):
            self.nfvo.deploy_ns_instance(self.policy['action']["nsd_name"])                
        

    def sdncAction():
        if(self.policy['action']["type"]=="add_rule_sdnc"):            
            self.sdnc.add_rule(self.policy['action']["deviceId"],self.policy['action']["mac"],self.policy['action']["port"])
        