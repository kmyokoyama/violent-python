#!/usr/bin/env python

import pexpect.pxssh as pxssh


class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)

            return s
        except Exception as err:
            print(err)
            print(f"[-] Error connecting")

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()

        return self.session.before


class Botnet:
    def __init__(self):
        self.bots = []

    def add_client(self, host, user, password):
        client = Client(host, user, password)
        self.bots.append(client)

    def send_command(command):
        for client in self.bots:
            output = client.send_command(command)
            print(f"[+] Output from {client.host}")
            print(f"[+] {output}")


def main():
    botnet = Botnet()

    # Read it from file?
    botnet.add_client("10.10.10.110", "root", "toor")
    botnet.add_client("10.10.10.120", "root", "toor")
    botnet.add_client("10.10.10.130", "root", "toor")

    botnet.command("uname -v")
    botnet.command("cat /etc/issue")
