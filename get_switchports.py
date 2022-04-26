# OBJECTIVE: Given a list of MAC addresses and a list of switches,
# create a CSV associating each MAC address with a particlar switchport.

# PREREQUISITES:
#   1. Module: paramiko
#   2. Text file list: switches.txt
#   3. Text file list: macs.txt

import paramiko
import csv

# Import the switch and MAC address lists and create the destination CSV.
switchlist = open('switches.txt').read().splitlines()
maclist = open('macs.txt').read().splitlines()
macswitchlist = open('camera-switchports.csv', mode='w')

# Set string variables.
sw_username = input("Enter your switch username: ")
sw_password = input("Enter your switch password: ")

# Set method variables.
ssh = paramiko.SSHClient()
csv_writer = csv.writer(macswitchlist, delimiter=',')

# Load system SSH host keys and add keys automatically if needed.
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# For each switch in the switch list...
for switch in switchlist:

    # ...check the MAC address table for each MAC in the MAC list.
    for mac_add in maclist:
        ssh.connect(switch,
                    username=sw_username,
                    password=sw_password,
                    look_for_keys=False)

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f"show mac address-table address {mac_add}")
        mac_output = ssh_stdout.readlines()
        ssh.close()

        try:
            # If the MAC address table command out put indicates a 10G switchport,
            # stop the loop. This is required because of the rstrip issue
            # noted in the chassis strip code block.
            for line in mac_output:
                if 'Te' in line:
                    raise StopIteration

                # FOR ACCESS SWITCHES:
                # Parse the MAC address table command output and put each
                # corresponding switchport into a variable.
                if 'DYNAMIC' in line:
                    try:
                        switchport = line[38:46].rstrip()

                        # Check to see if each switchport is a trunk. If it is,
                        # stop the loop.
                        ssh.connect(switch,
                            username=sw_username,
                            password=sw_password,
                            look_for_keys=False)

                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f"show interface {switchport} status")
                        intstatus_output = ssh_stdout.readlines()
                        ssh.close()

                        for line in intstatus_output:
                            if 'trunk' in line:
                                raise StopIteration

                        # Write the non-trunk switchports to the CSV.
                        print("Finding camera in switch",switch)
                        csv_writer.writerow([switch,switchport,mac_add])

                    except StopIteration: pass

                # FOR CHASSIS SWITCHES:
                # Parse the MAC address table command output and put each
                # corresponding switchport into a variable.
                if 'dynamic' in line:
                    try:
                        switchport = line[57:76].rstrip()
                        # ^^ These rstrip parameters do not work for 10G switchports
                        # on chassis switches, which causes the next code block to fail.
                        # That is why we reject 10G switchports in lines 47-49.

                        # Check to see if each switchport is a trunk. If it is,
                        # stop the loop.
                        ssh.connect(switch,
                            username=sw_username,
                            password=sw_password,
                            look_for_keys=False)

                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(f"show interface {switchport} status")
                        intstatus_output = ssh_stdout.readlines()
                        ssh.close()

                        for line in intstatus_output:
                            if 'trunk' in line:
                                raise StopIteration

                        # Write the non-trunk switchports to the CSV.
                        print("Finding camera in switch",switch)
                        csv_writer.writerow([switch,switchport,mac_add])

                    except StopIteration: pass
        except StopIteration: pass
