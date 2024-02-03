import socket
import sys
import random
from threading import Thread
import json
from smart_devices import *
import csv
import ast


def verificar_e_criar_arquivo_csv():
    arquivo_csv = 'devices.csv'
    arquivo_csv_client = 'client.csv'

    # checa se arquivo existe no diretorio atual
    if not os.path.exists(arquivo_csv):
        # caso não exista, ele é criado e tem cabeçalho adicionado para evitar errors com a função processar comando
        with open(arquivo_csv, mode='w', newline='') as file:
            fieldnames = ['device_id', 'unique_id',
                          'status', 'current_config', 'ip']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    if not os.path.exists(arquivo_csv_client):
        with open(arquivo_csv_client, mode='w', newline='') as file:
            fieldnames = ['user_login', 'user_pass', 'ip', 'devices_list']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


def gerar_endereco_ip():
    ip_base = "192.168.{}.{}"
    octeto3 = random.randint(0, 255)
    octeto4 = random.randint(0, 255)
    return ip_base.format(octeto3, octeto4)


def check_client(user_login, user_pass, unique_id):
    ip_to_update = None
    unique_ids = []

    with open('devices.csv', mode='r') as devices_file:
        devices_content = list(csv.DictReader(devices_file))

        with open('client.csv', mode='r') as client_file:
            client_content = list(csv.DictReader(client_file))

            for device_row in devices_content:
                for client_row in client_content:
                    if device_row['ip'] == client_row['ip']:
                        ip_to_update = client_row['ip']

                        # Check if unique_id is not already in the devices_list
                        if device_row['unique_id'] not in client_row['devices_list']:
                            unique_ids.append(device_row['unique_id'])

                            # Append the unique_id to the 'devices_list' column
                            current_devices_list = client_row['devices_list']
                            if current_devices_list:
                                current_devices_list += f',{device_row["unique_id"]}'
                            else:
                                current_devices_list = device_row["unique_id"]
                            client_row['devices_list'] = current_devices_list

            if unique_ids:
                # Update the 'client.csv' file with unique_ids in the 'devices_list' column
                with open('client.csv', mode='w', newline='') as client_file:
                    fieldnames = ['user_login',
                                  'user_pass', 'ip', 'devices_list']
                    writer = csv.DictWriter(client_file, fieldnames=fieldnames)

                    # Write the header
                    writer.writeheader()

                    # Write the updated rows
                    writer.writerows(client_content)

                return ip_to_update


def check_client_test(ip, user_login):
    with open('client.csv', mode='r') as file:
        content = csv.DictReader(file)
        clients = list(content)
        clients_ips = {client['ip'] for client in clients}
        clients_user_logins = {client['user_login'] for client in clients}
        if ip not in clients_ips or user_login not in clients_user_logins:
            # cliente nao cadastrado
            with open('client.csv', mode='a', newline='\n') as file:
                fieldnames = ['user_login', 'ip', 'devices_list']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writerow({'user_login': user_login,
                                 'ip': ip,
                                 'devices_list': ''})
            with open('client_ar.csv', mode='a', newline='\n') as file_2:
                fieldnames = ['user_login', 'ip', 'devices_list']
                writer = csv.DictWriter(file_2, fieldnames=fieldnames)

                writer.writerow({'user_login': user_login,
                                 'ip': ip,
                                 'devices_list': ''})
            return False, False
        elif user_login in clients_user_logins:
            return True, True


def check_client_test_ar(ip, user_login):
    with open('client_ar.csv', mode='r') as file:
        content = csv.DictReader(file)
        clients = list(content)
        clients_ips = {client['ip'] for client in clients}
        clients_user_logins = {client['user_login'] for client in clients}
        if ip not in clients_ips or user_login not in clients_user_logins:
            # cliente nao cadastrado
            with open('client.csv', mode='a', newline='\n') as file:
                fieldnames = ['user_login', 'ip', 'devices_list']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writerow({'user_login': user_login,
                                 'ip': ip,
                                 'devices_list': ''})
            return False, False
        elif user_login in clients_user_logins:
            return True, True


def get_devices_info_by_ip(ip, client_data, option, client_csv='client.csv', devices_csv='devices.csv'):
    devices_info = ""

    with open(client_csv, mode='r') as client_file:
        client_content = csv.DictReader(client_file)
        client_content = list(client_content)

        for client_row in client_content:
            if not client_row['devices_list']:
                client_row['devices_list'] = ''
            if client_row['ip'] == ip:
                unique_ids = list(
                    set(client_row['devices_list'].strip('"').split(",")))
                with open(devices_csv, mode='r') as devices_file:
                    devices_content = csv.DictReader(devices_file)
                    devices_content = list(devices_content)
                    for device_row in devices_content:
                        if device_row['unique_id'] in unique_ids and device_row['device_id'] == str(client_data):
                            devices_info += f"Device ID: {device_row['device_id']}, Unique ID: {device_row['unique_id']}, Status: {device_row['status']}, Current Config: {device_row['current_config']}, New Device: {option}\n"
    return devices_info
