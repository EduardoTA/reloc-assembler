from TabelaSimbolos import TabelaSimbolos
from Linha import Linha as Linha
from TabelaMnemonicos import TabelaMnemonicos as TabelaMnemonicos

# 1º passo do montador

def montar():
    nome_arq = str(input("Inserir nome do arquivo com o código: "))
    f = 0
    base_relocacao = 0 # Valor default de base de relocacao

    linha = Linha()
    tabelaSimbolos = TabelaSimbolos()
    tabelaMnemonicos = TabelaMnemonicos()

    ci = 0 # Contador de Programa
    nome_programa = '' # Nome do programa

    # Rotina de abertura de arquivo
    try:
        with open(nome_arq) as f:
            f = f.readlines()
    except:
        print("Erro na leitura de arquivo")
        return
    
    for linha_arq in f:
        linha_arq = linha_arq.split()
        linha.setLinha(linha_arq)

        rotulo = linha.getRotulo()
        operador = linha.getOperador()
        operando = linha.getOperando()

        # Se a linha tiver rótulo
        if rotulo:
            # Se o rótulo não estiver na tabela
            if not tabelaSimbolos.inTabela(rotulo):
                tabelaSimbolos.insertOrUpdate(simbolo=rotulo, endereco=str(ci), resolvido='Resolvido')
            else:
                print('Rótulo duplicado')
                return
        if tabelaMnemonicos.isPseudo(operador):
            if operador == 'NAME':
                nome_programa = operando
            elif operador == 'EXTERNAL':
                tabelaSimbolos.insertOrUpdate(simbolo=operando, tipoSim='External', endereco='Nenhum', resolvido='Resolvido')
            elif operador == 'ENTRY':
                tabelaSimbolos.insertOrUpdate(simbolo=operando, tipoSim='Entry')
                pass

        ci += 1
    print('Nome do programa: {0}'.format(nome_programa))
    print(tabelaSimbolos)
                







print("==================")
print("Montador Relocável")
print("==================")

montar()