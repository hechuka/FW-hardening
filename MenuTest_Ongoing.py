import Script_Test_Ongoing as script
output = []
menu = True

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

def level():
    script.level = input("Please select Level 1 or 2 hardening(E.g. 1): ")
    print(script.level)
    while int(script.level) < 1 or int(script.level) > 2:
        script.level = input("Please select Level 1 or 2 hardening(E.g. 1): ")

def main():
    global output, lst, user_choice, outputlist
    outputlist = []
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
                            output.append(userchoice(str(item + 1)))
                            outputlist.append(str(item + 1))                        
                        except:
                            print(f"{dictionary(str(item + 1))} hardened.")
                    print(output)
                elif script.level == "1":
                    if script.total == 6:
                        print("Everything has been hardened.")
                        continue               
                    for item in range(5):
                        try:
                            output.append(userchoice(str(item + 1)))
                            outputlist.append(str(item + 1))                        
                        except:
                            print(f"{dictionary(str(item + 1))} hardened.")
                    try:
                        output.append(userchoice("7"))
                        outputlist.append("7")                    
                    except:
                        print(f"{dictionary("7")} hardened.")
                    print(output)

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
                            output.append(userchoice(item))
                            outputlist.append(str(item))                        
                        except:
                            print(f"{dictionary(item)} hardened.")
                    print(output)
                    print(lst)
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
                            output.append(userchoice(item))
                            outputlist.append(str(item))                        
                        except:
                            print(f"{dictionary(item)} hardened.")
                    print(output)                   
                    print(lst)
                        
            elif user_choice == "0":
                userchoice(user_choice)

            elif script.level == "1" and int(user_choice) == 6 or int(user_choice) < 0 or int(user_choice) > 9:
                print("Please enter a number between 1 to 9 except 6")
            elif script.level == "2" and int(user_choice) < 0 or int(user_choice) > 9:
                print("Please enter a number between 1 to 9")
            else:
                try:
                    output.append(userchoice(user_choice))
                    outputlist.append(str(user_choice))                    
                except:
                    print(f"{dictionary(user_choice)} hardened.")
                print(output)
        except:
            print("No number detected. Please enter a number between 1 to 9 except 6") 

if __name__ == "__main__":
    level()
    main()
    for i in range(0, len(outputlist)):
        print(f'{"="*10} Processing Hardening on FW for {dictionary(outputlist[i])} {"="*10}')
        print(output[i])  