#!/usr/bin/env python3.6

import optparse
import socket
import threading


screen_lock = threading.Semaphore(value=1)


def conn_scan(target_host, target_port):
    try:
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((target_host, target_port))
        conn_socket.send("Violent Python\r\n")
        results = conn_socket.recv(100)

        screen_lock.acquire()
        print(f"[+]{target_port}/tcp open")
        print(f"[+] ")
        print(str(results))

        conn_socket.close()
    except:
        print(f"[-]{target_port}/tcp closed")
    finally:
        screen_lock.release()
        conn_socket.close()

def port_scan(target_host, target_ports):
    try:
        target_ip = socket.gethostbyname(target_host)
    except:
        print(f"[-] Cannot resolve '{target_host}'")
        return

    try:
        target_name = socket.gethostbyaddr(target_ip)
        print(f"\n[+] Scan results for: {target_name[0]}")
    except:
        print(f"\n[+] Scan results for: {target_ip[0]}")

    socket.setdefaulttimeout(1)
    for target_port in target_ports:
        t = threading.Thread(target=conn_scan, args=(target_host, int(target_port)))
        t.start()


def main():
    parser = optparse.OptionParser("usage: %prog -H <target_host> -p <target_port>")
    parser.add_option("-H", dest="target_host", type="string", help="specify target host")
    parser.add_option("-p", dest="target_port", type="string", help="specify target port")

    options, args = parser.parse_args()

    target_host = options.target_host
    target_ports = str(options.target_port).split(",")

    port_scan(target_host, target_ports)

    if (target_host is None or target_ports[0] is None):
        print(parser.usage)
        exit(0)


if __name__ == '__main__':
    main()
