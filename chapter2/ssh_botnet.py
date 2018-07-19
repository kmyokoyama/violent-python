#!/usr/bin/env python

import optparse
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

    conn_str = "ssh " + user + "@" + host + " -p " + port

    child = pexpect.spawn(conn_str)

    ret = child.expect([pexpect.TIMEOUT, ssh_conn_ref, ssh_newkey, "[P|p]assword:"])

    if ret == 0:
        print("[-] Error connecting: timeout")

        return None
    elif ret == 1:
        print(f"[-] Error connecting: \"{child.after.decode().strip()}\"")

        return None
    elif ret == 2:
        child.sendline("yes")
        ret = child.expect([pexpect.TIMEOUT, "[P|p]assword:"])
        if ret == 0:
            print("[-] Error connecting")

            return None
    elif ret == 3:
        child.sendline(password)
        child.expect(PROMPT)

        return child


def main():
    parser = optparse.OptionParser("usage: %prog -u <user> -h <host> -p <port>")

    parser.add_option("-u", dest="user", type="string", help="specify SSH user")
    parser.add_option("-p", dest="password", type="string", help="specify SSH password")
    parser.add_option("-H", dest="host", type="string", help="specify SSH host")
    parser.add_option("-P", dest="port", type="string", help="specify SSH port")

    options, ags = parser.parse_args()

    user = options.user
    password = options.password
    host = options.host
    port = options.port

    child = connect(user, password, host, port)
    send_command(child, "cat /etc/shadow | grep root")


if __name__ == '__main__':
    main()
