sent="if alice is detected as a trojan, in firewall, allow only user"
object='user'
trigger='alice'
target='firewall'
event='trojan'

print(",('"+sent+"', {")
print("\t'entities': [("+str(sent.index(object))+", "+str(sent.index(object)+len(object))+", 'object'), ("+str(sent.index(trigger))+", "+str(sent.index(trigger)+len(trigger))+", 'trigger'), ("+str(sent.index(target))+", "+str(sent.index(target)+len(target))+", 'target'), ("+str(sent.index(event))+", "+str(sent.index(event)+len(event))+", 'event')]")
print("})")