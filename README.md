Get Switchports
===============
And Find Out Where Your Stuff Is
--------------------------------

If you feed a list of MAC addresses and a list of switch hostnames/IP addresses into this script, it will output a CSV showing the switch and switchport associated with each MAC address. It only works with Cisco Catalyst switches, but with a few tweaks, it can be used in production.

How to use this script
----------------------

1. In the same directory as get_switchports.py, place your complete list of switch hostnames in a file called 'switches.txt'.
2. In the same directory as get_switchports.py, place your complete list of MAC addresses in a file called 'macs.txt'.
3. Execute get_switchports.py.

The script uses Paramiko, which is [notably and famously frustrating](https://github.com/paramiko/paramiko/issues/387) to use with SSH key exchange authentication. It therefore prompts for both a username and password.