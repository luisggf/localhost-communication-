# -*- coding: utf-8 -*-
__author__ = "Filipe Ribeiro"

import socket
import sys
import json

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def user_interface():
    login = str(input('Usuário: '))
    senha = str(input('Senha: '))
    option = str(input('Deseja adicionar um novo dispositivo? [s]/[n]: '))
    if option == 's':
        data = int(input(
            'Qual dispositivo deseja adicionar: Lâmpada Inteligente (1) Ar Condicionado (2): '))
        return login, senha, data, option

    data = int(input(
        'Qual dispositivo deseja modificar: Lâmpada Inteligente (1) Ar Condicionado (2): '))

    return login, senha, data, option


def interface(option, data_client):

    if (data_client == 1 and option == 's'):
        return [1, None, None, None]
    if (data_client == 2 and option == 's'):
        return [2, None, None, None]
    # while True:
    #     flag = int(input(
    #         '\nSelecione uma opção: Lâmpada Inteligente (1)\nAr Condicionado (2)\nSair (3): '))
    #     if isinstance(flag, int) and flag in [1, 2, 3]:
    #         break
    #     if flag == 3:
    #         return [-1, -1, -1, None]

    if data_client == 1:
        while True:
            lamp_flag = int(input(
                '\nLigar lâmpada (1)\nDesligar lâmpada (2)\nMudar cor de lâmpada (3)\nListar configuração atual (4)\nSair (5): '))
            if isinstance(lamp_flag, int) and lamp_flag in [1, 2, 3, 4]:
                break
        if lamp_flag == 3:
            data_input = str(input('\nDefina a cor da lâmpada: '))
            return [1, lamp_flag, data_input, None]
        return [1, lamp_flag, None, None]
    elif data_client == 2:
        while True:
            ac_flag = int(input(
                '\nLigar o Ar Condicionado: (1)\nDesligar o Ar Condicionado: (2)\nDefinir temperatura do ar: (3)\nListar configuração atual (4)\nSair(5): '))
            if isinstance(ac_flag, int) and ac_flag in [1, 2, 3, 4]:
                break
        if ac_flag == 3:
            data_input = str(input('Defina a temperatura do ar: '))
            return [2, ac_flag, data_input, None]
        return [2, ac_flag, None, None]


def interface_with_ids(device_ids, unique_ids, option):
    if option == 's' and int(device_ids[0]) == 1:
        return [1, None, None, None]
    if option == 's' and int(device_ids[0]) == 2:
        return [2, None, None, None]
    if int(device_ids[0]) == 1:
        while True:
            if int(device_ids[0]) == 1:
                if unique_ids:
                    id_selected = str(
                        input(f'Selecione uma das IDs de lâmpada: {unique_ids}: '))
                    if id_selected in unique_ids:
                        lamp_flag = int(input(
                            f'\nLigar lâmpada de ID {id_selected}: (1)\nDesligar lâmpada de ID {id_selected}: (2)\nMudar cor de lâmpada de ID {id_selected}: (3)\nListar configuração atual da lâmpada de ID {id_selected}: (4)\nSair (5): '))
                        if isinstance(lamp_flag, int) and lamp_flag in [1, 2, 3, 4]:
                            if lamp_flag == 3:
                                data_input = str(
                                    input('\nDefina a cor da lâmpada: '))
                                return [1, lamp_flag, data_input, id_selected]
                            return [1, lamp_flag, None, id_selected]

    elif int(device_ids[0]) == 2:
        while True:
            if int(device_ids[0]) == 2:
                if unique_ids:
                    id_selected = str(
                        input(f'Selecione uma das IDs de ar condicionado {unique_ids}: '))
                    if id_selected in unique_ids:
                        ac_flag = int(input(
                            f'\nLigar ar condicionado de ID {id_selected}: (1)\nDesligar ar condicionado de ID {id_selected}: (2)\nMudar a temperatura de ar condicionado de ID {id_selected}: (3)\nListar configuração atual do ar condicionado de ID {id_selected}: (4)\nSair (5): '))
                        if isinstance(ac_flag, int) and ac_flag in [1, 2, 3, 4]:
                            if ac_flag == 3:
                                data_input = str(
                                    input('\nDefina a temperatura do ar condicionado: '))
                                return [2, ac_flag, data_input, id_selected]
                            return [2, ac_flag, None, id_selected]


def extract_ids(device_info_string):
    if device_info_string == 'None':
        return None
    device_ids = []
    unique_ids = []

    # Split the string into lines
    lines = device_info_string.split('\n')

    # Iterate over each line and extract device_id and unique_id
    for line in lines:
        if line.strip():  # Check if the line is not empty
            parts = line.split(',')
            device_id = parts[0].split(':')[-1].strip()
            unique_id = parts[1].split(':')[-1].strip()
            option = parts[4].split(':')[-1].strip()

            device_ids.append(device_id)
            unique_ids.append(unique_id)

    return device_ids, unique_ids, option


def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Cliente conectado ao servidor!")

            while True:
                user_data = user_interface()

                client_data = {'CLIENT_LOGIN': user_data[0],
                               'CLIENT_PASS': user_data[1],
                               'CLIENT_DATA': user_data[2],
                               'CLIENT_OPTION': user_data[3]}

                client_json_string = json.dumps(client_data)
                s.send(client_json_string.encode())

                info = s.recv(BUFFER_SIZE)

                info = info.decode('utf-8')
                if info != 'None':
                    print('\nRecebido do servidor: ', info)

                if info == 'Dispositivo não cadastrado!':
                    break

                ids_from_ip = extract_ids(info)
                if not ids_from_ip:
                    ids_from_ip = ['', '', user_data[3]]
                if ids_from_ip[0]:
                    flag = interface_with_ids(
                        ids_from_ip[0], ids_from_ip[1], ids_from_ip[2])
                else:
                    flag = interface(ids_from_ip[2], user_data[2])

                my_obj = {'DEVICE': flag[0],
                          "UNIQUE_ID": flag[3],
                          "OPERATION": flag[1],
                          "DATA": flag[2],
                          'CLIENT_LOGIN': user_data[0],
                          'CLIENT_PASS': user_data[1],
                          'CLIENT_DATA': user_data[2],
                          'CLIENT_OPTION:': user_data[3]}

                # device_json_string = json.dumps(device_obj)
                json_string = json.dumps(my_obj)

                # flag.encode - converte a string para bytes
                s.send(json_string.encode())
                # s.send(device_json_string.encode())

                data = s.recv(BUFFER_SIZE)
                texto_string = data.decode('utf-8')

                print('\nRecebido do servidor: ', texto_string)

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
