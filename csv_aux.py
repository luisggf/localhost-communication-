import random
import os
import csv


def verificar_e_criar_arquivo_csv():
    """
    Caso os arquivos fundamentais não existam, essa função auxiliar os criam com o cabeçalho
    necessário para execução.
    """
    arquivo_csv_ar = 'ar.csv'
    arquivo_csv_lamp = 'lamp.csv'
    arquivo_csv_client_lamp = 'client.csv'
    arquivo_csv_client_ar = 'client_ar.csv'

    # checa se arquivo existe no diretorio atual
    if not os.path.exists(arquivo_csv_ar):
        # caso não exista, ele é criado e tem cabeçalho adicionado para evitar errors com a função processar comando
        with open(arquivo_csv_ar, mode='a', newline='') as file:
            fieldnames = ['unique_id', 'status',
                          'current_config', 'ip', 'user']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists(arquivo_csv_client_ar):
        with open(arquivo_csv_client_ar, mode='a', newline='') as file:
            fieldnames = ['user_login', 'ip', 'devices_list']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists(arquivo_csv_client_lamp):
        with open(arquivo_csv_client_lamp, mode='a', newline='') as file:
            fieldnames = ['user_login', 'ip', 'devices_list']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists(arquivo_csv_lamp):
        with open(arquivo_csv_lamp, mode='a', newline='') as file:
            fieldnames = ['unique_id', 'status',
                          'current_config', 'ip', 'user']

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


def gerar_endereco_ip():
    """
    Gera endereço IPV4 aleatório, atualmente não usado no código, porém pode ser
    útil.
    """
    ip_base = "192.168.{}.{}"
    octeto3 = random.randint(0, 255)
    octeto4 = random.randint(0, 255)
    return ip_base.format(octeto3, octeto4)


def check_client_test(ip, user_login):
    """
    Verifica se um cliente está cadastrado com base no endereço IP e login do usuário e escreve no arquivo de cliente as
    informações relacionadas ao usuário.

    Parâmetros:
    - ip (str): Endereço IP do cliente.
    - user_login (str): Login do usuário associado ao cliente.

    Retorna:
    - Tuple[bool, bool]: Um par de valores booleanos. O primeiro indica se o cliente está cadastrado, e o segundo indica se o usuário está associado ao cliente.
    """
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
    """
    Verifica se um cliente está cadastrado com base no endereço IP e login do usuário e escreve no arquivo de cliente as
    informações relacionadas ao usuário. Essa função existe para separar SmartDevices distintos, porém a função
    check_client_test() funciona de forma análoga a essa.

    Parâmetros:
    - ip (str): Endereço IP do cliente.
    - user_login (str): Login do usuário associado ao cliente.

    Retorna:
    - Tuple[bool, bool]: Um par de valores booleanos. O primeiro indica se o cliente está cadastrado, e o segundo indica se o usuário está associado ao cliente.
    """
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
