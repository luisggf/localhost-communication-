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
        verificar_e_criar_arquivo_csv()
        if comando == 5:
            random_id = random.randint(1, 999)
            if not self.check_device(random_id, ip):

                return ("Dispositivo: " + self.inicializar_dispositivo(random_id, self.status, self.color, ip, user) + "criado com sucesso!")
        elif comando == 1:
            with open('ar.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)
                for row in rows:
                    if row['ip'] == ip and int(row['unique_id']) == unique_id and user == row['user']:
                        unique = row['unique_id']
                        self.status = row['status']
                        self.color = row['current_config']
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
                        self.color = row['current_config']

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
                        self.color = row['current_config']

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
                        self.color = row['current_config']
                    if row['ip'] == ip and int(row['unique_id']) == unique_id:
                        return ('Dispositivo: ' + str(row))
        else:
            return 'Comando inválido para o Ar Condicionado!'

    def check_device(self, unique_id, ip):
        with open('ar.csv', mode='r') as file:
            content = csv.DictReader(file)
            rows = list(content)

            for row in rows:
                if row['unique_id'] == unique_id and row['ip'] == ip:
                    return True

            return False

    def update_csv(self, ip, unique_id):
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
        for client in rows:
            if client['ip'] == ip and client['user_login'] == user:
                return client
        return None


def check_device_test(ar, ip, user):
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
    try:
        verificar_e_criar_arquivo_csv()
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
            user = mensagem_json.get('USER_LOGIN', '')

            ip = addr[0]

            mensagem, unique_id = check_device_test(ar, ip, user)

            # if comando in [6, -1]:
            #     print('Vai encerrar o socket do cliente {} !'.format(addr[0]))
            #     clientsocket.send(str(comando).encode('utf-8'))
            #     return

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
    finally:
        clientsocket.close()


def verificar_e_criar_arquivo_csv():
    arquivo_csv = 'ar.csv'

    # checa se arquivo existe no diretorio atual
    if not os.path.exists(arquivo_csv):
        # caso não exista, ele é criado e tem cabeçalho adicionado para evitar errors com a função processar comando
        with open(arquivo_csv, mode='w', newline='') as file:
            fieldnames = ['unique_id', 'status',
                          'current_config', 'ip']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


def main():
    try:
        ar = ArCondicionado()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.3', 20002))
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
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()