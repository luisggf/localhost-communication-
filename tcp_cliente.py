# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
import json


HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def interface():
    while True:
        flag = int(input(
            'Selecione uma opção: Lâmpada Inteligente (1) Ar Condicionado (2) Sair (3): '))
        if isinstance(flag, int) and flag in [1, 2, 3]:
            break

    if flag == 1:
        while True:
            lamp_flag = int(input(
                'Ligar lâmpada (1)\nDesligar lâmpada (2)\nMudar cor de lâmpada (3)\nListar configuração atual (4)\nSair (5): '))
            if isinstance(lamp_flag, int) and lamp_flag in [1, 2, 3, 4]:
                break
            if lamp_flag == 3:
                data_input = str(input('Defina a cor da lâmpada: '))
                return [1, lamp_flag, data_input]
        return [1, lamp_flag, None]
    else:
        while True:
            ac_flag = int(input(
                'Ligar o Ar Condicionado: (1)\nDesligar o Ar Condicionado: (2)\nDefinir temperatura do ar: (3)\nListar configuração atual (4)\nSair(5): '))
            if isinstance(ac_flag, int) and ac_flag in [1, 2, 3, 4]:
                break
            if ac_flag == 3:
                data_input = str(input('Defina a temperatura do ar: '))
                return [2, ac_flag, data_input]
        return [2, ac_flag, None]


def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Cliente conectado ao servidor!")

            while True:
                flag = interface()
                my_obj = {'DEVICE': flag[0],
                          "OPERATION": flag[1],
                          "DATA": flag[2]}

                json_string = json.dumps(my_obj)

                # flag.encode - converte a string para bytes
                s.send(json_string.encode())
                data = s.recv(BUFFER_SIZE)
                # converte de bytes para um formato "printável"
                # texto_recebido = repr(data)
                # print('Recebido do servidor: ', texto_recebido)
                # converte os bytes em string
                texto_string = data.decode('utf-8')
                print('Recebido do servidor: ', texto_string)

                if texto_string == '5':
                    print('O servidor encerrou a conexão!')
                    s.close()
                    break

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
