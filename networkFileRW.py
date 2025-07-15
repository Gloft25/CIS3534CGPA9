#!/usr/bin/env python3
#GPA 8: Working With Files_GavinLoftus.py
#Gavin Loftus
#CIS3534C - Scripting for Network Professionals
#Update routers and switches;
#read equipment from a file, write updates & errors to file


try:
    import json
except ImportError:
    print("JSON module not found. Please ensure json is installed.")
    exit(1)

# File constants
EQUIP_R_FILE = "equip_r.txt"
EQUIP_S_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERRORS_FILE = "invalid.txt"

#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets)
        for byte in octets:
            try:
                byte = int(byte)
                if byte < 0 or byte > 255:
                    invalidIPCount += 1
                    invalidIPAddresses.append(ipAddress)
                    print(SORRY)
                    break
            except ValueError:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount
        
def main():
    # Open and read equipment files
    try:
        with open(EQUIP_R_FILE, 'r') as file:
            routers = json.load(file)
    except FileNotFoundError:
        print(f"Error: {EQUIP_R_FILE} not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: {EQUIP_R_FILE} contains invalid JSON.")
        exit(1)

    try:
        with open(EQUIP_S_FILE, 'r') as file:
            switches = json.load(file)
    except FileNotFoundError:
        print(f"Error: {EQUIP_S_FILE} not found.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: {EQUIP_S_FILE} contains invalid JSON.")
        exit(1)

    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function get valid IP address
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the updated dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    # Write updated equipment to file
    try:
        with open(UPDATED_FILE, 'w') as file:
            json.dump(updated, file, indent=4)
    except IOError:
        print(f"Error: Unable to write to {UPDATED_FILE}.")
        exit(1)
    
    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    # Write invalid addresses to file
    try:
        with open(ERRORS_FILE, 'w') as file:
            json.dump(invalidIPAddresses, file, indent=4)
    except IOError:
        print(f"Error: Unable to write to {ERRORS_FILE}.")
        exit(1)
    
    print("List of invalid addresses written to file 'invalid.txt'")

#top-level scope check
if __name__ == "__main__":
    main()

