# ZabbixTuner

ZabbixTuner é um projeto que utiliza a API do Zabbix que tem como objetivo verificar uma instalação do Zabbix e propor ajustes para melhorar a performance e a estabilidade do sistema.

[![asciicast](http://blog.conectsys.com.br/wp-content/uploads/2016/04/zabbixtuner.png)](https://asciinema.org/a/2ffakm0mxs70i6ipko5jmyt63)

## Instalação

```sh
$ sudo apt-get install pip git

$ git clone https://github.com/janssenlima/ZabbixTuner
$ cd ZabbixTuner
$ sudo pip install -r requirements.txt
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
Cadastre uma Issue aqui mesmo no GitHub ou envie um e-mail para janssen@conectsys.com.br
