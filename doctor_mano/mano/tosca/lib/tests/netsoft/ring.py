n=16
durationFile='./'+str(n)+'_ring.yaml';

with open(durationFile, 'w') as the_file:
    the_file.write('imports:\n');
    the_file.write('  - data.yaml\n');
    the_file.write('  - doctor_nodes.yaml\n');
    the_file.write('tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0\n');
    the_file.write('description: Template for deploying DOCTOR security use case.\n');
    the_file.write('metadata:\n');
    the_file.write('  template_name: security_policies_example\n');
    the_file.write('topology_template:\n');
    the_file.write('  node_templates:\n');

    the_file.write('\n');
    the_file.write('##########################################################################\n');
    the_file.write('# Virtual Network Functions\n');
    the_file.write('##########################################################################\n');
    the_file.write('\n');

    for i in xrange(1,n+1):
        the_file.write('    router_'+str(i)+':\n');
        the_file.write('      type: tosca.nodes.nfv.doctor.VNF\n');
        the_file.write('      properties:\n');
        the_file.write('        id: '+str(i)+'\n');
        the_file.write('        vendor: orange\n');
        the_file.write('        version: 1.0\n');
        the_file.write('      requirements:\n');
        the_file.write('        - VDU: VDU'+str(i)+'\n');
    
    the_file.write('\n');
    the_file.write('##########################################################################\n');
    the_file.write('# Virtual Network Functions\n');
    the_file.write('##########################################################################\n');
    the_file.write('\n');

    for i in xrange(1,n+1):
        the_file.write('    VDU'+str(i)+':\n');
        the_file.write('      type: tosca.nodes.nfv.doctor.VDU\n');
        the_file.write('      properties:\n');
        the_file.write('        name: VDU'+str(i)+'\n');
        the_file.write('        sw_image: maouadj/ndn_router:v2\n');
        the_file.write('        config: /doctor/launch_nfd_router.sh\n');
        the_file.write('        flavor: medium\n');
        if (i<=round(n/3)):
            the_file.write('        placement_policy: [\'popLocation==uk\']\n');
        elif (i<=round(n/3)*2):
            the_file.write('        placement_policy: [\'popLocation==germany\']\n');
        else:
            the_file.write('        placement_policy: [\'popLocation==netherlands\']\n');

    the_file.write('\n');
    the_file.write('##########################################################################\n');
    the_file.write('# Virtual Network Functions\n');
    the_file.write('##########################################################################\n');
    the_file.write('\n');
    
    for i in xrange(1,n+1):
        j=i+1
        if i==n:
            j=1
        the_file.write('    VDU'+str(i)+'_VL'+str(i)+'_'+str(j)+'_CP:\n');
        the_file.write('      type: tosca.nodes.nfv.doctor.Cpd\n');
        the_file.write('      properties:\n');
        the_file.write('        name: VDU'+str(i)+'_VL'+str(i)+'_'+str(j)+'_CP\n');
        the_file.write('        layer_protocol: VXLAN\n');
        the_file.write('      requirements:\n');
        the_file.write('        - virtual_link: VL'+str(i)+'_'+str(j)+'\n');
        the_file.write('        - virtual_binding: VDU'+str(i)+'\n');
    
    the_file.write('\n');
    the_file.write('##########################################################################\n');
    the_file.write('# Virtual Network Functions\n');
    the_file.write('##########################################################################\n');
    the_file.write('\n');
    
    for i in xrange(1,n+1):
        j=i+1
        if i==n:
            j=1
        the_file.write('    VL'+str(i)+'_'+str(j)+':\n');
        the_file.write('      type: tosca.nodes.nfv.doctor.VnfVirtualLinkDesc\n');
        the_file.write('      properties:\n');
        the_file.write('        name: VL'+str(i)+'_'+str(j)+'\n');
        the_file.write('        connectivity_type: VXLAN\n');

netsoft_clean='../../../../../netsoft_clean_'+str(n);

"""with open(netsoft_clean, 'w') as clean_file:    
    clean_file.write('#!/bin/bash\n');
    clean_file.write('docker service rm vnfm\n');
    for i in xrange(1,n+1):
        clean_file.write('docker service rm VDU'+str(i)+'\n');
    clean_file.write('docker network rm admin_net\n');
    for i in xrange(1,n):
        for j in xrange(i+1,n+1):
            clean_file.write('docker network rm VL'+str(i)+'_'+str(j)+'\n');
"""