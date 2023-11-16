# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
import random
from threading import Thread
import json
from smart_devices import *
import csv
import ast

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


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

    with open('client.csv', mode='r') as file:
        content = csv.DictReader(file)
        for row in content:
            if row['user_login'] == user_login and row['user_pass'] == user_pass:
                return row['ip']

    # se credenciais não existem gera ip simulando um cliente aleatório
    new_ip = gerar_endereco_ip()

    with open('client.csv', mode='a', newline='\n') as file:
        fieldnames = ['user_login', 'user_pass', 'ip', 'devices_list']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writerow({'user_login': user_login,
                        'user_pass': user_pass, 'ip': new_ip,
                         'devices_list': unique_id})

    return new_ip


def get_devices_info_by_ip(ip, client_csv='client.csv', devices_csv='devices.csv'):
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
                        if device_row['unique_id'] in unique_ids:
                            devices_info += f"Device ID: {device_row['device_id']}, Unique ID: {device_row['unique_id']}, Status: {device_row['status']}, Current Config: {device_row['current_config']}\n"
    return devices_info


def on_new_client(clientsocket, addr, devices):
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE)
            if not data:
                break

            # converte os bytes em string
            texto_recebido = data.decode('utf-8')
            print('recebido do cliente {} na porta {}: {}'.format(
                addr[0], addr[1], texto_recebido))

            # Tenta converter a mensagem recebida para um dicionário JSON
            try:
                mensagem_json = json.loads(texto_recebido)
            except json.JSONDecodeError:
                mensagem_json = {}

            user_login = mensagem_json.get('CLIENT_LOGIN', '')
            user_pass = mensagem_json.get('CLIENT_PASS', '')
            client_data = mensagem_json.get('CLIENT_DATA', '')

            ip = check_client(user_login, user_pass, '')

            message = get_devices_info_by_ip(ip)
            if not message:
                message = 'None'
            try:
                clientsocket.send(message.encode('utf-8'))
            except Exception as error:
                print(error)
                return

            data = clientsocket.recv(BUFFER_SIZE)

            if not data:
                break

            try:
                mensagem_json = json.loads(data)
            except json.JSONDecodeError:
                mensagem_json = {}

            # converte os bytes em string
            texto_recebido = data.decode('utf-8')
            print('recebido do cliente {} na porta {}: {}'.format(
                addr[0], addr[1], texto_recebido))

            tipo_dispositivo = mensagem_json.get('DEVICE', '')
            unique_id = mensagem_json.get('UNIQUE_ID', '')
            comando = mensagem_json.get('OPERATION', '')
            dados = mensagem_json.get('DATA', '')

            if tipo_dispositivo == devices[tipo_dispositivo - 1].id and comando != 5 or comando != -1:
                dispositivo = devices[tipo_dispositivo - 1]
                resposta = dispositivo.processar_comando(
                    comando, dados, ip, client_data, unique_id)
                print(resposta)
                clientsocket.send(resposta.encode('utf-8'))

            if comando == 5 or comando == -1:
                print('Vai encerrar o socket do cliente {} !'.format(addr[0]))
                clientsocket.send(str(comando).encode('utf-8'))
                clientsocket.close()
                return

        except Exception as error:
            # print(tipo_dispositivo, comando, 'Erro: ', error)
            print('Erro: ', error)
            print("Erro na conexão com o cliente!!")
            return


def main(argv):

    try:
        lamp = Lampada()
        air_conditioner = ArCondicionado()
        devices = [lamp, air_conditioner]

        print(devices, devices[1].id)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=on_new_client, args=(
                    clientsocket, addr, devices))
                t.start()

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
