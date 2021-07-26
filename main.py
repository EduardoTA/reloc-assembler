import json

from TabelaSimbolos import TabelaSimbolos
from TabelaEquivalencias import TabelaEquivalencias
from Linha import Linha as Linha
from TabelaMnemonicos import TabelaMnemonicos as TabelaMnemonicos

def montar():
    nome_arq = str(input("Inserir nome do arquivo com o código: "))
    f = 0
    base_relocacao = 0 # Valor default de base de relocacao

    linha = Linha()
    tabelaSimbolos = TabelaSimbolos()
    tabelaMnemonicos = TabelaMnemonicos()
    tabelaEquivalencias = TabelaEquivalencias()

    ci_abs = 0 # Contador de Programa Absoluto
    ci_code = 0 # Contador de Programa de Locação de Código
    ci_data = 0 # Contador de Programa de Locação de Dados
    passo = 0 # Quanto o contador de Instrução deve andar

    # Esta variável indica o esquena de endereçamento atual
    # 'Absoluto'
    # 'Dados'
    # 'Codigo'
    enderecamento_atual = 'Codigo' # Default

    nome_programa = '' # Nome do programa

    # Rotina de abertura de arquivo
    try:
        with open(nome_arq) as f:
            f = f.readlines()
    except:
        print("Erro na leitura de arquivo")
        return
    
    # 1º Passo do Montador
    for linha_arq in f:
        linha_arq = linha_arq.split() # Cada linha é quebrada em átomos
        linha.setLinha(linha_arq) # Carregamos a linha no objeto auxiliar da classe Linha
        
        # A classe auxiliar extrai o rótulo, operador e operando da linha
        rotulo = linha.getRotulo() 
        operador = linha.getOperador()
        operando = linha.getOperando()

        # Se a linha tiver rótulo
        if rotulo:
            # Se o rótulo não estiver na tabela, o campo de endereço depende do esquema de endereçamento
            if enderecamento_atual == 'Absoluto':
                tabelaSimbolos.insertOrUpdate(simbolo=rotulo, endereco=str(ci_abs), base=str(base_relocacao), tipoEnd=enderecamento_atual, resolvido='Resolvido')
            elif enderecamento_atual == 'Dados':
                tabelaSimbolos.insertOrUpdate(simbolo=rotulo, endereco=str(ci_data), base=str(base_relocacao), tipoEnd=enderecamento_atual, resolvido='Resolvido')
            else:
                tabelaSimbolos.insertOrUpdate(simbolo=rotulo, endereco=str(ci_code), base=str(base_relocacao), tipoEnd=enderecamento_atual, resolvido='Resolvido')
        
        # Se a linha conter pseudoinstrução
        if tabelaMnemonicos.isPseudo(operador):
            if operador == 'NAME':
                nome_programa = operando
            elif operador == 'EXTERNAL':
                # Se for 'EXTERNAL', o endereço já nasce resolvido
                tabelaSimbolos.insertOrUpdate(simbolo=operando, tipoSim='External', endereco='Nenhum', resolvido='Resolvido')
            elif operador == 'ENTRY':
                tabelaSimbolos.insertOrUpdate(simbolo=operando, tipoSim='Entry')
            elif operador == 'ORG':
                # A insterpretação do operando de "ORG" depende do esquema de endereçamento atual
                if enderecamento_atual == 'Absoluto':
                    ci_abs = operando
                elif enderecamento_atual == 'Dados':
                    ci_data = operando
                else:
                    ci_code = operando
            
            # Se o programa encontrar essa pesudoinstrução, vai para o 2º passo imediatamente
            elif operador == 'END':
                break

            # Essas pseudoinstruções definem o esquema de endereçamento
            elif operador == 'ASEG':
                enderecamento_atual = 'Absoluto'
                base_relocacao = operando
            elif operador == 'DSEG':
                base_relocacao = operando
                enderecamento_atual = 'Dados'
            elif operador == 'CSEG':
                base_relocacao = operando
                enderecamento_atual = 'Codigo'
            
            # Para esta última pseudoinstrução, ela insere ou atualiza a tabela de equivalências
            elif operador == 'EQU':
                tabelaSimbolos.tabela.pop(rotulo)
                tabelaEquivalencias.insertOrUpdate(equivalencia=rotulo, valor=operando)
            
        passo = tabelaMnemonicos.getSize(operador) # O tamanho do passo do contador de instrução (ci) depende do
                                                   # tamanho da instrução
        
        # Contador de instrução é incrementado de acordo com o tamanho da instrução
        # e o esquema de endereçamento
        if enderecamento_atual == 'Absoluto':
            ci_abs += passo
        elif enderecamento_atual == 'Dados':
            ci_data += passo
        else:
            ci_code += passo
        
    print('Nome do programa: {0}\n'.format(nome_programa))
    print('Tabela de Simbolos:\n')
    json_object = json.dumps(tabelaSimbolos.__str__(), indent = 4, sort_keys=False) 
    print(json_object) 
    print('\nTabela de Equivalência:')
    json_object = json.dumps(tabelaEquivalencias.__str__(), indent = 4, sort_keys=False) 
    print(json_object)
    #print(json.dumps(json.loads(tabelaEquivalencias)))
                







print("==================")
print("Montador Relocável")
print("==================")

montar()