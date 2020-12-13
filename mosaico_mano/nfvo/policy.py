import requests
import json

class Policy(object):
    def __init__(self,policy_json,nfvo,sdnc):
        self.policy=policy_json
        self.nfvo=nfvo
        self.sdnc=sdnc
    
    def isPolicyTriggered(self,condition_json):
        isTriggered=False
        print(self.policy)
        if(self.policy['trigger']['condition']["triggred_by"]==condition_json["triggred_by"] and self.policy['trigger']['condition']["metric"]==condition_json["metric"] and self.policy['trigger']['condition']["value"]==condition_json["value"]):
            isTriggered=True
        return isTriggered

    def triggerPolicy(self):        
        if(self.policy["target"]=="nfvo"):
            self.nfvoAction()
        elif(self.policy["target"]=="sdnc"):
            self.sdncAction()
        

    def nfvoAction(self):        
        if(self.policy['action']["type"]=="deploy_ns_instance"):
            for ns in self.policy['action']["ns"]:
                self.nfvo.deploy_ns_instance(ns)
        

    def sdncAction(self):
        if(self.policy['action']["type"]=="add_rule_sdnc"):            
            self.sdnc.add_rule(self.policy['action']["deviceId"],self.policy['action']["mac"],self.policy['action']["port"])
        