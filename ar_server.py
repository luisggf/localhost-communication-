import csv
import os
import random
import socket
from threading import Thread
import sys
import json
from csv_aux import *

BUFFER_SIZE = 1024


class ArCondicionado:
    def __init__(self):
        self.temperatura = 22  # temperatura inicial
        self.status = False
        self.id = 2
        self.allowed_range = range(15, 30)

    def processar_comando(self, comando, ip, data, unique_id, user):
        """
        Processa comandos para controle de uma lâmpada.

        Parâmetros:
        - comando (int): Número do comando a ser executado.
        - ip (str): Endereço IP do cliente.
        - data (str): Dados associados ao comando.
        - unique_id (int): Identificador único da lâmpada.
        - user (str): Nome do usuário associado à lâmpada.

        Retorna:
        - str: Mensagem de resposta ao comando.
        """
        if comando == 1:
            with open('ar.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)
                for row in rows:
                    if row['ip'] == ip and int(row['unique_id']) == unique_id and user == row['user']:
                        unique = row['unique_id']
                        self.status = row['status']
                        self.temperatura = row['current_config']
                # if str(self.status) == 'True':
                #     return 'Ar Condicionado já está acesa!'
                self.status = True
                self.update_csv(ip, unique_id)
                return f'Ar Condicionado ligado na temperatura padrão: {self.temperatura} / IP: {ip}'

        elif comando == 2:
            with open('ar.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)
                for row in rows:
                    if row['ip'] == ip and int(row['unique_id']) == unique_id:
                        self.status = row['status']
                        self.temperatura = row['current_config']

                if str(self.status) == 'False':
                    return 'Ar Condicionado já está desligado!'
                self.status = False
                self.update_csv(ip, unique_id)
                return 'Ar Condicionado desligado!'

        elif comando == 3:
            with open('ar.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['ip'] == ip and int(row['unique_id']) == unique_id:
                        unique = row['unique_id']
                        self.status = row['status']
                        self.temperatura = row['current_config']

                if str(self.status) == 'False':
                    return 'Não foi possível alterar a temperatura do ar, ele está desligado!'
                if self.temperatura == int(data):
                    return 'A temperatura selecionada já está ativa!'
                if int(data) in self.allowed_range:
                    self.temperatura = int(data)
                    self.update_csv(ip, unique_id)
                    return (f'Temperatura alterada para {self.temperatura} com sucesso!')
                else:
                    return 'Temperatura inválida, por favor tente novamente!'

        elif comando == 4:
            with open('ar.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['ip'] == ip and int(row['unique_id']) == unique_id:
                        self.status = row['status']
                        self.temperatura = row['current_config']
                    if row['ip'] == ip and int(row['unique_id']) == unique_id:
                        return ('Dispositivo: ' + str(row))

        elif comando == 5:
            random_id = random.randint(1, 999)
            return ("Dispositivo: " + self.inicializar_dispositivo(random_id, self.status, self.temperatura, ip, user) + "criado com sucesso!")
        else:
            return 'Comando inválido para o Ar Condicionado!'

    def update_csv(self, ip, unique_id):
        """
        Atualiza o arquivo csv da lâmpada baseado nas informações enviadas e em dados da memória RAM
        Parâmetros:
        - ip (str): Endereço IP do cliente.
        - unique_id (int): Identificador único da lâmpada.
        """
        with open('ar.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            print(row['unique_id'])
            if int(row['unique_id']) == unique_id and ip == row['ip']:
                row['status'] = str(self.status)
                row['current_config'] = self.temperatura
                row['ip'] = ip

        with open('ar.csv', mode='w', newline='') as file:
            fieldnames = ['unique_id', 'status',
                          'current_config', 'ip', 'user']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def inicializar_dispositivo(self, unique_id, default_status, default_temperature, ip, user):
        """
        Inicializa um novo dispositivo de lâmpada com as configurações padrão.

        Parâmetros:
        - unique_id (int): Identificador único do dispositivo.
        - default_status (bool): Status padrão do dispositivo.
        - default_temperature (str): Cor padrão do dispositivo.
        - ip (str): Endereço IP do cliente associado ao dispositivo.
        - user (str): Nome do usuário associado ao dispositivo.

        Retorna:
        - str: Mensagem indicando a inicialização bem-sucedida do dispositivo.
        """
        # Read client_ar.csv
        with open("client_ar.csv", mode='r') as file_client:
            reader_client = csv.DictReader(file_client)
            rows_client = list(reader_client)

        # Find the client in the list based on ip and user
        client = self.find_client(rows_client, ip, user)

        if client:
            # Add the new unique_id to devices_list
            devices_list = eval(
                client['devices_list']) if client['devices_list'] else []
            devices_list.append(unique_id)
            client['devices_list'] = str(devices_list)

            # Update client_ar.csv with the new devices_list
            with open("client_ar.csv", mode='w', newline='') as file_client:
                fieldnames_client = reader_client.fieldnames
                writer_client = csv.DictWriter(
                    file_client, fieldnames=fieldnames_client)
                writer_client.writeheader()
                writer_client.writerows(rows_client)

            # Update ar.csv with the new device
            with open('ar.csv', mode='a', newline='\n') as file:
                writer = csv.DictWriter(
                    file, fieldnames=['unique_id', 'status', 'current_config', 'ip', 'user'])
                writer.writerow({'unique_id': str(unique_id), 'status': str(default_status),
                                'current_config': str(default_temperature), 'ip': str(ip), 'user': str(user)})

            return f'Dispositivo {unique_id} foi inicializado com as configurações padrões para o usuário {user} '

        else:
            return f'Cliente não encontrado para o usuário {user} e IP {ip}'

    def find_client(self, rows, ip, user):
        """
            Encontra um cliente na lista fornecida com base no IP e informações do usuário.

            Parâmetros:
            - rows (list): Lista de dicionários representando informações do cliente.
            - ip (str): Endereço IP do cliente a ser encontrado.
            - user (str): Login de usuário associado ao cliente.

            Retorna:
            - dict ou None: Se um cliente correspondente for encontrado, o dicionário representando o cliente; caso contrário, None.
        """
        for client in rows:
            if client['ip'] == ip and client['user_login'] == user:
                return client
        return None


def check_device_test(ar, ip, user):
    """
    Verifica a existência do dispositivo associado a um usuário e IP específicos.

    Parâmetros:
    - Ar (Ar-Condicionado): Instância da classe ArCondicionado.
    - ip (str): Endereço IP do dispositivo.
    - user (str): Login de usuário associado ao dispositivo.

    Retorna:
    - tuple: Uma tupla contendo uma mensagem informativa e o identificador único do dispositivo.
    """
    with open('client_ar.csv', mode='r') as file_client:
        content_client = csv.DictReader(file_client)
        rows_client = list(content_client)
        clients = {client['user_login'] for client in rows_client}
        with open('ar.csv', mode='r') as file:
            content = csv.DictReader(file)
            rows = list(content)
            devices_ips = {device['ip'] for device in rows}
            client_devc = {client['user'] for client in rows}

            # entende-se que usuario não possui ar ainda, portanto a cria
            if ip not in devices_ips or user not in client_devc:
                unique_id = random.randint(1, 999)
                return ar.inicializar_dispositivo(
                    unique_id, "False", 22, ip, user), unique_id

            elif user in clients:
                for client_row in rows_client:
                    if client_row['user_login'] == user:
                        ar_lists = eval(client_row['devices_list'])
                        return f"Usuário {user} encontrado em nosso sistema! Ar Condicionados associados ao cliente: {ar_lists}", ar_lists
            else:
                print(
                    f"No matching row found for user {user} with IP {ip}")


def on_new_client(clientsocket, addr, ar):
    """
    Lida com uma nova conexão de cliente.

    Parâmetros:
    - clientsocket (socket): Socket do cliente.
    - addr (tuple): Tupla contendo o endereço IP e porta do cliente.
    - Ar (Ar-Condicionado): Instância da classe ArCondicionado.
    """
    try:
        client_ip = addr[0]

        # Define your IP range
        start_ip_range = '192.168.0.0'
        end_ip_range = '192.168.255.255'

        # Check if the client's IP is within the specified range
        if is_ip_in_range(client_ip, start_ip_range, end_ip_range):
            try:
                while True:
                    data = clientsocket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    texto_recebido = data.decode('utf-8')
                    print('recebido do cliente {} na porta {}: {}'.format(
                        addr[0], addr[1], texto_recebido))
                    try:
                        mensagem_json = json.loads(texto_recebido)
                    except json.JSONDecodeError:
                        mensagem_json = {}

                    tipo_dispositivo = mensagem_json.get('DEVICE', '')
                    comando = mensagem_json.get('OPERATION', '')
                    dados = mensagem_json.get('DATA', '')
                    user = mensagem_json.get('CLIENT_LOGIN', '')

                    # caso comando seja 6 servidor lampada será encerrado
                    if comando in [6, -1]:
                        print(
                            'Vai encerrar o socket do cliente {} !'.format(addr[0]))
                        clientsocket.send(str(comando).encode('utf-8'))
                        break
                    ip = addr[0]

                    mensagem, unique_id = check_device_test(ar, ip, user)

                    msg_to_client = [mensagem, unique_id]

                    msg_to_client_json = json.dumps(msg_to_client)

                    clientsocket.send(msg_to_client_json.encode('utf-8'))

                    # resposta
                    unique_id_aswner = (clientsocket.recv(BUFFER_SIZE))
                    try:
                        unique_id_aswner_json = json.loads(unique_id_aswner)
                    except Exception as error:
                        print(
                            "Não foi possivel converter mensagem do servidor em formato JSON: Erro: ", error)
                        mensagem_json = {}

                    unique_id = unique_id_aswner_json
                    resposta = ar.processar_comando(
                        comando, ip, dados, unique_id, user)
                    print(resposta)
                    clientsocket.send(resposta.encode('utf-8'))

            except Exception as error:
                print('Erro: ', error)
                print("Erro na conexão com o cliente!!")
    except:
        print(f"IPv4: {addr[0]} não permitido.")


def is_ip_in_range(ip_address, start_range, end_range):
    ip_int = int(ip_address.replace('.', ''))
    start_int = int(start_range.replace('.', ''))
    end_int = int(end_range.replace('.', ''))

    return start_int <= ip_int <= end_int


def main_ar_server():
    try:
        ar = ArCondicionado()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 20002))
        server_socket.listen()

        print('Aguardando conexões...')
        while True:
            clientsocket, addr = server_socket.accept()
            print('Conectado ao cliente no endereço:', addr)
            t = Thread(target=on_new_client, args=(clientsocket, addr, ar))
            t.start()

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)


if __name__ == "__main__":
    main_ar_server()
