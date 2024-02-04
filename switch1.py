from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler
import pandas as pd
import process_definition

hosts = pd.read_csv("./hosts.csv", usecols=["ip", "device_type", "fast_cli"])
for host in hosts.values.tolist():
    net_connect = process_definition.try_to_connect_to_switch(host[0], host[1])
    print(f'Connected to {net_connect.find_prompt().replace("#","")}')
    backup_config_file_name = f'./backup_config/{net_connect.find_prompt().replace("#","")}.txt'
    process_definition.write_config_from_switch(net_connect, backup_config_file_name)
    process_definition.deploy_config(net_connect)

    result_config_file_name = f'./result_config/{net_connect.find_prompt().replace("#","")}.txt'
    process_definition.write_config_from_switch(net_connect, result_config_file_name)
    net_connect.disconnect()

    # with ConnectHandler(**device) as net_connect:
    #     print(f'Connected to {net_connect.find_prompt().replace("#","")}')
    #     backup_config_file_name = f'./backup_config/{net_connect.find_prompt().replace("#","")}.txt'
    #     process_definition.write_config_from_switch(net_connect, backup_config_file_name)
    #     process_definition.deploy_config(net_connect)

    #     result_config_file_name = f'./result_config/{net_connect.find_prompt().replace("#","")}.txt'
    #     process_definition.write_config_from_switch(net_connect, result_config_file_name)
    #     net_connect.disconnect()
