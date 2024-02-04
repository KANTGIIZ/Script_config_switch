from netmiko import ConnectHandler, BaseConnection
import pandas as pd

def try_to_connect_to_switch(ip:str, device_type:str, fast_cli=True) -> BaseConnection:
    secret_lists = pd.read_csv("./secrets.csv").values.tolist()
    for secret in secret_lists:
        device = {
            'host': ip,
            'username': secret[0],
            'password': secret[1],
            'device_type': device_type,
            'fast_cli': fast_cli
        }
        try:
            net_connect = ConnectHandler(**device)
            return net_connect
        except Exception as e:
            print(f'Cannot connect to {ip}')
            print(str(e))
            continue

def write_config_from_switch(connection: BaseConnection, fileName: str):
    config = connection.send_command("show run", delay_factor=5, read_timeout=60)
    with open(fileName, "w", encoding="utf8") as backup_file:
        backup_file.write(config)

def deploy_config(connection: BaseConnection):
    connection.config_mode()
    with open("config.txt", "r", encoding="utf8") as config_command:
        for command in config_command.readlines():
            if not (command is None or command == ""):
                command_result = connection.send_command(command)
            print(command_result)
    connection.exit_config_mode()