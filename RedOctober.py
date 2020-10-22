
# V1 : dpeet 9/21/2020 - Site separation for Enterprise wide incident

from netmiko import ConnectHandler

print("*************WARNING!!***************\n\n")
proceed = input("Running this program will sever communication between all major sites - CDR CAMPUS, P2P, MPLS and IPSec\nDo you wish to continue? (Y or N)").upper()

if proceed != "Y" or "YES":
    quit()


core_switch = {
    'device_type': 'cisco_ios',
    'host': '10.2.200.253',
    'username': 'ipsoft',
    'password': 'crstC1sc0',
    }

mpls_switch = {
    'device_type': 'cisco_ios',
    'host': '10.2.75.1',
    'username': 'ipsoft',
    'password': 'crstC1sc0',
    }

csw_switch = {
    'device_type': 'cisco_ios',
    'host': '10.2.50.253',
    'username': 'ipsoft',
    'password': 'crstC1sc0',
    }

CDR1_FW = {
    'device_type': 'fortinet',
    'host': '10.2.0.70',
    'username': 'admin',
    'password': 'crstC1sc0',
    }

#common device ports/tunnels
core_p2p=['3/4','3/6','3/17','3/18']
ipsec_shut=['CAR1','CDR5-Backup','CDR6_Downtown','FTW1','FTW1_Backup','GardnerVPN','ATL2','MLP1','LAR1','MLP1','DAL1','CIN1-BESL','EDG1','EPO1','NTA1','OKC1','RIV1','SFL1','VST1-FORT-AFW']


#shutdown P2Ps and CDR3 in DSW1
core = ConnectHandler(**core_switch)
core.send_command_timing('conf t')
for port in core_p2p:
    cmd=(f"int gig {port}")
    core.send_command_timing(cmd)
    core.send_command('shut')
core.save_config()
core.disconnect()

#shutdown MPLS in SRVSTACK
mpls = ConnectHandler(**mpls_switch)
mpls.send_command_timing('conf t')
mpls.send_command_timing('int gig 2/0/48')
mpls.send_command('shut')
mpls.save_config()
mpls.disconnect()

#shutdown CDR5 in CSW1
csw = ConnectHandler(**csw_switch)
csw.send_command_timing('conf t')
csw.send_command_timing('int te 1/3')
csw.send_command('shut')
csw.save_config()
csw.disconnect()


#shutdown IPSecs
fw = ConnectHandler(**CDR1_FW)
fw.send_command_timing('config system interface')
for site in ipsec_shut:
    cmd=(f"edit {site}")  
    fw.send_command_timing(cmd)
    fw.send_command('set status down')
    fw.send_command_timing('next')
fw.disconnect()

