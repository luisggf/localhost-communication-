# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
from threading import Thread
import json
from smart_devices import *

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


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

            if tipo_dispositivo == devices[tipo_dispositivo - 1].id and comando != 5:
                dispositivo = devices[tipo_dispositivo - 1]
                resposta = dispositivo.processar_comando(comando, dados)
                print(resposta)
                clientsocket.send(resposta.encode('utf-8'))

            if comando == 5:
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
