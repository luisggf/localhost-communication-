import csv


class Lampada:
    def __init__(self):
        # configuracoes padrao
        self.status = False
        self.id = 1
        self.color = 'white'
        self.allowed_colors = ['white', 'red',
                               'green', 'blue', 'cyan', 'magenta']

    def processar_comando(self, comando, data):
        if comando == 1:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                for row in content:
                    if row['device_id'] != 1:
                        continue
                    self.status = row['status']
                if bool(self.status) == True:
                    return 'Lâmpada já está acesa!'
                self.status = True
                self.update_csv('')
                return 'Lâmpada ligada!'
        elif comando == 2:
            with open('devices.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['device_id'] != 1:
                        continue
                    self.status = row['status']
                if bool(self.status) == False:
                    return 'Lâmpada já está desligada!'
                self.status = False
                self.update_csv('')
                return 'Lâmpada desligada!'
        elif comando == 3:
            if not self.status:
                return 'Não foi possível alterar a cor da lâmpada, ela está desligada!'
            if data in self.allowed_colors:
                self.color = data
                self.update_csv(data)

        elif comando == 4:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                # se o arquivo estiver vazio, adiciona uma linha com as configurações atuais do dispositivo
                if not rows:
                    default_row = {'\ndevice_id': str(self.id), 'status': str(
                        self.status), 'modification_spec': '', 'current_config': str(self.color)}
                    rows.append(default_row)
                    with open('devices.csv', mode='a', newline='') as file:
                        writer = csv.DictWriter(
                            file, fieldnames=default_row.keys())
                        writer.writeheader()
                        writer.writerow(default_row)

                for row in rows:
                    if int(row['device_id']) == self.id:
                        return 'Dispositivo: ' + str(row)

        else:
            return 'Comando inválido para a lâmpada!'

    def update_csv(self, modification_spec):
        with open('devices.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            if int(row['device_id']) == self.id:
                row['device_id'] = self.id
                row['status'] = str(self.status)
                row['modification_spec'] = modification_spec
                row['current_config'] = self.color

        with open('devices.csv', mode='w', newline='') as file:
            fieldnames = ['device_id', 'status',
                          'modification_spec', 'current_config']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


class ArCondicionado:
    def __init__(self):
        self.temperatura = 22  # temperatura inicial
        self.status = False
        self.id = 2

    def processar_comando(self, comando, data):
        if comando == 1:
            self.temperatura += 1
            self.update_csv(
                'Temperatura aumentada para {}°C'.format(self.temperatura))
            return 'Temperatura aumentada para {}°C'.format(self.temperatura)
        elif comando == 2:
            self.temperatura -= 1
            self.update_csv(
                'Temperatura abaixada para {}°C'.format(self.temperatura))
            return 'Temperatura abaixada para {}°C'.format(self.temperatura)
        elif comando == 3:
            if not self.status:
                return 'Não foi possível alterar a cor do ar condicionado, ele está desligado!'
        elif comando == 4:
            with open('devices.csv', mode='r') as file:
                content = csv.DictReader(file)
                rows = list(content)

                for row in rows:
                    if int(row['device_id']) == self.id:
                        return ('Dispositivo: ' + row)
        else:
            return 'Comando inválido para o ar-condicionado!'

    def update_csv(self, modification_spec):
        with open('devices.csv', mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        for row in rows:
            if int(row['device_id']) == self.id:
                row['device_id'] = self.id
                row['status'] = str(self.status)
                row['modification_spec'] = modification_spec
                row['last_modification'] = self.temperatura

        with open('devices.csv', mode='w', newline='') as file:
            fieldnames = ['device_id', 'status',
                          'modification_spec', 'current_config']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
