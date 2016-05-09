MKBRUTUS
========

Password bruteforcer for MikroTik devices and boxes running RouterOS.

Project Website: http://mkbrutusproject.github.io/MKBRUTUS/

## Summary

Some boxes running MikroTik RouterOS (3.x or newer) have API port enabled for administrative purposes (by default at port 8728/TCP) instead or alongside SSH, Winbox or HTTPS. This is an attack vector as it could be possible to perform a bruteforce to obtain valid credentials if access to this port is not restricted. The API uses a specific proprietary protocol so some code published by the vendor is included.

## Dependencies

    sudo pip install -r requirements.txt

If you don't have pip, find it here: http://pypi.python.org/pypi/pip

## Disclaimer

This tool is intended only for testing MikroTik devices security during ethical pentests or audit processes.
The authors are not responsible for any damage caused by the use of this tool.

## Credits

Authors:
Ramiro Caire (@rcaire) ramiro.caire@gmail.com
Federico Massa (@fgmassa) fmassa@vanguardsec.com

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.
