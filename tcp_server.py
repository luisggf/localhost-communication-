# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
from threading import Thread
import json
from smart_devices import *
from csv_aux import *
import struct


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def on_new_client(clientsocket, addr):
    try:
        verificar_e_criar_arquivo_csv()
        while True:
            data = clientsocket.recv(BUFFER_SIZE)
            if not data:
                break

            texto_recebido = data.decode('utf-8')
            print('recebido do cliente {} na porta {}: {}'.format(
                addr[0], addr[1], texto_recebido))

            ip = addr[0]

            # Tenta converter a mensagem recebida para um dicionário JSON
            try:
                mensagem_json = json.loads(texto_recebido)
            except json.JSONDecodeError:
                mensagem_json = {}

            user_login = mensagem_json.get('CLIENT_LOGIN', '')

            client_existence_flag, user_login_colision_flag = check_client_test(
                ip, user_login)

            msg_to_server = struct.pack(
                '?', client_existence_flag) + struct.pack('?', user_login_colision_flag)

            clientsocket.send(msg_to_server)

            # shutdown_flag = clientsocket.recv(BUFFER_SIZE)
            # if shutdown_flag:
            #     print('Vai encerrar o socket do cliente {} !'.format(addr[0]))
            #     clientsocket.close()
            #     break

    except Exception as error:
        print('Erro: ', error)
        print("Erro na conexão com o cliente!!")
    finally:
        return


def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()

            print('Aguardando conexões...')
            while True:
                clientsocket, addr = server_socket.accept()
                print('Conectado ao cliente no endereço:', addr)
                t = Thread(target=on_new_client, args=(
                    clientsocket, addr))
                t.start()

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
