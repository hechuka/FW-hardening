import netmiko
import getpass
import datetime
import Script_Test_Ongoing as script
import re

menu = True
useroutput = []
vdom_list = []
profile_list = []
zone_list = []
#useroutput = ""
# Getting the Password but without showing the password; Otherwise use input() for normal data request.
defaultStr = input('Default IP/Username? Type "y" for default values: ')

remoteHost = ""
userStr = ""
passStr = ""

catchvdom = [
    "config global",
    "diagnose sys vd list | grep name=",
]

catchprofile = [
    "config global",
    "config application list",
    "get"
]

def catchzone(i):
    catchzone = [
        "config vdom",
        f"edit {script.scriptvdom[i]}",
        "config system zone",
        "get"
    ]
    return catchzone

# Remote Host Details
if defaultStr.lower() == 'y':
    remoteHost = "10.10.101.2 "
    userStr = "nera"
    passStr = "3e4r5t^Y&U*I"
    script.username = userStr
else:
    remoteHost = input('IP of Remote Host: ')
    userStr = input('Username : ')
    passStr = getpass.getpass(prompt='FW Password: ')
    script.username = userStr


def connect_to_fortigate(host, username, password):
    device = {
        'device_type': 'fortinet',
        'host': host,
        'username': username,
        'password': password,
    }

    try:
        connection = netmiko.ConnectHandler(**device)
        return connection
    except netmiko.NetmikoTimeoutException as e:
        print(f"Timeout connecting to {host}: {e}")
    except netmiko.NetmikoAuthenticationException as e:
        print(f"Authentication failed for {host}: {e}")
    except Exception as e:
        print(f"Error connecting to {host}: {e}")

def execute_commands(connection, commands):
    """
    Executes multiple commands on the FortiGate firewall.

    Args:
        connection (netmiko.ConnectHandler): An SSH client object connected to the FortiGate.
        commands (list): A list of commands to execute.

    Returns:
        str: The output of the commands.
    """

    if isinstance(commands, str):
        commands = [commands]  # Convert single command to list
    output = connection.send_config_set(commands)

    return output

def vdom():
    global vdom_list
    host = remoteHost
    username = userStr
    password = passStr

    print(f'{"="*10} Trying to connect to Fortigate FW.... {"="*10}')

    connection = connect_to_fortigate(host, username, password)
    if connection:


        print(f'\nTime of Execution: {datetime.datetime.now()} SGT\n')
        print(f'{"="*10} Getting list of VDOM {"="*10}')
        output = execute_commands(connection, catchvdom)  
        connection.disconnect()
    
    # Use regular expression to extract the names
    pattern = r"name=([^/]+)"
    names = re.findall(pattern, output)
    #print(names)
    cleaned_names = []
    for name in names:
        cleaned_names.append(name.replace('\nname=', ''))
    vdom_list = [name for name in cleaned_names if not name.startswith('vsys')]   
    # Print the extracted cleaned names
    print("\n",vdom_list)
    print(f'\n{"="*10} Completed and Exiting {"="*10}')
    print(f'\nTime of Completion: {datetime.datetime.now()} SGT\n')
    script.scriptvdom = vdom_list

def profile():
    global profile_list
    host = remoteHost
    username = userStr
    password = passStr

    print(f'{"="*10} Trying to connect to Fortigate FW.... {"="*10}')

    connection = connect_to_fortigate(host, username, password)
    if connection:


        print(f'\nTime of Execution: {datetime.datetime.now()} SGT\n')
        print(f'{"="*10} Getting list of profile {"="*10}')
        output = execute_commands(connection, catchprofile)  
        connection.disconnect()
    
    # Use regular expression to extract the names
    pattern = r"== \[ (.*?) \]"
    names = re.findall(pattern, output)
    print(names)
    script.profile_name = names
    print(f'\n{"="*10} Completed and Exiting {"="*10}')
    print(f'\nTime of Completion: {datetime.datetime.now()} SGT\n')

def zone():
    global zone_list
    host = remoteHost
    username = userStr
    password = passStr
    print(f'{"="*10} Trying to connect to Fortigate FW.... {"="*10}')
    print(f'\nTime of Execution: {datetime.datetime.now()} SGT\n')
    for i in range(0, len(script.scriptvdom)):
        connection = connect_to_fortigate(host, username, password)
        if connection:           
            print(f'{"="*10} Getting list of zone from {script.scriptvdom[i]} {"="*10}')
            output = execute_commands(connection, catchzone(i))  
            connection.disconnect()
        
        # Use regular expression to extract the names
        pattern = r"== \[ (.*?) \]"
        names = re.findall(pattern, output)
        print(names)
        script.nested_list.append(names)
    print(f'\n{"="*10} Completed and Exiting {"="*10}')
    print(f'\nTime of Completion: {datetime.datetime.now()} SGT\n')
    print(script.nested_list)

def level():
    script.level = input("Please select Level 1 or 2 hardening(E.g. 1): ")

def dictionary(x):
    match x:
        case '1':
            return "network"             
        case '2':
            return "system"
        case '3':
            return "Policy_and_object"
        case '4':
            return "Security_profiles"
        case '5':
            return "Security_Fabric"
        case '6':
            return "VPN"
        case '7':
            return "Logs_and_reports"

def userchoice(x):
    global menu
    match x:
        case '1':
            return script.network()               
        case '2':
            return script.system()
        case '3':
            return script.Policy_and_object()
        case '4':
            return script.Security_profiles()
        case '5':
            return script.Security_Fabric()
        case '6':
            return script.VPN()
        case '7':
            return script.Logs_and_reports()
        case '0':
            menu = False
        case _:
            return "Please enter a number between 1 to 9"

def main():
    global useroutput, lst, outputlist
    outputlist = []
    level()
    vdom()
    profile()
    zone()
    while menu == True:
        try:
            if script.level == "1":
                user_choice = input("Please select which you would like to harden:\
                                    \n1. Network\
                                    \n2. System\
                                    \n3. Policy_and_object\
                                    \n4. Security_profiles\
                                    \n5. Security_Fabric\
                                    \n7. Logs_and_reports\
                                    \n8. All\
                                    \n9. Custom\
                                    \n0. Proceed with FW hardening\n"
                                    )
            else:
                user_choice = input("Please select which you would like to harden:\
                                    \n1. Network\
                                    \n2. System\
                                    \n3. Policy_and_object\
                                    \n4. Security_profiles\
                                    \n5. Security_Fabric\
                                    \n6. VPN\
                                    \n7. Logs_and_reports\
                                    \n8. All\
                                    \n9. Custom\
                                    \n0. Proceed with FW hardening\n"
                                    )
            
            if user_choice == "8":
                if script.level == "2":
                    if script.total == 7:
                        print("Everything has been hardened.")
                        continue               
                    for item in range(7):
                        try:
                            useroutput.append(userchoice(str(item + 1)))
                            if useroutput[-1] == None:
                                useroutput.pop()
                                print(f"{dictionary(str(item + 1))} hardened.")
                            else:
                                outputlist.append(str(item + 1))                                                          
                        except:
                            print(f"{dictionary(str(item + 1))} hardened.")
                    print(useroutput)
                elif script.level == "1":
                    if script.total == 6:
                        print("Everything has been hardened.")
                        continue               
                    for item in range(5):
                        try:
                            useroutput.append(userchoice(str(item + 1)))
                            if useroutput[-1] == None:
                                useroutput.pop()
                                print(f"{dictionary(item + 1)} hardened.")
                            else:
                                outputlist.append(str(item + 1))                            
                            outputlist.append(str(item + 1))                          
                        except:
                            print(f"{dictionary(str(item + 1))} hardened.")
                    try:
                        useroutput.append(userchoice("7"))
                        if useroutput[-1] == None:
                            useroutput.pop()
                            print(f"{dictionary("7")} hardened.")
                            break
                        else:
                            outputlist.append("7")                                               
                    except:
                        print(f"{dictionary("7")} hardened.")
                    print(useroutput)

            elif user_choice == "9":
                if script.level == "2":
                    if script.total == 7:
                        print("Everything has been hardened.")
                        continue
                    # creating an empty list
                    lst = []
                    # number of elements as input
                    n = int(input(f"Enter number of categories to harden(available: {7-script.total}) : "))
                    # loop if input is not in correct format
                    while n < 1 or n > (7-script.total):
                            print(f"Please enter a number between 1 to {7-script.total}")
                            n = int(input(f"Enter number of categories to harden(available: {7-script.total}) : "))
                    # iterating till the range
                    for i in range(0, n):
                        ele = str(input(f"Please enter category {i+1}: "))
                        while int(ele) < 1 or int(ele) > 7:
                            print("Please enter a number between 1 to 7")
                            ele = str(input(f"Please enter category {i+1}: "))   
                        # adding the element
                        lst.append(ele) 
                    for item in lst:
                        try:
                            useroutput.append(userchoice(item))
                            if useroutput[-1] == None:
                                useroutput.pop()
                                print(f"{dictionary(item)} hardened.")
                            else:
                                outputlist.append(str(item))                            
                        except:
                            print(f"{dictionary(item)} hardened.")
                    print(useroutput)
                elif script.level == "1":
                    if script.total == 6:
                        print("Everything has been hardened.")
                        continue
                    # creating an empty list
                    lst = []
                    # number of elements as input
                    n = int(input(f"Enter number of catergories to harden(available: {6-script.total}) : "))
                    # loop if input is not in correct format
                    while n < 1 or n > (6-script.total):
                            print(f"Please enter a number between 1 to {6-script.total}")
                            n = int(input(f"Enter number of categories to harden(available: {6-script.total}) : "))
                    # iterating till the range
                    for i in range(0, n):
                        ele = str(input(f"Please enter category {i+1}(excluding 6): "))
                        while int(ele) == 6 or int(ele) < 1 or int(ele) > 7:
                            print("Please enter a number between 1 to 7 except 6")
                            ele = str(input(f"Please enter category {i+1}(excluding 6): "))   
                        # adding the element
                        lst.append(ele) 
                    for item in lst:
                        try:
                            useroutput.append(userchoice(item))
                            if useroutput[-1] == None:
                                useroutput.pop()
                                print(f"{dictionary(item)} hardened.")
                            else:
                                outputlist.append(str(item))                                                                                  
                        except:
                            print(f"{dictionary(item)} hardened.")
                    print(useroutput)
                        
            elif user_choice == "0":
                userchoice(user_choice)

            elif script.level == "1" and int(user_choice) == 6 or int(user_choice) < 0 or int(user_choice) > 9:
                print("Please enter a number between 1 to 9 except 6")
            elif script.level == "2" and int(user_choice) < 0 or int(user_choice) > 9:
                print("Please enter a number between 1 to 9")
            else:
                try:
                    useroutput.append(userchoice(user_choice))
                    if useroutput[-1] == None:
                        useroutput.pop()
                        print(f"{dictionary(user_choice)} hardened.")
                    else:
                        outputlist.append(user_choice)
                    print(outputlist)                   
                except:
                    print(f"{dictionary(user_choice)} hardened.")
                print(useroutput)
        except:
            print("No number detected. Please enter a number between 1 to 9 except 6") 


if __name__ == "__main__":
    host = remoteHost
    username = userStr
    password = passStr

    main()
    for i in range(0, len(outputlist)):
        print(f'{"="*10} Trying to connect to Fortigate FW.... {"="*10}')

        connection = connect_to_fortigate(host, username, password)
        if connection:

            print(f'\nTime of Execution: {datetime.datetime.now()} SGT\n')
            print(f'{"="*10} Processing Hardening on FW for {dictionary(outputlist[i])} {"="*10}')
            print(useroutput[i])
            output = execute_commands(connection, useroutput[i])
            print(output)
            
            connection.disconnect()
        print(f'\n{"="*10} Completed and Exiting {"="*10}')
        print(f'Time of Completion: {datetime.datetime.now()} SGT')