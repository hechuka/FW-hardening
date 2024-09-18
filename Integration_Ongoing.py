import netmiko
import getpass
import datetime
import Script_Test_Ongoing as script

menu = True
useroutput = ['config global',]
#useroutput = ""
# Getting the Password but without showing the password; Otherwise use input() for normal data request.
defaultStr = input('Default IP/Username? Type "y" for default values: ')

remoteHost = ""
userStr = ""
passStr = ""



# Remote Host Details
if defaultStr.lower() == 'y':
    remoteHost = "10.10.101.2 "
    userStr = "nera"
    passStr = "3e4r5t^Y&U*I"
else:
    remoteHost = input('IP of Remote Host: ')
    userStr = input('Username : ')
    passStr = getpass.getpass(prompt='FW Password: ')



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

# def execute_command(connection, command):
#     output = connection.send_command(command)
#     return output

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

def mainmenu():
    global useroutput
    script.Vdom() 
    while menu == True:
        try:
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
                                \n0. Proceed with FW hardening...\n"
                                )
            
            if user_choice == "8":
                if script.total == 7:
                    print("Everything has been hardened.")
                    continue               
                for item in range(7):
                    try:
                        useroutput.extend(userchoice(str(item + 1)))
                        print(useroutput)
                    except:
                        print(f"{dictionary(str(item + 1))} hardened.")

            elif user_choice == "9":
                if script.total == 7:
                    print("Everything has been hardened.")
                    continue
                # creating an empty list
                lst = []
                # number of elements as input
                n = int(input(f"Enter number of elements(available: {7-script.total}) : "))
                # loop if input is not in correct format
                while n < 1 or n > (7-script.total):
                        print(f"Please enter a number between 1 to {7-script.total}")
                        n = int(input(f"Enter number of elements(available: {7-script.total}) : "))
                # iterating till the range
                for i in range(0, n):
                    ele = str(input())
                    while int(ele) < 1 or int(ele) > 7:
                        print("Please enter a number between 1 to 7")
                        ele = str(input())   
                    # adding the element
                    lst.append(ele) 
                for item in lst:
                    try:
                        useroutput.extend(userchoice(item))
                        print(useroutput)
                    except:
                        print(f"{dictionary(item)} hardened.")
                        
            elif user_choice == "0":
                userchoice(user_choice)

            elif int(user_choice) < 0 or int(user_choice) > 9:
                print("Please enter a number between 1 to 9")
            else:
                try:
                    useroutput.extend(userchoice(user_choice))
                    print(useroutput)
                except:
                    print(f"{dictionary(user_choice)} hardened.")
        except:
            print("No number detected. Please enter a number between 1 to 9")


if __name__ == "__main__":
    host = remoteHost
    username = userStr
    password = passStr

    mainmenu()

    print(f'{"="*10} Trying to connect to Fortigate FW.... {"="*10}')

    connection = connect_to_fortigate(host, username, password)
    if connection:


        print(f'\nTime of Execution: {datetime.datetime.now()} SGT\n')
        print(f'{"="*10} Processing Hardening on FW.... {"="*10}')
        #print(useroutput)
        output = execute_commands(connection, useroutput)
        print(output)
        
        connection.disconnect()
        print(f'\n{"="*10} Completed and Exiting {"="*10}')

        print(f'Time of Completion: {datetime.datetime.now()} SGT')