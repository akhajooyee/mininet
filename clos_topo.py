#!/usr/bin/python
import mininet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

import argparse
import sys
import time


class ClosTopo(Topo):
    def __init__(self, fanout, cores, **opts):
        # Initialize topology and default options
        f = fanout
        c = cores
        aggrNum = c ** f
        edgeNum = aggrNum * fanout
        hostNum = edgeNum * fanout
        Topo.__init__(self, **opts)

        # "Set up Core and Aggregate level, Connection Core - Aggregation level"
        # WRITE YOUR CODE HERE!
        cors = []
        i = 0
        while i < c:
            cores.append(self.addSwitch('c' + str(i)))
            i += 1

        i = 0
        aggrs = []
        while i < aggrNum:
            aggrs.append(self.addSwitch('aggr' + str(i)))
            for core in cors:
                self.addLink(aggrs[i] , core)
            i += 1



        pass

        # "Set up Edge level, Connection Aggregation - Edge level "
        i = 0
        edges = []
        while i < edgeNum:
            edges.append(self.addSwitch('edge' + str(i)))
            for aggr in aggrs:
                self.addLink(edges[i] , aggr)
            i += 1

        # WRITE YOUR CODE HERE!
        pass

        # "Set up Host level, Connection Edge - Host level "
        i = 0
        temp = 0
        hosts = []
        while i < edgeNum:
            fanTemp = 0
            while fanTemp < f:
                hosts.append(self.addHost('h' + str(temp)))
                self.addLink(hosts[temp] , edges[i])
                fanTemp += 1
                temp += 1
            i += 1
        # WRITE YOUR CODE HERE!
        pass


def setup_clos_topo(fanout=2, cores=1):
    "Create and test a simple clos network"
    assert (fanout > 0)
    assert (cores > 0)
    topo = ClosTopo(fanout, cores)
    net = Mininet(topo=topo, controller=lambda name: RemoteController('c0', "127.0.0.1"), autoSetMacs=True, link=TCLink)
    net.start()
    time.sleep(20)  # wait 20 sec for routing to converge
    net.pingAll()  # test all to all ping and learn the ARP info over this process
    CLI(net)  # invoke the mininet CLI to test your own commands
    net.stop()  # stop the emulation (in practice Ctrl-C from the CLI
    # and then sudo mn -c will be performed by programmer)


def main(argv):
    parser = argparse.ArgumentParser(description="Parse input information for mininet Clos network")
    parser.add_argument('--num_of_core_switches', '-c', dest='cores', type=int, help='number of core switches')
    parser.add_argument('--fanout', '-f', dest='fanout', type=int, help='network fanout')
    args = parser.parse_args(argv)
    setLogLevel('info')
    setup_clos_topo(args.fanout, args.cores)


if __name__ == '__main__':
    main(sys.argv[1:])
