#!/usr/bin/env python


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import Intf


def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    info( '*** Add hosts\n' )
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')
    info( '*** Add links\n' )
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s1, s2)
    '''
        s1-eth1<->h1-eth0
        s1-eth2<->h2-eth0
        s2-eth1<->h3-eth0
        s2-eth2<->h4-eth0
        s1-eth3<->s2-eth3
    '''

    '''
        In this senario we would want to have two vlans :
        h1 and h3: vlan 100
        h2 and h4: vlan 200
        We have to write these flows for s1 and s2 switches :
        Any traffic from h1 to h3 must be tagged with id of 100
        Any traffic from h2 to h4 must be tagged with id of 200

    '''
    info( '*** Starting network\n')
    net.start()
    info( '*** Obtaining MAC addresses...\n' )

    h1_mac = str.rstrip(h1.cmd("ip -a link | grep ether | awk '{print $2}'"))
    h2_mac = str.rstrip(h2.cmd("ip -a link | grep ether | awk '{print $2}'"))
    h3_mac = str.rstrip(h3.cmd("ip -a link | grep ether | awk '{print $2}'"))
    h4_mac = str.rstrip(h4.cmd("ip -a link | grep ether | awk '{print $2}'"))
    info('*** Done!\n')


    info( '*** Post configure switches and hosts\n' )

    info('*** Seting vlan id 100 for h1,h2 and 200 for h3,h4\n')
    info('*** Adding OpenFlow rules for switches...\n')
    '''
    s1 open flow port list:
        h1 : ofport 1
        h3 : ofport 2
        s2 : ofport 3
    '''
    s1.cmdPrint('ovs-ofctl add-flow s1 dl_src=%s,dl_vlan=0xffff,actions=mod_vlan_vid:100,output:3'%h1_mac)
    s1.cmdPrint('ovs-ofctl add-flow s1 dl_src=%s,dl_vlan=0xffff,actions=mod_vlan_vid:200,output:3'%h2_mac)
    s1.cmdPrint('ovs-ofctl add-flow s1 in_port=3,dl_vlan=100,actions=strip_vlan,output:1')
    s1.cmdPrint('ovs-ofctl add-flow s1 in_port=3,dl_vlan=200,actions=strip_vlan,output:2')


    '''
    s2 open flow port list:
        h2 : ofport 1
        h4 : ofport 2
        s2 : ofport 3
    '''
    s2.cmdPrint('ovs-ofctl add-flow s2 dl_src=%s,dl_vlan=0xffff,actions=mod_vlan_vid:100,output:3'%h3_mac)
    s2.cmdPrint('ovs-ofctl add-flow s2 dl_src=%s,dl_vlan=0xffff,actions=mod_vlan_vid:200,output:3'%h4_mac)
    s2.cmdPrint('ovs-ofctl add-flow s2 in_port=3,dl_vlan=100,actions=strip_vlan,output:1')
    s2.cmdPrint('ovs-ofctl add-flow s2 in_port=3,dl_vlan=200,actions=strip_vlan,output:2')
    info('*** Done!\n')

    CLI(net)


    '''
    Clean mininet
    '''
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
