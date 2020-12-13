import requests
import json

class Policy(object):
    def __init__(self,policy_json,nfvo):
        self.policy=policy_json
        self.nfvo=nfvo

    def isTriggerPolicy(condition_json):
        return True

    def prepareActions(actions_json):
        #if(actions_json["action_type"]=="")
        return