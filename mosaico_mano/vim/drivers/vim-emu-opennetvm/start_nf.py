import subprocess
import os
import time

isFailed=True
while(isFailed):
    result = subprocess.run(['docker','exec','mn.dc1_test-1-flow_forward-1','ps','-eaf'], stdout=subprocess.PIPE)
    output=str(result.stdout.decode('utf-8')).split('\n')
    #print(output)
    for o in output:
        if("openNetVM" in o):
            isFailed=False
            break
    if(isFailed):
        print(">>>> START OpenNetVM NF flow_forward")
        os.system('docker exec mn.dc1_test-1-flow_forward-1 sh -c "cd examples/flow_forward/ ; ./go.sh 1 -d 2" &')
        time.sleep(5)

isFailed=True

while(isFailed):
    result = subprocess.run(['docker','exec','mn.dc1_test-2-firewall-1','ps','-eaf'], stdout=subprocess.PIPE)
    output=str(result.stdout.decode('utf-8')).split('\n')
    #print(output)
    for o in output:
        if("openNetVM" in o):
            isFailed=False
            break
    if(isFailed):
        print(">>>> START OpenNetVM NF firewall")
        os.system('docker exec mn.dc1_test-2-firewall-1 sh -c "cd examples/firewall/ ; ./go.sh 2 -d 4 -f rules.json" &')
        time.sleep(5)

isFailed=True

while(isFailed):
    result = subprocess.run(['docker','exec','mn.dc1_test-3-simple_forward-1','ps','-eaf'], stdout=subprocess.PIPE)
    output=str(result.stdout.decode('utf-8')).split('\n')
    #print(output)
    for o in output:
        if("openNetVM" in o):
            isFailed=False
            break
    if(isFailed):
        print(">>>> START OpenNetVM NF simple_forward")
        os.system('docker exec mn.dc1_test-3-simple_forward-1 sh -c "cd examples/simple_forward/ ; ./go.sh 3 -d 4" &')
        time.sleep(5)

isFailed=True

while(isFailed):
    result = subprocess.run(['docker','exec','mn.dc1_test-4-speed_tester-1','ps','-eaf'], stdout=subprocess.PIPE)
    output=str(result.stdout.decode('utf-8')).split('\n')
    #print(output)
    for o in output:
        if("openNetVM" in o):
            isFailed=False
            break
    if(isFailed):
        print(">>>> START OpenNetVM NF speed_tester")
        os.system('docker exec mn.dc1_test-4-speed_tester-1 sh -c "cd examples/speed_tester/ ; ./go.sh 4 -d 1 -o pcap/pktgen_traffic_sample.pcap -c 100" &')
        time.sleep(5)

isFailed=True
