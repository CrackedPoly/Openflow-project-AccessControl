#!/usr/bin/env python
import os

from config import ODL_ip
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController


# avoid IP conflict
def convert_to_ip(n):
    return '10.0.' + str((int(n) + 1) // 256) + '.' + str((int(n) + 1) % 256)


# avoid MAC conflict
def convert_to_mac(n):
    return '12:34:56:78:' + '%02X' % ((int(n) + 1) // 256) + ':' + '%02X' % ((int(n) + 1) % 256)


def myNetwork():
    net = Mininet(topo=None, build=False, link=TCLink, controller=RemoteController)

    info('*** Adding controller\n')
    net.addController(ip=ODL_ip)

    info('*** Add switches\n')
    # s0 used for AC_server
    s0 = net.addSwitch('s0')
    s1 = net.addSwitch('s1', protocols="OpenFlow13")

    info('*** Add hosts\n')
    AC_server = net.addHost("AC_server", ip=convert_to_ip(0), mac=convert_to_mac(0))
    hosts = ["printer", "web_server", "Alice", "Bob", "Cindy", "David"]
    for idx in range(len(hosts)):
        net.addHost(hosts[idx], ip=convert_to_ip(idx+1), mac=convert_to_mac(idx+1))

    info('*** Add links\n')
    for host in hosts:
        net.addLink(host, s1)
    net.addLink(AC_server, s1)
    net.addLink(AC_server, s0)

    info('*** Starting network\n')
    net.start()
    os.system('ovs-ofctl del-flows s0')
    os.system('ovs-ofctl add-flow s0 actions=NORMAL')
    os.system('ovs-vsctl add-port s0 eth0')
    os.system('ifconfig eth0 0')
    os.system('dhclient s0')

    AC_server.cmdPrint('ifconfig AC_server-eth1 0')
    AC_server.cmdPrint('dhclient AC_server-eth1')
    AC_server.cmd('python3 server.py &')
    AC_server.cmd('iperf -s &')
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
