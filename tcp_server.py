# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
import random
from threading import Thread
import json
from smart_devices import *
import csv

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def cadastrar_dispositivo(self, tipo, configuracoes, endereco_ip):
    with open('devices.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
                                'device_id', 'status', 'modification_spec', 'current_config', 'ip'])

        # Verifica se o dispositivo já está cadastrado
        with open('devices.csv', mode='r') as read_file:
            content = csv.DictReader(read_file)
            for row in content:
                if row['ip'] == endereco_ip:
                    return f'Dispositivo já cadastrado com IP: {endereco_ip}'
        # Se não estiver cadastrado, adiciona uma nova linha no CSV
        device_id = len(list(content)) + 1
        default_status = False
        default_modification_spec = ''
        default_current_config = configuracoes.get('default_config', '')

        writer.writerow({'device_id': device_id, 'status': default_status, 'modification_spec': default_modification_spec,
                         'current_config': default_current_config, 'ip': endereco_ip})

        return f'Dispositivo cadastrado com sucesso! ID: {device_id}'


def gerar_endereco_ip():
    ip_base = "192.168.{}.{}"
    octeto3 = random.randint(0, 255)
    octeto4 = random.randint(0, 255)
    return ip_base.format(octeto3, octeto4)


def check_client(user_login, user_pass):
    with open('client.csv', mode='r') as file:
        content = csv.DictReader(file)

        for row in content:
            if row['user_login'] == user_login and row['user_pass'] == user_pass:
                return row['ip']

    # se credenciais não existem gera ip simulando um cliente aleatório
    new_ip = gerar_endereco_ip()

    # Append the new client to the CSV file
    with open('client.csv', mode='a', newline='\n') as file:
        fieldnames = ['user_login', 'user_pass', 'ip']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the new client to the CSV file
        writer.writerow({'user_login': user_login,
                        'user_pass': user_pass, 'ip': new_ip})

    return new_ip


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

            tipo_dispositivo = mensagem_json.get('DEVICE', '')
            comando = mensagem_json.get('OPERATION', '')
            dados = mensagem_json.get('DATA', '')
            user_login = mensagem_json.get('CLIENT_LOGIN', '')
            user_pass = mensagem_json.get('CLIENT_PASS', '')
            data = mensagem_json.get('CLIENT_DATA', '')

            ip = check_client(user_login, user_pass)

            if tipo_dispositivo == devices[tipo_dispositivo - 1].id and comando != 5 or comando != -1:
                dispositivo = devices[tipo_dispositivo - 1]
                resposta = dispositivo.processar_comando(comando, dados, ip)
                print(resposta)
                clientsocket.send(resposta.encode('utf-8'))

            if comando == 5 or comando == -1:
                print('Vai encerrar o socket do cliente {} !'.format(addr[0]))
                clientsocket.send(str(comando).encode('utf-8'))
                clientsocket.close()
                return

        except Exception as error:
            print(tipo_dispositivo, comando, 'Erro: ', error)
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
