export LC_ALL=C.UTF-8
export LANG=C.UTF-8
osm ns-delete 2flows_nsi
osm ns-delete simple_2vnf_nsi
sleep 30
osm ns-delete 2flows_nsi --force
osm ns-delete simple_2vnf_nsi --force
sleep 30
osm nsd-delete 2flows_ns --force
osm nsd-delete simple_2vnf_ns --force
sleep 30
osm vnfd-delete speed_tester
osm vnfd-delete flow_forward
osm vnfd-delete simple_forward
osm vnfd-delete firewall
#osm vim-delete emu-vim1 --force
#sleep 30
#sudo docker stop vim-emu
#sudo docker rm vim-emu
#sleep 30