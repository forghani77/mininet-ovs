#!/usr/bin/env python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import Node
from mininet.link import Link
from mininet.log import  setLogLevel, info
from mininet.link import TCLink, Intf

def myNetwork():
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', inNamespace=False)
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', ip='10.0.0.3', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    '''
        s1-eth1<->h1-eth0
        s1-eth2<->h2-eth0
        s1-eth3<->h3-eth0
    '''
    '''
        The goal of this network is to make a biodirectional flow between h1 and h2.
        The flow is based upon MAC address.
        Any trafic from/to h3 will be ignored.

    '''

    info( '*** Starting network\n')
    net.start()
    info( '*** Obtaining MAC addresses...\n')
    h1_mac = str.rstrip(h1.cmd("ip -a link | grep ether | awk '{print $2}'"))
    h2_mac = str.rstrip(h2.cmd("ip -a link | grep ether | awk '{print $2}'"))
    h3_mac = str.rstrip(h3.cmd("ip -a link | grep ether | awk '{print $2}'"))
    info('*** Done!\n')
    info( '*** Post configure switches and hosts\n')
    info('*** Adding OpenFlow rules to switches...\n')
    s1.cmdPrint( 'ovs-ofctl add-flow s1 dl_src=%s,dl_dst=%s,actions=output:2'%(h1_mac,h2_mac) )

    s1.cmdPrint( 'ovs-ofctl add-flow s1 dl_src=%s,dl_dst=%s,actions=output:1'%(h2_mac,h1_mac) )

    s1.cmdPrint( 'ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,actions=flood')
    info('*** Done!\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

