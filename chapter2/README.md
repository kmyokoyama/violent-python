# Chapter 2

## Scripts

### `scanner.py`:

**Description** : Simple network scanner using TCP.

**Usage** :

```
$ python scanner.py -H <target_host> -P <target_port>
```

* `target_host`: IP address of the target.
* `target_port`: port of the target to be scanned.

### `scanner_nmap.py`:

**Description** : Simple network scanner using Nmap.

**Usage** :

```
$ python scanner_nmap.py -H <target_host> -P <target_port>
```

* `target_host`: IP address of the target.
* `target_port`: port of the target to be scanned.

### `ssh_pxssh.py`:

**Description** : Brute force SSH passwords.

**Usage** :

```
$ python ssh_pxssh.py -u <user> -H <target_host> -P <target_port> -f <password_file>
```

* `user`: SSH user to brute force password.
* `target_host`: IP address of the target.
* `target_port`: port of the target.
* `password_file`: passwords file.

### `ssh_botnet.py`:

**Description** : SSH botnet.

**Usage** :

```
$ python ssh_botnet.py -u <user> -p <password> -H <target_host> -P <target_port>
```

* `user`: SSH user.
* `password`: SSH user's password.
* `target_host`: IP address of the target.
* `target_port`: port of the target.

### `ftp_attack.py`:

**Description** : Injection of code into web pages served by FTP servers.

**Usage** :

```
$ python ftp_attack.py -H <target_hosts> -f <passwd_file>
```

* `target_hosts`: IP address of the target(s).
* `passwd_file`: user/password file.

## Requirements

The following packages are also listed in `requirements.txt`:

* certifi
* chardet
* idna
* python-nmap
* requests
* urllib3
