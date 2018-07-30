#!/usr/bin/env python

import os
import requests
import tarfile
import urllib


def get_file(base_url, file):
    url = urllib.parse.urljoin(base_url, file)

    print(f"[*] Getting '{file}'. It may take a while...")

    r = requests.get(url)
    open(file, "wb").write(r.content)

    r.close()


def untar_file(file):
    print(f"[*] Extracting '{file}'.")

    tar = tarfile.open(file)
    tar.extractall()
    tar.close()


def main():
    keys_dir = "weak_keys"
    alg_sizes = ["dsa_1024", "rsa_2048"]
    base_url = "http://digitaloffense.net/tools/debian-openssl/"
    file = "debian_ssh_{}_x86.tar.bz2"

    files = [file.format(alg_size) for alg_size in alg_sizes]

    try:
        os.mkdir(keys_dir)
    except FileExistsError as e:
        pass

    os.chdir(keys_dir)

    for file in files:
        if not os.path.exists(file):
            get_file(base_url, file)
        else:
            print(f"[*] Skipping fetch of '{file}'.")

    for file in files:
        if os.path.exists(file):
            untar_file(file)

    print("[+] Done.")

if __name__ == '__main__':
    main()
