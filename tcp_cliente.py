# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
import json
from tcp_server import *
from ar_server import *
from lamp_server import *

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


# conectar no server lampada
HOST_LAMP = '127.0.0.2'
PORT_LAMP = 20001

# conectar no server socket
HOST_AR = '127.0.0.3'
PORT_AR = 20002


def user_interface():
    login = str(input('Insira um Usuário: '))
    return login


def interface_option():
    while True:
        flag = int(
            input(("Deseja modificar qual dispositivo? (1) Lâmpada || (2) Ar-Condicionado: ")))
        if isinstance(flag, int) and flag in [1, 2]:
            break
    return flag


def interface_lamp(device_id=1):
    while True:
        lamp_flag = int(input(
            '\nLigar lâmpada (1)\nDesligar lâmpada (2)\nMudar cor de lâmpada (3)\nListar configuração atual (4) \nCriar nova lâmpada (5)\nSair (6): '))
        if isinstance(lamp_flag, int) and lamp_flag in [1, 2, 3, 4, 5, 6]:
            break
    if lamp_flag == 3:
        data_input = str(input('\nDefina a cor da lâmpada: '))
        return [device_id, lamp_flag, data_input]
    return [device_id, lamp_flag, None]


def interface_ar(device_id=2):
    while True:
        ar_flag = int(input(
            '\nLigar Ar-Condicionado (1)\nDesligar Ar-Condicionado (2)\nMudar temperatura de Ar-Condicionado (3)\nListar configuração atual (4)\nCriar novo Ar-Condicionado (5)\nSair (6): '))
        if isinstance(ar_flag, int) and ar_flag in [1, 2, 3, 4, 5, 6]:
            break
    if ar_flag == 3:
        data_input = str(input('\nDefina a temperatura do ar: '))
        return [device_id, ar_flag, data_input]
    return [device_id, ar_flag, None]


def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_lamp:
                socket_lamp.connect((HOST_LAMP, PORT_LAMP))
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_ar:
                    socket_ar.connect((HOST_AR, PORT_AR))
                    print("Cliente conectado ao servidor!")
                    while True:
                        # validar usuario (não pode haver colisão de nomes)
                        user_data = user_interface()
                        flag = interface_option()
                        if flag == 1:
                            information_to_be_sent = interface_lamp()
                        else:
                            information_to_be_sent = interface_ar()

                        metadata_msg = {'CLIENT_LOGIN': user_data,
                                        'DEVICE': information_to_be_sent[0],
                                        "OPERATION": information_to_be_sent[1],
                                        "DATA": information_to_be_sent[2],
                                        }
                        # envia dados coletados ao servidor de validação do cliente
                        metadata_msg_to_servers = json.dumps(metadata_msg)
                        if metadata_msg["OPERATION"] == 6:
                            s.send(metadata_msg_to_servers.encode())
                            socket_ar.send(metadata_msg_to_servers.encode())
                            socket_lamp.send(metadata_msg_to_servers.encode())
                            print("Aplicação será encerrada!")
                            break

                        s.send(metadata_msg_to_servers.encode())
                        # verifica resposta de validação do cliente
                        info_received = list(s.recv(BUFFER_SIZE))

                        if not info_received[0] and not info_received[1]:
                            print(
                                "Cadastro de cliente realizado, já que não existia!")
                        else:
                            print("Usuário validado!")

                        if metadata_msg["DEVICE"] == 1:
                            try:
                                socket_lamp.send(
                                    metadata_msg_to_servers.encode())
                                recv = (socket_lamp.recv(BUFFER_SIZE))
                                received_msg = json.loads(recv)
                                resposta_svr = received_msg[0]
                                print(resposta_svr)
                                if metadata_msg["OPERATION"] == 5 and len(received_msg[1]) > 1:
                                    print("Escolha uma lâmpada para copiar configurações de lâmpada já existente. ",
                                          "[", received_msg[1], "]: ", end='')
                                    decision = str(input())
                                elif metadata_msg["OPERATION"] == 5 and len(received_msg[1]) == 1:
                                    print(
                                        "Lâmpada criada recebeu configurações padrões! ", end='')
                                    decision = str(received_msg[1])
                                else:
                                    print("Qual lâmpada deseja editar: ",
                                          "[", received_msg[1], "]: ", end='')
                                    decision = str(input())
                                socket_lamp.send(decision.encode())
                                # edição de lampada
                                resposta = socket_lamp.recv(BUFFER_SIZE)
                                resposta_str = resposta.decode('utf-8')
                                print(resposta_str)
                            except Exception as e:
                                print(
                                    "Não foi possível conectar ao servidor da lâmpada. Erro: ", e)

                        if metadata_msg["DEVICE"] == 2:
                            try:
                                socket_ar.send(
                                    metadata_msg_to_servers.encode())
                                recv = (socket_ar.recv(BUFFER_SIZE))
                                received_msg = json.loads(recv)
                                resposta_svr = received_msg[0]
                                print(resposta_svr)
                                if metadata_msg["OPERATION"] == 5 and len(received_msg[1]) > 1:
                                    print("Escolha uma Ar-Condicionado para copiar configurações de Ar já existente. ",
                                          "[", received_msg[1], "]: ", end='')
                                    decision = str(input())
                                elif metadata_msg["OPERATION"] == 5 and len(received_msg[1]) == 1:
                                    print(
                                        "Ar Condicionado criado recebeu configurações padrões! ", end='')
                                    decision = str(received_msg[1])
                                else:
                                    print("Qual Ar Condicionado deseja editar: ",
                                          "[", received_msg[1], "]: ", end='')
                                    decision = str(input())
                                socket_ar.send(decision.encode())
                                # edição de lampada
                                resposta = socket_ar.recv(BUFFER_SIZE)
                                resposta_str = resposta.decode('utf-8')
                                print(resposta_str)
                            except Exception as e:
                                print(
                                    "Não foi possível conectar ao servidor do Ar Condicionado. Erro: ", e)

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
