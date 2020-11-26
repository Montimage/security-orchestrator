docker exec mn.dc1_test-1-flow_forward-1 sh -c "cd examples/flow_forward/ ; ./go.sh 1 -d 2" &
docker exec mn.dc1_test-2-firewall-1 sh -c "cd examples/firewall/ ; ./go.sh 2 -d 4 -f rules.json" &
docker exec mn.dc1_test-3-simple_forward-1 sh -c "cd examples/simple_forward/ ; ./go.sh 3 -d 4" &
docker exec mn.dc1_test-4-speed_tester-1 sh -c "cd examples/speed_tester/ ; ./go.sh 4 -d 1 -o pcap/pktgen_traffic_sample.pcap -c 100" &