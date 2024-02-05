# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
import json

# substituir pelo endereço ipv4 do computador servidor
HOST = '192.168.0.101'  # endereço IP
PORT = 20001            # Porta utilizada pelo servidor
BUFFER_SIZE = 1024      # tamanho do buffer para recepção dos dados


# conectar no server lampada
HOST_LAMP = '192.168.0.101'
PORT_LAMP = 20003

# conectar no server socket
HOST_AR = '192.168.0.101'
PORT_AR = 20002


def user_interface():
    """
        Recebe Input do usuário de informação cadastral: Nome de usuário.
    """
    login = str(input('Insira um Usuário: '))
    return login


def interface_option():
    """
        Recebe Input do usuário de qual dispositivo será modificado.
    """
    while True:
        try:
            flag = int(
                input(("Deseja modificar qual dispositivo? (1) Lâmpada || (2) Ar-Condicionado: ")))
            if flag in [1, 2]:
                break
            else:
                print(
                    "Intervalo indefinido ou tipo de dados inválido, por favor escolha (1 ou 2)!")
        except:
            print(
                "Intervalo indefinido ou tipo de dados inválido, por favor escolha (1 ou 2)!")
    return flag


def interface_lamp(device_id=1):
    """
        Recebe Input do usuário de qual será a operação realizada sobre a lâmpada X.
    """
    while True:
        try:
            lamp_flag = int(input(
                '\nLigar lâmpada (1)\nDesligar lâmpada (2)\nMudar cor de lâmpada (3)\nListar configuração atual (4) \nCriar nova lâmpada (5)\nSair (6): '))
            if lamp_flag in range(1, 6):
                break
            else:
                print(
                    "Intervalo indefinido ou tipo de dados inválido, por favor escolha (1,2,3,4,5 ou 6)!")
        except:
            print(
                "Intervalo indefinido ou tipo de dados inválido, por favor escolha (1,2,3,4,5 ou 6)!")
    if int(lamp_flag) == 3:
        allowed_colors = ['white', 'red',
                          'green', 'blue',
                          'cyan', 'magenta',
                          'branco', 'vermelho',
                          'amarelo', 'verde',
                          'azul', 'ciano',
                          'yellow', 'laranja', 'orange']
        while True:
            data_input = str(input('\nDefina a cor da lâmpada: '))

            if data_input.lower() not in allowed_colors:
                print(
                    f"Cor é inválida para o dispositivo. Escolha uma das cores a seguir: {allowed_colors}")
            else:
                return [device_id, lamp_flag, data_input]
    return [device_id, lamp_flag, None]


def interface_ar(device_id=2):
    """
        Recebe Input do usuário de qual será a operação realizada sobre a Ar Condicionado X.
    """
    while True:
        try:
            ar_flag = int(input(
                '\nLigar Ar-Condicionado (1)\nDesligar Ar-Condicionado (2)\nMudar temperatura de Ar-Condicionado (3)\nListar configuração atual (4)\nCriar novo Ar-Condicionado (5)\nSair (6): '))
            if ar_flag in range(1, 6):
                break
            else:
                print(
                    "Intervalo indefinido ou tipo de dados inválido, por favor escolha (1,2,3,4,5 ou 6)!")
        except:
            print(
                "Intervalo indefinido ou tipo de dados inválido, por favor escolha (1,2,3,4,5 ou 6)!")

    if ar_flag == 3:
        allowed_range = range(15, 30)
        while True:
            try:
                data_input = int(input('\nDefina a temperatura do ar: '))
                if data_input not in allowed_range:
                    print(
                        f"Valor de temperatura não é válido. Por favor escolha um valor entre: {allowed_range}")
                else:
                    return [device_id, ar_flag, data_input]
            except:
                print(
                    f"Formato de dados inválido, por favor forneça um valor entre: {allowed_range}")
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
                                if metadata_msg["OPERATION"] == 5:
                                    while True:
                                        try:
                                            if len(received_msg[1]) == 1:
                                                print(
                                                    "Lâmpada criada recebeu configurações padrões! ", end='')
                                                decision = str(received_msg[1])
                                                break
                                            elif len(received_msg[1]) > 1:
                                                decision = int(input(f"Escolha uma Lâmpada para copiar configurações já existente: "
                                                                     f"[{received_msg[1]}]: "))
                                                if decision in received_msg[1]:
                                                    break
                                                else:
                                                    print(
                                                        "Por Favor informe um dispositivo válido!")
                                        except ValueError:
                                            print(
                                                "Por Favor informe o dispositivo corretamente!")
                                else:
                                    while True:
                                        try:
                                            decision = int(input(f"Escolha uma Lâmpada para editar: "
                                                                 f"[{received_msg[1]}]: "))
                                            if decision in received_msg[1]:
                                                break
                                        except:
                                            print(
                                                "Por Favor informe um dispositivo válido!")
                                decision = str(decision)
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
                                if metadata_msg["OPERATION"] == 5:
                                    while True:
                                        try:
                                            if isinstance(received_msg[1], int):
                                                print(
                                                    "Ar Condicionado criado recebeu configurações padrões! ", end='')
                                                decision = str(received_msg[1])
                                                break
                                            elif isinstance(received_msg[1], list):
                                                decision = int(input(f"Escolha um Ar Condicionado para copiar configurações já existente: "
                                                                     f"[{received_msg[1]}]: "))
                                                if decision in received_msg[1]:
                                                    break
                                                else:
                                                    print(
                                                        "Por Favor informe um dispositivo válido!")
                                        except ValueError:
                                            print(
                                                "Por Favor informe o dispositivo corretamente!")
                                else:
                                    while True:
                                        try:
                                            decision = int(input(f"Escolha uma Lâmpada para editar: "
                                                                 f"[{received_msg[1]}]: "))
                                            if decision in received_msg[1]:
                                                break
                                        except:
                                            print(
                                                "Por Favor informe um dispositivo válido!")
                                decision = str(decision)
                                decision = str(decision)
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
