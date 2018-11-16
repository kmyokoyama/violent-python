#!/usr/bin/env python

import argparse
import sys

import nmap


def find_smb_targets(subnet):
    SMB_PORT = 445

    nmscan = nmap.PortScanner()
    nmscan.scan(subnet, f"{SMB_PORT}")

    target_hosts = []
    for host in nmscan.all_hosts():
        if nmscan[host].has_tcp(SMB_PORT):
            state = nmscan[host]['tcp'][SMB_PORT]['state']
            if state == "open":
                print(f"[+] Found target host: {host}:{SMB_PORT}.")

                target_hosts.append(host)

    return target_hosts


def main():
    parser = argparse.ArgumentParser(description="Simple nmap parser for port 445 (SMB)")
    parser.add_argument("-s", dest="subnet", type=str, help="Specify target subnet")

    args = parser.parse_args()
    subnet = args.subnet

    if not subnet:
        print(f"[-] Subnet must be provided")
        parser.print_help()
        return 1

    print(f"[*] Searching for hosts with SMB port open...")
    hosts = find_smb_targets(subnet)

    print(f"[*] Done.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
