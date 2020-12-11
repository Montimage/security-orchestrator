export LC_ALL=C.UTF-8
export LANG=C.UTF-8
osm ns-create --nsd_name $1 --ns_name $2 --vim_account emu-vim1
#osm ns-create --nsd_name simple_2vnf_ns --ns_name simple_2vnf_nsi --vim_account emu-vim1
#sleep 60
#python3 start_nf.py $1 $2
sudo docker exec -it montimage-mano sh -c "python3 testro.py $1 $2"