export LC_ALL=C.UTF-8
export LANG=C.UTF-8
echo ">>>> ONBOARD VNFD examples/vnfs/speed_tester_vnfd/speed_tester_vnfd.yaml"
osm vnfd-create examples/vnfs/speed_tester_vnfd/speed_tester_vnfd.yaml 
echo ">>>> ONBOARD VNFD examples/vnfs/simple_forward_vnfd/simpleforwarder_vnfd.yaml"
osm vnfd-create examples/vnfs/simple_forward_vnfd/simpleforwarder_vnfd.yaml
echo ">>>> ONBOARD VNFD examples/vnfs/flow_forwarder_vnfd/flow_forwarder_vnfd.yaml"
osm vnfd-create examples/vnfs/flow_forwarder_vnfd/flow_forwarder_vnfd.yaml
echo ">>>> ONBOARD VNFD examples/vnfs/firewall_vnfd/firewall_vnfd.yaml " 
osm vnfd-create examples/vnfs/firewall_vnfd/firewall_vnfd.yaml 
echo ">>>> ONBOARD NSD examples/services/2flows_nsd/2flows_nsd.yaml "
osm nsd-create examples/services/2flows_nsd/2flows_nsd.yaml 
echo ">>>> ONBOARD NSD examples/services/2flows_nsd/simple_2vnf_nsd.yaml "
osm nsd-create examples/services/2flows_nsd/simple_2vnf_nsd.yaml 
#docker run --name vim-emu -it -d --rm --privileged --pid='host' --network=netosm --volume=/var/run:/var/run --volume=/dev/hugepages/:/dev/hugepages/ --volume=/home/long/openNetVM:/home/long/openNetVM -v /home/long/vim-emu:/vim-emu -v /var/run/docker.sock:/var/run/docker.sock vim-emu-img python3 /vim-emu/examples/openstack_single_dc.py
#sleep 30
#export VIMEMU_HOSTNAME=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' vim-emu)
#osm vim-create --name emu-vim1 --user username --password password --auth_url http://$VIMEMU_HOSTNAME:6001/v2.0 --tenant tenantName --account_type openstack
#sleep 30
#osm ns-create --nsd_name 2flows_ns --ns_name 2flows_nsi --vim_account emu-vim1
#osm ns-create --nsd_name simple_2vnf_ns --ns_name simple_2vnf_nsi --vim_account emu-vim1
#sleep 60
#python3 start_nf.py