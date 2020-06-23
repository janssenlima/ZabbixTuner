# ZabbixTuner

ZabbixTuner é um projeto que utiliza a API do Zabbix que tem como objetivo verificar uma instalação do Zabbix e propor ajustes para melhorar a performance e a estabilidade do sistema.

Testado e funcionando no Zabbix 5
## Instalação

```sh
$ sudo apt-get install python-pip git

$ git clone https://github.com/janssenlima/ZabbixTuner
$ cd ZabbixTuner
$ sudo pip install -r requirements.txt
```
### Instalação com venv no python3

```sh
$ sudo apt-get install python-pip git

$ git clone https://github.com/janssenlima/ZabbixTuner
$ cd ZabbixTuner
$ python -m venv ./venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ ./ZabbixTuner.py
```

## Configurar parâmetros de conexão do Zabbix

>Inserir URL, usuário e senha de acesso ao Zabbix

```sh
$ vim conf/zabbix.py
```

## Execução

```sh
$ ./ZabbixTuner.py
```

## Quer ajudar no projeto?
Achou algum erro ou quer fazer uma sugestão para o projeto? <br>
Cadastre uma Issue aqui mesmo no GitHub ou envie um e-mail para janssenreislima@gmail.com
