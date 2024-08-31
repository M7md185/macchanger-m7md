import subprocess
import optparse
import re

# This is a reader that will take network interface and mac address
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="network_interface", help="Specify the network interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="Specify the new MAC address")
    options, arguments = parser.parse_args()

    if not options.network_interface:
        parser.error("[-] Specify Network Interface. type -h for help")
        exit(1)

    if not options.new_mac:
        parser.error("[-] Please specify a new MAC address.type -h for help")
        exit(1)

    return options

# This is a system command that will change the mac address for a network interface
def mac_changer(network_interface, new_mac):
    subprocess.call(f"ifconfig {network_interface} down", shell=True)
    subprocess.call(f"ifconfig {network_interface} hw ether {new_mac}", shell=True)
    subprocess.call(f"ifconfig {network_interface} up", shell=True)
    print(f"[+] Changing MAC Address for {network_interface} to {new_mac}")

# Filter mac address
def get_mac(network_interface):
    ifconfig_result = subprocess.check_output(f"ifconfig {network_interface}", shell=True).decode("UTF-8")
    mac_address = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result)
    if mac_address:
        return mac_address.group(0)
    else:
        return None

options = get_arguments()
mac_changer(options.network_interface, options.new_mac)
mac_address = get_mac(options.network_interface)

if mac_address and mac_address == options.new_mac:
    print("[+] MAC address has changed successfully")
else:
    print("[-] Something went wrong....")
