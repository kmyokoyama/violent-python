#!/usr/bin/env python

import argparse
import nmap

def nmap_scan(target_host, target_port):
    nm_scan = nmap.PortScanner()
    nm_scan.scan(target_host, target_port)

    state = nm_scan[target_host]['tcp'][int(target_port)]['state']

    print(f" [*] {target_host} tcp/{target_port} {state}")


def main():
    parser = argparse.ArgumentParser(description="simple network scanner using Nmap")
    parser.add_argument("-H", dest="target_host", type=str, help="specify target host")
    parser.add_argument("-p", dest="target_port", type=str, help="specify target port")

    args = parser.parse_args()

    target_host = args.target_host
    target_ports = str(args.target_port).split(",")

    for target_port in target_ports:
        nmap_scan(target_host, target_port)

    if (target_host is None or target_ports[0] is None):
        print(parser.usage)
        exit(0)


if __name__ == '__main__':
    main()
