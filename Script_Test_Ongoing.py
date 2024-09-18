import getpass

nc = 0
sc = 0
paoc = 0
spc = 0
sfc = 0
vc = 0
larc = 0
total = 0
vdom = ""

#network - done (global) (Level 1)
def network():
    global nc, total
    if nc == 1:
        return None
    else:
        zone = input("Does your FW have zone?(Yes/No)")
        port_number = input("Please enter the WAN port to disable all management related services(E.g. port1): ")
        if zone.lower() == "yes":
            commands = [
                # 1.1 Ensure DNS server is configured
                "config system dns",
                "set primary 8.8.8.8",
                "set secondary 8.8.4.4",
                "end",  

                # 1.2 Ensure intra-zone traffic is not always allowed
                "config system zone",
                "edit DMZ",
                "set intrazone deny",
                "end",

                # 1.3 Disable all management related services on WAN port
                "config system interface",
                f'edit "{port_number}"',
                "unselect allowaccess ping https ssh snmp http radius-acct",
                "end",
            ]
        else:
            commands = [
                # 1.1 Ensure DNS server is configured
                "config system dns",
                "set primary 8.8.8.8",
                "set secondary 8.8.4.4",
                "end",  

                # 1.3 Disable all management related services on WAN port
                "config system interface",
                f'edit "{port_number}"',
                "unselect allowaccess ping https ssh snmp http radius-acct",
                "end",
            ]
    nc = 1
    total += 1
    
    return commands

#system - undone (global) (Level 1 and 2)
def system():
    global sc, total
    if sc == 1:
        return None
    else:

        timezone = input("Please enter the timezone(E.g. 8): ")
        password = getpass.getpass(prompt='Please enter new password for admin: ')
        port_number = input("Please enter which port to allow only HTTPS access to the GUI and SSH access(E.g. port1): ")
        id = input("Please enter ID: ")
        commands = [
                # 2.1.1 Ensure 'Pre-Login Banner' is set /
                "config system global",
                "set pre-login-banner enable",
                "end",

                # 2.1.2 Ensure 'Post-Login-Banner' is set /
                "config system global",
                "set post-login-banner enable",
                "end",

                # 2.1.3 Ensure timezone is properly configured /
                'config system global',
                f'set timezone {timezone}',
                'end',

                # 2.1.4 Ensure correct system time is configured through NTP /
                'config system ntp',
                'set type custom',
                'config ntpserver',
                'edit 1',
                'set server pool.ntp.org',
                'next',
                'edit 2',
                'set server 1.1.1.1',
                'end',
                'end',

                # 2.1.5 Ensure hostname is set /
                "config system global",
                'set hostname "New_FGT1"',
                "end",

                # 2.1.6 Ensure the latest firmware is installed
                # # No CLI command, complete step in GUI

                # 2.1.7 Disable USB Firmware and configuration installation /
                "config system auto-install",
                "set auto-install-config disable",
                "set auto-install-image disable",
                "end",

                # 2.1.8 Disable static keys for TLS /
                "config system global",
                "set ssl-static-key-ciphers disable",
                "end",

                # 2.1.9 Enable Global Strong Encryption /
                "config system global",
                "set strong-crypto enable",
                "end",

                # 2.1.10 Ensure management GUI listens on secure TLS version /
                "config system global",
                "set admin-https-ssl-versions tlsv1-3",

                # 2.1.11 Ensure CDN is enabled for improved GUI performance /
                "config system global",
                "set gui-cdn-usage enable",
                "end",

                # # 2.1.12 Ensure single CPU core overloaded event is logged (not available in current version)
                # "config system global",
                # "set log-single-cpu-high enable",
                # "end",

                # 2.2.1 Ensure 'Password Policy' is enabled /
                "config system password-policy", 
                "set status enable",
                "set apply-to admin-password ipsec-preshared-key",
                "set minimum-length 8",
                "set min-lower-case-letter 1",
                "set min-upper-case-letter 1",
                "set min-non-alphanumeric 1",
                "set min-number 1",
                "set expire-status enable",
                "set expire-day 90",
                "set reuse-password disable",
                "end",

                # 2.2.2 Ensure administrator password retries and lockout time are configured /
                "config system global",
                "set admin-lockout-threshold 3",
                "set admin-lockout-duration 900",
                "end",

                # 2.3.1 Ensure only SNMPv3 is enabled /
                'config system snmp sysinfo',
                'set status enable',
                'end',
                'config system snmp community',
                'delete public',
                'end',
                'config system snmp user',
                'edit "snmp_test"',
                'set security-level auth-priv',
                'set auth-proto sha256',
                'set auth-pwd xxxx',
                'set priv-proto aes256',
                'set priv-pwd xxxx',
                'end',

                # 2.3.2 Allow only trusted hosts in SNMPv3 /
                'config system snmp user',
                'edit "snmp_test"',
                'unselect notify-hosts 0.0.0.0',
                'end',

                # 2.4.1 Ensure default 'admin' password is changed
                'config system admin',
                'edit "admin"',
                f'set password {password}',
                'end',

                # 2.4.2 Ensure all the login accounts having specific trusted hosts enabled
                # unsure what to add
                # remove trusted host
                'config system admin',
                'edit "test_admin"',
                'unset trusthost1',
                'end',
                # add trusted host
                'config system admin',
                'edit "test_admin"',
                'set trusthost6 1.1.1.1 255.255.255.255',
                'end',
                
                # 2.4.3 Ensure admin accounts with different privileges have their correct profiles assigned
                # Provide the profile "tier_1" the ability to view and modify address objects
                'config system accprofile',
                'edit "tier_1"',
                'set fwgrp custom',
                'config fwgrp-permission',
                'set address read-write',
                'end',
                'end',

                # Assign the profile "tier_1" to the account "support1".
                'config system admin',
                'edit "support1"',
                'set accprofile "tier_1"',
                'end',

                # 2.4.4 Ensure idle timeout time is configured (Level 1)
                "config system global",
                "set admintimeout 5",
                "end",    

                # Port 1 does not have allowaccess 
                # 2.4.5 Ensure only encrypted access channels are enabled
                "config system interface",
                f"edit {port_number}",
                "set allowaccess ssh https ping snmp",
                "end",

                # Need to clarify
                # 2.4.6 Apply Local-in Policies
                "config firewall {local-in-policy | local-in-policy6}",
                "edit <policy_number>",
                "set intf <interface>",
                "set srcaddr <source_address> [source_address] ...",
                "set dstaddr <destination_address> [destination_address] ...",
                "set action {accept | deny} set service <service_name> [service_name] ...",
                "set schedule <schedule_name>",
                "set comments <string>",
                "next",
                "end",

                # Example
                # 'config firewall address',
                # 'edit "10.10.10.0"',
                # 'set subnet 10.10.10.0 255.255.255.0',
                # 'next',
                # 'end',
                # 'config firewall local-in-policy',
                # 'edit 1 set intf "port1"',
                # 'set srcaddr "10.10.10.0"',
                # 'set dstaddr "all"',
                # 'set service "PING"',
                # 'set schedule "always"',
                # 'next',
                # 'end',

                # 2.4.7 Ensure default Admin ports are changed
                'config system global',
                'set admin-https-redirect disable',
                'set admin-port 8082 **(or any other uncommon port)**',
                'set admin-server-cert "self-sign"',
                'set admin-sport 4343 **(or any other uncommon port)**',
                'end',

                # 2.4.8 Virtual patching on the local-in management interface
                "config firewall local-in-policy",
                f"edit {id}",
                "set virtual-patch enable",
                "next",
                "end",
                
                # 2.5.1 Ensure High Availability configuration is enabled
                'config system ha',
                'set mode a-p', ####(Active-Passive)
                'set group-name "FGT-HA"', ###(Set cluster name)
                'set password *******',  ###(Set password)
                'set hbdev port10 50',   ###(Set Heartbeat Interface and priority)
                'end',

                # set password ENC does not change
                # 2.5.2 Ensure "Monitor Interfaces" for High Availability devices is enabled
                "config system ha",
                'set monitor "port6" "port7"',
                "end",  

                # 2.5.3 Ensure HA Reserved Management Interface is configured
                'config system ha',
                'set ha-mgmt-status enable',
                'config ha-mgmt-interfaces',
                'edit 1',
                'set interface port6',
                'set gateway 10.10.10.1',
                'end',
                'end',

    ]
    sc = 1
    total += 1
    return commands

#policy and object - undone (vdom) (Level 1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
def Policy_and_object():
    global paoc, total, vdom
    if paoc == 1:
        return None
    else:
        commands = [
            "end",
            "config vdom",
            f"edit {vdom}",
            # 3.1 Ensure that unused policies are reviewed regularly
            # No CLI command, complete step in GUI

            # 3.2 Ensure that policies do not use "ALL" as Service (vdom)
            'config firewall policy',
            'edit 2',
            'set service "FTP" "SNMP"',
            'end',

            # 3.3 Ensure firewall policy denying all traffic to/from Tor, malicious server, or scanner IP addresses using ISDB
            # No CLI command, complete step in GUI

            # 3.4 Ensure logging is enabled on all firewall policies
            # No CLI command, complete step in GUI
            "end",
            "config global",
        ]
    paoc = 1
    total += 1
    return commands

#security profiles - undone (global and vdom) (Level 1 and 2)
def Security_profiles():
    global spc, total, vdom
    if spc == 1:
        return None
    else:
        profile_name = input("Please enter profile to be edited: ")
        commands = [

            # 4.1.1 Detect Botnet connections
            # No CLI command, complete step in GUI

            # 4.1.2 Apply IPS Security Profile to Policies
            # No CLI command, complete step in GUI

            # 4.2.1 Ensure Antivirus Definition Push Updates are Configured (global)
            "config system autoupdate schedule",
            "set status enable",
            "set frequency automatic",
            "end",

            # 4.2.2 Apply Antivirus Security Profile to Policies
            # No CLI command, complete step in GUI

            # 4.2.3 Enable Outbreak Prevention Database
            # No CLI command, complete step in GUI

            # 4.2.4 Enable AI /heuristic based malware detection (vdom)
            "end"
            "config vdom"
            f"edit {vdom}"

            "config antivirus settings",
            "set machine-learning-detection enable",

            # 4.2.5 Enable grayware detection on antivirus (vdom)
            "config antivirus settings",
            "set grayware enable",

            # 4.2.6 Ensure inline scanning with FortiGuard AI-Based Sandbox Service is enabled
            #not complete

            # 4.3.1 Enable Botnet C&C Domain Blocking DNS Filter
            # No CLI command, complete step in GUI
        
            # 4.3.2 Ensure DNS Filter logs all DNS queries and responses
            # No CLI command, complete step in GUI

            # 4.3.3 Apply DNS Filter Security Profile to Policies
            # No CLI command, complete step in GUI

            # 4.4.1 Block high risk categories on Application Control
            # No CLI command, complete step in GUI
            "end",
            "end",
            "config global",

            # 4.4.2 Block applications running on non-default ports (global)
            'config application list',
            f'edit "{profile_name}"',
            'set enforce-default-app-port enable',
            'end',
            # 4.4.3 Ensure all Application Control related traffic is logged
            # No CLI command, complete step in GUI

            # 4.4.4 Apply Application Control Security Profile to Policies
            # No CLI command, complete step in GUI

        
        ]
    spc = 1
    total += 1
    return commands

#security fabric - done (global) (level 1)
def Security_Fabric():
    global sfc,total
    if sfc == 1:
        return None
    else:
        commands = [

            # 5.1.1 Enable Compromised Host Quarantine (Level 1)
            'config system automation-action',
            'edit "Quarantine on FortiSwitch + FortiAP"',
            'set description "Default automation action configuration for quarantining a MAC address on FortiSwitches and FortiAPs."',
            'set action-type quarantine',
            'next',
            'edit "Quarantine FortiClient EMS Endpoint"',
            'set description "Default automation action configuration for quarantining a FortiClient EMS endpoint device."',
            'set action-type quarantine-forticlient',
            'next',
            'end',
            'config system automation-trigger',
            'edit "Compromised Host - High"',
            'set description "Default automation trigger configuration for when a high severity compromised host is detected."',
            'next',
            'end',
            'config system automation-stitch',
            'edit "Compromised Host Quarantine"',
            'set description "Default automation stitch to quarantine a high severity compromised host on FortiAPs, FortiSwitches, and FortiClient EMS."',
            'set status enable',
            'set trigger "Compromised Host - High"',
            'config actions',
            'edit 1',
            'set action "Quarantine on FortiSwitch + FortiAP"',
            'next',
            'edit 2',
            'set action "Quarantine FortiClient EMS Endpoint"',
            'next',
            'end',
            'next',
            'end',

            # 5.2.1.1 Ensure Security Fabric is Configured
            # No CLI command, complete step in GUI
        ]
    sfc = 1
    total += 1
    
    return commands

#vpn - done (vdom) (Level 2)
def VPN():
    global vc, total
    if vc == 1:
        return None
    else:
        commands = [
            "end",
            "config vdom",
            f"edit {vdom}",

            # 6.1.1 Apply a Trusted Signed Certificate for VPN Portal
            # No CLI command, complete step in GUI

            # 6.1.2 Enable Limited TLS Versions for SSL VPN (vdom)
            "config vpn ssl settings",
            "set ssl-max-prot-ver tls1-3",
            "set ssl-min-proto ver tls1-2",
            "set algorithm high",

            "end",
            "end",
            "config global",

        ]
    vc = 1
    total += 1
    
    return commands

#logs and reports - undone (Level 1 and 2) (global and vdom) Issue: Attribute 'server' MUST be set. Command fail. Return code -56
def Logs_and_reports():
    global larc, total
    if larc == 1:
        return None
    else:
        commands = [
            "end",
            "config vdom",
            f"edit {vdom}",
            # 7.1.1 Enable Event Logging (vdom)
            "config log eventfilter",
            "set event enable",
            "end",
            "end",
           
            "config global",
            # 7.2.1 Encrypt Log Transmission to FortiAnalyzer / FortiManager (global)
            "config log fortianalyzer setting",
            "set status enable",
            "set reliable enable",
            "set enc-algorithm high",
            "end",

            # 7.3.1 Centralized Logging and Reporting
            # No CLI command, complete step in GUI
        ]
    larc = 1
    total += 1
    
    return commands
