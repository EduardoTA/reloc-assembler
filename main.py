import json
from typing import AsyncIterable

from TabelaSimbolos import TabelaSimbolos
from Linha import Linha as Linha
from TabelaMnemonicos import TabelaMnemonicos as TabelaMnemonicos

def digitosBin(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

def montar():
    nome_arq = str(input("Inserir nome do arquivo com o código: "))
    f = 0
    ci = 0 # Contador de instruções

    linha = Linha()
    tabelaSimbolos = TabelaSimbolos()
    tabelaMnemonicos = TabelaMnemonicos()

    tamanho_instrucao = 0 # Quanto o contador de Instrução deve andar

    nome_programa = '' # Nome do programa
    tamanho_programa = 0 # Tamanho do programa, em bytes

    passo = 1 # Passo do montador

    # Rotina de abertura de arquivo
    try:
        with open(nome_arq) as f:
            f = f.readlines()
    except:
        print("Erro na leitura de arquivo")
        return
    
    codigo_obj = '' # String onde o código objeto será armazenado
    codigo_obj_dados = '' # String auxiliar onde o código objeto de dados será armazenado temporariamente
    c_ext = 0 # Contador de Externals
    origem = 0 # Endereço de origem
    checksum_bloco_dados = 0

    # 1º Passo do Montador
    for passo in range(1,3):
        c_ext = 0
        for linha_arq in f:
            linha_arq = linha_arq.split() # Cada linha é quebrada em átomos
            linha.setLinha(linha_arq) # Carregamos a linha no objeto auxiliar da classe Linha
            
            # A classe auxiliar extrai o rótulo, operador e operando da linha
            rotulo = linha.getRotulo() 
            operador = linha.getOperador()
            operando = linha.getOperando()
            if passo == 1:
                # Se a linha tiver rótulo
                if rotulo:
                    tabelaSimbolos.insertOrUpdate(simbolo=rotulo, endereco=str(ci), resolvido='Resolvido')
                
                # Se a linha conter pseudoinstrução
                if tabelaMnemonicos.isPseudo(operador):
                    if operador == 'NAME':
                        nome_programa = operando
                    elif operador == 'ENTRY':
                        tabelaSimbolos.insertOrUpdate(simbolo=operando, tipoSim='Entry')
                    elif operador == 'EXTERNAL':
                        # Se for 'EXTERNAL', o endereço já nasce resolvido
                        tabelaSimbolos.insertOrUpdate(simbolo=operando, tipoSim='External', endereco=str(c_ext), resolvido='Resolvido')
                        c_ext += 1
                    elif operador == 'ORG':
                        ci = int(operando)
                        origem = int(operando)
                    
                    # Se o programa encontrar essa pesudoinstrução, vai para o 2º passo imediatamente
                    elif operador == 'END':
                        break
                

                # Aqui não teremos problema nas pseudo instruções DB, DW e DA pois as outras pseudoinstruções
                # tem tamanho nulo
                tamanho_instrucao = tabelaMnemonicos.getSize(operador) # O tamanho do passo do contador de instrução (ci) depende do
                                                                       # tamanho da instrução
                
                # Contador de instrução é incrementado de acordo com o tamanho da instrução
                ci += tamanho_instrucao
                tamanho_programa += tamanho_instrucao

            if passo == 2:
                # Se a linha conter pseudoinstrução
                if tabelaMnemonicos.isPseudo(operador):
                    if operador == 'NAME':
                        codigo_obj += ' '+digitosBin(0, 32)
                        # Gerar campos de nome no código-objeto
                        print("\n\nBloco de Nome e Tipo:")
                        checksum = 0 # Começa checksum em 0
                        numero_bytes_bloco = 13
                        checksum -= numero_bytes_bloco

                        tipo_bloco = -1 # Tipo de bloco=-1
                        checksum -= tipo_bloco # Subtrai a contribuição de tipo de bloco no checksum
                        tipo_bloco = digitosBin(tipo_bloco, 8) # Converte tipo de bloco para binário de 1 byte

                        isMain_bloco = 0
                        if nome_programa == '#MAIN' or 'MAIN':
                            checksum -= 1
                            isMain_bloco = digitosBin(1,8)
                        else:
                            checksum -= 0
                            isMain_bloco = digitosBin(0,8)

                        nome_programa_byte_array = bytearray(nome_programa, "utf8")
                        nome_bloco = []
                        for i in range(0, 10):
                            if i < len(nome_programa_byte_array):
                                checksum -= nome_programa_byte_array[i]
                                nome_bloco.append(digitosBin(nome_programa_byte_array[i], 8))
                            else:
                                checksum -= 0
                                nome_bloco.append(digitosBin(0, 8))
                        
                        numero_bytes_bloco = digitosBin(numero_bytes_bloco, 8)

                        checksum = digitosBin(checksum, 8)

                        print("n° de bytes: {0}\ntipo: {1}\nprograma principal: {2}\nnome: {3}\nchecksum: {4}"
                        .format(numero_bytes_bloco, tipo_bloco, isMain_bloco, nome_bloco, checksum))

                        print("------------------")

                        # Inserir campos de nome na fita-objeto
                        codigo_obj += numero_bytes_bloco
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += tipo_bloco
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += isMain_bloco
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += ''.join(nome_bloco)
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += checksum
                    
                    if operador == 'EXTERNAL':
                        codigo_obj += ' '+digitosBin(0, 32)
                        # Gerar bloco de externos
                        print("\nBloco de Externals:")
                        checksum = 0 # Começa checksum em 0
                        numero_bytes_bloco = 14
                        checksum -= numero_bytes_bloco

                        tipo_bloco = -3 # Tipo de bloco=-1
                        checksum -= tipo_bloco # Subtrai a contribuição de tipo de bloco no checksum
                        tipo_bloco = digitosBin(tipo_bloco, 8) # Converte tipo de bloco para binário de 1 byte

                        nome_external_byte_array = bytearray(operando, "utf8")
                        external_bloco = []
                        for i in range(0, 10):
                            if i < len(nome_external_byte_array):
                                checksum -= nome_external_byte_array[i]
                                external_bloco.append(digitosBin(nome_external_byte_array[i], 8))
                            else:
                                checksum -= 0
                                external_bloco.append(digitosBin(0, 8))
                        checksum -= c_ext

                        numero_bytes_bloco = digitosBin(numero_bytes_bloco, 8)

                        checksum = digitosBin(checksum, 8)

                        print("n° de bytes: {0}\ntipo: {1}\nnome: {2}\nc_ext: {3}\nchecksum: {4}"
                        .format(numero_bytes_bloco, tipo_bloco, external_bloco, digitosBin(c_ext, 16), checksum))

                        print("------------------")

                        # Inserir campos de nome na fita-objeto
                        codigo_obj += numero_bytes_bloco
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += tipo_bloco
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += ''.join(external_bloco)
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += digitosBin(c_ext, 16)
                        #print('fita-objeto: '+digitosBin(c_ext, 8))
                        codigo_obj += checksum

                        c_ext += 1 # Incrementa o contador de externals
                    
                    if operador == 'ENTRY':
                        codigo_obj += ' '+digitosBin(0, 32)
                        # Gerar bloco de entries
                        print("\nBloco de Entries:")
                        checksum = 0 # Começa checksum em 0
                        numero_bytes_bloco = 14
                        checksum -= numero_bytes_bloco

                        tipo_bloco = -2 # Tipo de bloco=-1
                        checksum -= tipo_bloco # Subtrai a contribuição de tipo de bloco no checksum
                        tipo_bloco = digitosBin(tipo_bloco, 8) # Converte tipo de bloco para binário de 1 byte

                        nome_entry_byte_array = bytearray(operando, "utf8")
                        entry_bloco = []
                        for i in range(0, 10):
                            if i < len(nome_entry_byte_array):
                                checksum -= nome_entry_byte_array[i]
                                entry_bloco.append(digitosBin(nome_entry_byte_array[i], 8))
                            else:
                                checksum -= 0
                                entry_bloco.append(digitosBin(0, 8))

                        endereco = int(tabelaSimbolos.getTabela()[str(operando)]['endereco'])
                        checksum -= endereco
                        endereco = digitosBin(endereco, 16)

                        numero_bytes_bloco = digitosBin(numero_bytes_bloco, 8)

                        checksum = digitosBin(checksum, 8)

                        print("n° de bytes: {0}\ntipo: {1}\nnome: {2}\nendereco: {3}\nchecksum: {4}"
                        .format(numero_bytes_bloco, tipo_bloco, entry_bloco, endereco, checksum))

                        print("------------------")

                        # Inserir campos de nome na fita-objeto
                        codigo_obj += numero_bytes_bloco
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += tipo_bloco
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += ''.join(entry_bloco)
                        #print('fita-objeto: '+codigo_obj)
                        codigo_obj += endereco
                        #print('fita-objeto: '+digitosBin(c_ext, 8))
                        codigo_obj += checksum
                    
                    if operador == 'ORG' or operador == 'END':
                        if len(codigo_obj_dados) > 0:
                            codigo_obj += ' '+digitosBin(0, 32)
                            numero_bytes_bloco = int(len(codigo_obj_dados)/8) + 3
                            tipo = -4
                            endereco_origem = origem
                            checksum_bloco_dados -= numero_bytes_bloco+tipo+endereco_origem

                            numero_bytes_bloco = digitosBin(numero_bytes_bloco, 8)
                            codigo_obj += numero_bytes_bloco
                            tipo = digitosBin(tipo, 8)
                            codigo_obj += tipo
                            endereco_origem = digitosBin(endereco_origem, 8)
                            codigo_obj += endereco_origem
                            codigo_obj += codigo_obj_dados
                            checksum_bloco_dados = digitosBin(checksum_bloco_dados, 8)
                            codigo_obj += checksum_bloco_dados
                            
                            # Gerar bloco de dados
                            print("\nBloco de Dados:")
                            print("n° de bytes: {0}\ntipo: {1}\nendereço origem: {2}\nconteúdo: {3}\nchecksum: {4}"
                            .format(numero_bytes_bloco, tipo, endereco_origem, codigo_obj_dados, checksum_bloco_dados))

                            print("------------------")

                            codigo_obj_dados = ''
                            checksum_bloco_dados = 0
                            if operador == 'ORG':
                                origem = int(operando)
                    
                    if operador == 'END':
                        codigo_obj += ' '+digitosBin(0, 32)
                        numero_bytes_bloco = 4
                        tipo = -5
                        endereco_origem = origem
                        checksum = numero_bytes_bloco - tipo - endereco_origem
                        codigo_obj += digitosBin(numero_bytes_bloco, 8)
                        codigo_obj += digitosBin(tipo, 8)
                        codigo_obj += digitosBin(endereco_origem, 8)
                        codigo_obj += digitosBin(checksum, 8)

                        # Gerar bloco de fim
                        print("\nBloco de Fim:")
                        print("n° de bytes: {0}\ntipo: {1}\nendereço: {2}\nchecksum: {3}"
                        .format(numero_bytes_bloco, tipo, endereco_origem, checksum))

                        print("------------------")

                        codigo_obj += ' '+digitosBin(0, 32)

                if tabelaMnemonicos.getSize(operador) > 0:
                    Ai = '' # Byte indicador de tamanho de bloco
                    BiCi = '' # 2 bytes com dados
                    if tabelaMnemonicos.acceptsSymbol(operador): # Se o operador aceita simbólico
                        if tabelaMnemonicos.getSize(operador) == 2: # Se a instrução for de 2 bytes
                            Ai = digitosBin(1, 8) # Como a instrução é de 2 bytes, Ai=1
                            BiCi = str(tabelaMnemonicos.getCodigo(operador))+digitosBin(int(tabelaSimbolos.getTabela()[operando]['endereco']), 12)
                            codigo_obj_dados += Ai + BiCi
                        else:
                            Ai = digitosBin(0, 8) # Como a instrução é de 1 byte, Ai=0
                            BiCi = str(tabelaMnemonicos.getCodigo(operador))+digitosBin(0, 4)+'00000000'
                            codigo_obj_dados += Ai + BiCi
                    else:
                        if tabelaMnemonicos.getSize(operador) == 2: # Se a instrução for de 2 bytes
                            Ai = digitosBin(1, 8) # Como a instrução é de 2 bytes, Ai=1
                            BiCi = digitosBin(int(operando), 16)
                            codigo_obj_dados += Ai + BiCi
                        else:
                            if operador == "STOP" or operador == "RTN":
                                Ai = digitosBin(0, 8) # Como a instrução é de 1 byte, Ai=0
                                BiCi = tabelaMnemonicos.getCodigo(operador) + '0000' + '00000000'
                                codigo_obj_dados += Ai + BiCi
                            else:
                                Ai = digitosBin(0, 8) # Como a instrução é de 1 byte, Ai=0
                                BiCi = digitosBin(int(operando), 8) + '00000000'
                                codigo_obj_dados += Ai + BiCi


                        

                    
        #print('operador = '+str(operador)+', tamanho = '+str(tamanho_instrucao))

    print('Nome do programa: {0}\n'.format(nome_programa))
    print('Tabela de Simbolos:\n')
    json_object = json.dumps(tabelaSimbolos.__str__(), indent = 4, sort_keys=False) 
    print(json_object) 
        
    print('fita-objeto: '+codigo_obj)

print("==================")
print("Montador Relocável")
print("==================")

montar()