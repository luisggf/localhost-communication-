import csv
import os
import random


class Lampada:
    def __init__(self):
        # configuracoes padrao
        self.status = False
        self.id = 1
        self.color = 'white'
        self.allowed_colors = ['white', 'red',
                               'green', 'blue',
                               'cyan', 'magenta',
                               'branco', 'vermelho',
                               'amarelo', 'verde',
                               'azul', 'ciano',
                               'yellow', 'laranja', 'orange']

    def processar_comando(self, comando, data, ip, client_option, unique_id):
        verificar_e_criar_arquivo_csv()
        if client_option == 's':
            random_id = random.randint(2, 17)
            if not self.check_device(self.id, random_id, ip):
                return ("Dispositivo: " + self.inicializar_dispositivo(self.id, random_id, self.status, self.color, ip) + "criado com sucesso!")
        if comando == 1:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)
                for row in rows:
                    if row['ip'] == ip and row['unique_id'] == unique_id and self.id == int(row['device_id']):
                        unique = row['unique_id']
                        self.status = row['status']
                        self.color = row['current_config']
                if str(self.status) == 'True':
                    return 'Lâmpada já está acesa!'
                self.status = True
                self.update_csv(ip, unique_id)
                return f'Lâmpada ligada! IP: {ip}'

        elif comando == 2:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)
                for row in rows:
                    if row['ip'] == ip and row['unique_id'] == unique_id and self.id == int(row['device_id']):
                        self.status = row['status']
                        self.color = row['current_config']

                if str(self.status) == 'False':
                    return 'Lâmpada já está desligada!'
                self.status = False
                self.update_csv(ip, unique_id)
                return 'Lâmpada desligada!'

        elif comando == 3:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['ip'] == ip and row['unique_id'] == unique_id and self.id == int(row['device_id']):
                        unique = row['unique_id']
                        self.status = row['status']
                        self.color = row['current_config']

                if str(self.status) == 'False':
                    return 'Não foi possível alterar a cor da lâmpada, ela está desligada!'
                if self.color == data.lower():
                    return 'Cor selecionada já está ativa!'
                if data.lower() in self.allowed_colors:
                    self.color = data.lower()
                    self.update_csv(ip, unique_id)
                    return ('Cor alterada para ' + self.color + ' com sucesso!')
                else:
                    return 'Cor inválida, por favor tente novamente!'

        elif comando == 4:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['ip'] == ip and row['unique_id'] == unique_id and self.id == int(row['device_id']):
                        self.status = row['status']
                        self.color = row['current_config']
                    if int(row['device_id']) == self.id and row['ip'] == ip and row['unique_id'] == unique_id:
                        return ('Dispositivo: ' + str(row))
        else:
            return 'Comando inválido para a lâmpada!'

    def check_device(self, id, unique_id, ip):
        with open('devices.csv', mode='r') as file:
            content = csv.DictReader(file)
            rows = list(content)

            for row in rows:
                if row['device_id'] == id and row['unique_id'] == unique_id and row['ip'] == ip:
                    return True

            return False

    def update_csv(self, ip, unique_id):
        with open('devices.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            if int(row['device_id']) == self.id and int(row['unique_id'] == unique_id) and ip == row['ip']:
                row['device_id'] = self.id
                row['status'] = str(self.status)
                row['current_config'] = self.color
                row['ip'] = ip

        with open('devices.csv', mode='w', newline='') as file:
            fieldnames = ['device_id', 'unique_id', 'status',
                          'current_config', 'ip']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def inicializar_dispositivo(self, device_id, unique_id, default_status, default_color, ip):
        with open('devices.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            default_row = {'device_id': str(device_id), 'unique_id': str(unique_id), 'status': str(default_status),
                           'current_config': str(default_color), 'ip': str(ip)}
            rows.append(default_row)

            with open('devices.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=default_row.keys())
                writer.writerow(default_row)

            return f'Dispositivo {device_id} foi inicializado com as configurações padrões: {default_row}'


class ArCondicionado:
    def __init__(self):
        self.temperatura = 22  # temperatura inicial
        self.status = False
        self.id = 2
        self.allowed_range = range(15, 30)

    def processar_comando(self, comando, data, ip, client_option, unique_id):
        verificar_e_criar_arquivo_csv()
        if client_option == 's':
            random_id = random.randint(2, 17)
            if not self.check_device(self.id, random_id, ip):
                return ("Dispositivo: " + self.inicializar_dispositivo(self.id, random_id, self.status, self.temperatura, ip) + "criado com sucesso!")
        if comando == 1:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['ip'] == ip and row['unique_id'] == unique_id and self.id == int(row['device_id']):
                        unique = row['unique_id']
                        self.status = row['status']
                if str(self.status) == 'True':
                    return 'Ar condicionado já está ligado!'
                self.status = True
                self.update_csv(ip, unique_id)
                return f'Ar condicionado ligado! IP: {ip}'

        elif comando == 2:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['ip'] == ip and row['unique_id'] == unique_id and self.id == int(row['device_id']):
                        unique = row['unique_id']
                        self.status = row['status']

                if str(self.status) == 'False':
                    return 'Ar condicionado já está desligado!'
                self.status = False
                self.update_csv(ip, unique_id)
                return 'Ar condicionado desligado!'

        elif comando == 3:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['ip'] == ip and row['unique_id'] == unique_id and self.id == int(row['device_id']):
                        unique = row['unique_id']
                        self.status = row['status']
                        self.temperatura = row['current_config']

                if str(self.status) == 'False':
                    return 'Não foi possível alterar a temperatura do ar condicionado, ele está desligado!'
                if int(self.temperatura) == int(data):
                    return 'Temperatura selecionada já está ativa!'
                if int(data) in self.allowed_range:
                    self.temperatura = int(data)
                    self.update_csv(ip, unique_id)
                    return ('Temperatura alterada para ' + str(self.temperatura) + ' com sucesso!')
                else:
                    return 'temperatura inválida, por favor tente novamente!'

        elif comando == 4:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if row['device_id'] == str(self.id) and row['ip'] == ip and row['unique_id'] == unique_id:
                        return ('Dispositivo? ' + str(row))
        else:
            return 'Comando inválido para o Ar Condicionado!'

    def check_device(self, id, unique_id, ip):
        with open('devices.csv', mode='r') as file:
            content = csv.DictReader(file)
            rows = list(content)

            for row in rows:
                if row['device_id'] == id and row['unique_id'] == unique_id and row['ip'] == ip:
                    return True
            return False

    def update_csv(self, ip, unique_id):
        with open('devices.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            if int(row['device_id']) == self.id and int(row['unique_id'] == unique_id) and ip == row['ip']:
                row['device_id'] = self.id
                row['status'] = str(self.status)
                row['current_config'] = self.temperatura
                row['ip'] = ip

        with open('devices.csv', mode='w', newline='') as file:
            fieldnames = ['device_id', 'unique_id', 'status',
                          'current_config', 'ip']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def inicializar_dispositivo(self, device_id, unique_id, default_status, default_temperature, ip):
        with open('devices.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            default_row = {'device_id': str(device_id), 'unique_id': str(unique_id), 'status': str(default_status),
                           'current_config': str(default_temperature), 'ip': str(ip)}
            rows.append(default_row)

            with open('devices.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=default_row.keys())
                writer.writerow(default_row)

            return f'Dispositivo {device_id} foi inicializado com as configurações padrões: {default_row}'


def verificar_e_criar_arquivo_csv():
    arquivo_csv = 'devices.csv'

    # checa se arquivo existe no diretorio atual
    if not os.path.exists(arquivo_csv):
        # caso não exista, ele é criado e tem cabeçalho adicionado para evitar errors com a função processar comando
        with open(arquivo_csv, mode='w', newline='') as file:
            fieldnames = ['device_id', 'status',
                          'current_config']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
