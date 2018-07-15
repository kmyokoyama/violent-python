#!/usr/bin/env python

import optparse
import nmap

def nmap_scan(target_host, target_port):
    nm_scan = nmap.PortScanner()
    nm_scan.scan(target_host, target_port)

    state = nm_scan[target_host]['tcp'][int(target_port)]['state']

    print(f" [*] {target_host} tcp/{target_port} {state}")


def main():
    parser = optparse.OptionParser("usage: %prog -H <target_host> -p <target_port>")
    parser.add_option("-H", dest="target_host", type="string", help="specify target host")
    parser.add_option("-p", dest="target_port", type="string", help="specify target port")

    options, args = parser.parse_args()

    target_host = options.target_host
    target_ports = str(options.target_port).split(",")

    for target_port in target_ports:
        nmap_scan(target_host, target_port)

    if (target_host is None or target_ports[0] is None):
        print(parser.usage)
        exit(0)


if __name__ == '__main__':
    main()
