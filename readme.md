# README

## Descrição

Este projeto consiste em um sistema de controle de dispositivos de ar condicionado e lâmpadas, onde é possível interagir com esses dispositivos por meio de servidores Python.

O sistema é dividido em três arquivos principais:

### 1. **AR_SERVER.py**

Este arquivo contém a implementação do servidor responsável pelo controle do dispositivo de ar condicionado. O servidor aceita conexões de clientes e processa comandos para ligar, desligar, alterar temperatura e exibir informações sobre o ar condicionado.

### 2. **LAMP_SERVER.py**

Este arquivo contém a implementação do servidor responsável pelo controle do dispositivo de lâmpada. Semelhante ao servidor do ar condicionado, aceita conexões de clientes e processa comandos para ligar, desligar, alterar cor e exibir informações sobre a lâmpada.

### 3. **CSV_AUX.py**

Este arquivo fornece funções auxiliares relacionadas à manipulação de arquivos CSV. Ele contém funções para verificar e criar arquivos CSV para os dispositivos de ar condicionado e lâmpadas.

## Instruções de Uso

### Pré-requisitos

- Python 3.x instalado
- Biblioteca `socket` disponível (já inclusa na biblioteca padrão do Python)

### Execução

1. **AR_SERVER.py**

   Execute o servidor do ar condicionado com o seguinte comando:

   ```bash
   python AR_SERVER.py
   ```

   O servidor ficará ouvindo por conexões na porta `20002`.

2. **LAMP_SERVER.py**

   Execute o servidor da lâmpada com o seguinte comando:

   ```bash
   python LAMP_SERVER.py
   ```

   O servidor da lâmpada ficará ouvindo por conexões na porta `20003`.

3. **TCP_SERVER.py**

   Execute o servidor de gerenciamente de clientes da seguinte forma:

   ```bash
   python TCP_SERVER.py
   ```

   O servidor de clientes ficará ouvindo por conexões na porta `20003`.

### Clientes

Os clientes podem se conectar aos servidores e enviar comandos utilizando o formato JSON. Para isso, primeiramente deve-se configurar o parâmetro global HOST, substituindo-o pelo endereço IPV4 da máquina cliente. Exemplos de comandos possíveis incluem ligar/desligar dispositivos, alterar configurações e exibir informações. Certifique-se de que os clientes são configurados corretamente para se conectar aos servidores e que os servidores estão aguardando contato, ou então a aplicação falhará.

## Estrutura dos Arquivos CSV

Os dados dos dispositivos e clientes são armazenados em arquivos CSV. Os arquivos CSV incluem:

- `ar.csv`: Informações sobre dispositivos de ar condicionado.
- `lamp.csv`: Informações sobre dispositivos de lâmpadas.
- `client.csv`: Informações sobre clientes gerais.
- `client_ar.csv`: Informações específicas para clientes de ar condicionado.
