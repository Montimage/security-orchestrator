import yaml
import entity
import intent
import sys


f = open(sys.argv[1], "r")
lines=(f.readlines())
policies={"policies":[]}
for l in lines:
    result_intent=(intent.predict(l))
    entites=(entity.predict(l))
    result_entity={"target":"","event":"","trigger":"","object":""}
    for e in entites:
        result_entity[list(e.values())[0]]=list(e.keys())[0]
    policy={"targets":{}}
    policy["targets"]=result_entity["target"]    
    policy["triggers"]={"conditions":{}}
    policy["triggers"]["conditions"]={"event":result_entity["event"],"triggred_by":result_entity["trigger"]}
    policy["actions"]={"action_type":result_intent,"object":result_entity["object"]}
    policies["policies"].append({"policy":policy})
with open(sys.argv[2], 'w') as file:
    yaml.dump(policies, file)