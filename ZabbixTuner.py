#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__    = "Janssen dos Reis Lima"

from zabbix_api import ZabbixAPI
import os, sys
from termcolor import colored
from conf.zabbix import *

def banner():
    print colored('''
    ______       ______ ______ _____            ________
    ___  /______ ___  /____  /____(_)___  __    ___  __/___  _____________________
    __  / _  __ `/_  __ \_  __ \_  /__  |/_/    __  /  _  / / /_  __ \  _ \_  ___/
    _  /__/ /_/ /_  /_/ /  /_/ /  / __>  <      _  /   / /_/ /_  / / /  __/  /
    /____/\__,_/ /_.___//_.___//_/  /_/|_|      /_/    \__,_/ /_/ /_/\___//_/
    ''', 'red', attrs=['bold'])
    print

try:
    zapi = ZabbixAPI(server=server, path="", log_level=loglevel)
    zapi.login(username, password)
except:
    os.system('clear')
    banner()
    print colored('    Não foi possível conectar ao Zabbix Server.', 'yellow', attrs=['bold'])
    print u"\n    Verifique se a URL " + colored (server, 'red', attrs=['bold']) + u" está disponível."
    print
    print colored('''
    Desenvolvido por Janssen Lima - janssen@conectsys.com.br
    ''', 'blue', attrs=['bold'])
    exit(1)

def menu():
    os.system('clear')
    banner()
    print colored("[+] - Bem-vindo ao ZABBIX TUNER - [+]\n" 
    "[+] - Zabbix Tuner faz um diagnóstico do seu ambiente e propõe melhorias na busca de um melhor desempenho - [+]\n"
    "[+] - Desenvolvido por Janssen Lima - [+]\n"
    "[+] - Dúvidas/Sugestões envie e-mail para janssen@conectsys.com.br - [+]", 'blue')
    print
    print colored("--- Escolha uma opção do menu ---",'yellow', attrs=['bold'])
    print
    print "[1] - Relatório de itens do sistema"
    print "[2] - Listar itens não suportados"
    print "[3] - Desabilitar itens não suportados"
    print "[4] - Relatório da média de coleta dos itens (por tipo)"
    print "[5] - Iniciar diagnóstico"
    print "[6] - Relatório de Agentes Zabbix desatualizados"
    print
    print "[0] - Sair"
    print
    menu_opcao()

def menu_opcao():
    opcao = raw_input( "[+] - Selecione uma opção[0-9]: ")
    if opcao == '1':
        dadosItens()
    elif opcao == '2':
        listagemItensNaoSuportados()
    elif opcao == '3':
        desabilitaItensNaoSuportados()
    elif opcao == '5':
        diagnosticoAmbiente()
    elif opcao == '6':
        agentesDesatualizados()
    elif opcao == '0':
        sys.exit()
    else:
        menu()

def desabilitaItensNaoSuportados():
	opcao = raw_input( "Confirma operação? [s/n]")
	if opcao == 's' or opcao == 'S':
		itens = zapi.item.get({
			"output": "extend",
			"filter": {
				"state": 1
			},
			"monitored": True
		})
		
		for x in itens:
			zapi.item.update({
				"itemid": x['itemid'], "status":1
			})
		print "Itens desabilitados!!!"
		raw_input("Pressione ENTER para continuar")
		main()
	else:
		main()		

def agentesDesatualizados():
    itens = zapi.item.get ({
                            "filter": {"key_": "agent.version"},
                            "output": ["lastvalue", "hostid"],
                            "templated": False,
                            "selectHosts": ["host"],
                            "sortorder": "ASC"
    })
    
    versaoZabbixServer = zapi.item.get ({
                            "filter": {"key_": "agent.version"},
                            "output": ["lastvalue", "hostid"],
                            "hostids": "10084"
    })[0]["lastvalue"]
    
    print colored('{0:6} | {1:30}' .format("Versão","Host"), attrs=['bold'])

    for x in itens:
        if x['lastvalue'] != versaoZabbixServer and x['lastvalue'] <= versaoZabbixServer:
            print '{0:6} | {1:30}'.format(x["lastvalue"], x["hosts"][0]["host"])        
    print ""
    raw_input("Pressione ENTER para continuar")     
    main()
    
def diagnosticoAmbiente():
    print colored("[+++]", 'green'), "analisando itens não númericos"
    itensNaoNumericos = zapi.item.get ({
                                        "output": "extend",
                                        "monitored": True,
                                        "filter": {"value_type": [1, 2, 4]},
                                        "countOutput": True
    })
    print colored("[+++]", 'green'), "analisando itens ICMPPING com histórico acima de 7 dias"
    itensPing = zapi.item.get ({
                                "output": "extend",
                                "monitored": True,
                                "filter": {"key_": "icmpping"},
    })
    
    contPing = 0    
    for x in itensPing:
        if int(x["history"]) > 7:
            contPing += 1
    
    print ""
    print colored("Resultado do diagnóstico:", attrs=['bold'])
    print colored("[INFO]", 'blue'), "Quantidade de itens com chave icmpping armazenando histórico por mais de 7 dias:", contPing
    print colored("[WARN]", 'yellow', None, attrs=['blink']), "Quantidade de itens não numéricos (ativos): ", itensNaoNumericos
    print ""
    raw_input("Pressione ENTER para continuar")     
    main()
        
def listagemItensNaoSuportados():
    itensNaoSuportados = zapi.item.get({"output": ["itemid", "error", "name"],
                              "filter": {"state": 1,"status":0},
                              "monitored": True,
                              "selectHosts": ["hostid", "host"],
                              })

    if itensNaoSuportados:
        print colored('{0:5} | {1:30} | {2:40} | {3:10}' .format("Item","Nome", "Error", "Host"), attrs=['bold'])

        for x in itensNaoSuportados:
            print u'{0:5} | {1:30} | {2:40} | {3:10}'.format(x["itemid"], x["name"], x["error"], x["hosts"][0]["host"])
        print ""
    else:
        print "Não há dados a exibir"
        print ""
    raw_input("Pressione ENTER para continuar")
    main()

def dadosItens():
    itensNaoSuportados = zapi.item.get({"output": "extend",
                              "filter": {"state": 1,"status":0},
                              "monitored": True,
                              "countOutput": True                           
                              })
    
    totalItensHabilitados = zapi.item.get({"output": "extend",
                                         "filter": {"state": 0},
                                         "monitored": True,
                                         "countOutput": True
                                         })

    itensDesabilitados = zapi.item.get({"output": "extend",
                                   "filter": {"status": 1},
                                   "templated": False,
                                   "countOutput": True
                                   })

    itensDescobertos = zapi.item.get({"output": "extend",
                                    "selectItemDiscovery": ["itemid"],
                                    "selectTriggers": ["description"],
                                    "monitored": True
                                    })
                                    
    itensZabbixAgent = zapi.item.get({"output": "extend",
                               "filter": {"type": 0},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensSNMPv1 = zapi.item.get({"output": "extend",
                               "filter": {"type": 1},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensZabbixTrapper = zapi.item.get({"output": "extend",
                               "filter": {"type": 2},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })
                                
    itensChecagemSimples = zapi.item.get({"output": "extend",
                               "filter": {"type": 3},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })                                

    itensSNMPv2 = zapi.item.get({"output": "extend",
                               "filter": {"type": 4},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })
                                
    itensZabbixInterno = zapi.item.get({"output": "extend",
                               "filter": {"type": 5},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensSNMPv3 = zapi.item.get({"output": "extend",
                               "filter": {"type": 6},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensZabbixAgentAtivo = zapi.item.get({"output": "extend",
                               "filter": {"type": 7},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensZabbixAggregate = zapi.item.get({"output": "extend",
                               "filter": {"type": 8},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensWeb = zapi.item.get({"output": "extend",
                               "filter": {"type": 9},
                                "templated": False,
                                "webitems": True,
                                "countOutput": True,
                                "monitored": True
                                })

    itensExterno = zapi.item.get({"output": "extend",
                               "filter": {"type": 10},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensDatabase = zapi.item.get({"output": "extend",
                               "filter": {"type": 11},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensIPMI = zapi.item.get({"output": "extend",
                               "filter": {"type": 12},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensSSH = zapi.item.get({"output": "extend",
                               "filter": {"type": 13},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensTelnet = zapi.item.get({"output": "extend",
                               "filter": {"type": 14},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensCalculado = zapi.item.get({"output": "extend",
                               "filter": {"type": 15},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensJMX = zapi.item.get({"output": "extend",
                               "filter": {"type": 16},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })

    itensSNMPTrap = zapi.item.get({"output": "extend",
                               "filter": {"type": 17},
                                "templated": False,
                                "countOutput": True,
                                "monitored": True
                                })                                
    cont = 0
    for i in itensDescobertos:
        if i["itemDiscovery"]:
            cont += 1

    print ""
    print "Relatório de itens"
    print "=" * 18
    print ""
    print colored("[INFO]",'blue'), "Total de itens: ", int(totalItensHabilitados) + int(itensDesabilitados) + int(itensNaoSuportados)
    print colored("[INFO]",'blue'), "Itens habilitados: ", totalItensHabilitados
    print colored("[INFO]",'blue'), "Itens desabilitados: ", itensDesabilitados
    if itensNaoSuportados > "0":
        print colored("[ERRO]",'red'), "Itens não suportados: ", itensNaoSuportados
    else:
        print colored("[-OK-]",'green'), "Itens não suportados: ", itensNaoSuportados
    #print colored("[INFO]",'blue'), "Itens descobertos: ", cont
    print ""
    print "Itens por tipo em monitoramento"
    print "=" * 14
    print colored("[INFO]",'blue'), "Itens Zabbix Agent (passivo): ", itensZabbixAgent
    print colored("[INFO]",'blue'), "Itens Zabbix Agent (ativo): ", itensZabbixAgentAtivo
    print colored("[INFO]",'blue'), "Itens Zabbix Trapper: ", itensZabbixTrapper
    print colored("[INFO]",'blue'), "Itens Zabbix Interno: ", itensZabbixInterno
    print colored("[INFO]",'blue'), "Itens Zabbix Agregado: ", itensZabbixAggregate
    print colored("[INFO]",'blue'), "Itens SNMPv1: ", itensSNMPv1
    print colored("[INFO]",'blue'), "Itens SNMPv2: ", itensSNMPv2
    print colored("[INFO]",'blue'), "Itens SNMPv3: ", itensSNMPv3
    print colored("[INFO]",'blue'), "Itens SNMNP Trap: ", itensSNMPTrap
    print colored("[INFO]",'blue'), "Itens JMX: ", itensJMX
    print colored("[INFO]",'blue'), "Itens IPMI: ", itensIPMI
    print colored("[INFO]",'blue'), "Itens SSH: ", itensSSH
    print colored("[INFO]",'blue'), "Itens Telnet: ", itensTelnet
    print colored("[INFO]",'blue'), "Itens Web: ", itensWeb
    print colored("[INFO]",'blue'), "Itens Checagem Simples: ", itensChecagemSimples
    print colored("[INFO]",'blue'), "Itens Calculado: ", itensCalculado
    print colored("[INFO]",'blue'), "Itens Checagem Externa: ", itensExterno
    print colored("[INFO]",'blue'), "Itens Database: ", itensDatabase
    print ""
    raw_input("Pressione ENTER para continuar")    
    main()


def main():
    menu()

main()
