class TabelaMnemonicos:

    # Retorno o código binário do mnemonico
    def getCodigo(self, mnemonico):
        switcher = {
            "JUMP": "0000",
            "JUMP0": "0001",
            "JUMPN": "0010",
            "ADD": "0011",
            "SUB": "0100",
            "MUL": "0101",
            "DIV": "0110",
            "LOAD": "0111",
            "STORE": "1000",
            "CALL": "1001",
            "RTN": "1100",
            "STOP": "1101"
        }
        retorno = switcher.get(mnemonico)
        if retorno == None:
            return False
        else:
            return retorno
    
    # Retorna o tamanho da instrução em bytes
    def getSize(self, mnemonico):
        switcher = {
            "JUMP": 2,
            "JUMP0": 2,
            "JUMPN": 2,
            "ADD": 2,
            "SUB": 2,
            "MUL": 2,
            "DIV": 2,
            "LOAD": 2,
            "STORE": 2,
            "CALL": 2,
            "RTN": 1,
            "STOP": 1,
            "DB": 1, # Apesar de DB, DW e DA serem pseudoinstruções, elas têm tamanho
            "DW": 2,
            "DA": 2
        }
        retorno = switcher.get(mnemonico)
        if retorno == None:
            return 0
        else:
            return retorno
    
    # Testa se a instrução é pseudo
    def isPseudo(self, mnemonico):
        switcher = {
            "ORG": True,
            "END": True,
            "NAME": True,
            "ENTRY": True,
            "EXTERNAL": True,
            #"CSEG": True,
            #"DSEG": True,
            #"ASEG": True,
            "EQU": True,
            "DB": False,
            "DW": False,
            "DA": False
        }
        retorno = switcher.get(mnemonico)
        if retorno == None:
            return False
        else:
            return retorno

    # Testa se o mnemonico é válido
    def isValido(self, mnemonico):
        switcher = {
            "ORG": True,
            "END": True,
            "DB": True,
            "DW": True,
            "DA": True,
            "NAME": True,
            "ENTRY": True,
            "EXTERNAL": True,
            #"CSEG": True,
            #"DSEG": True,
            #"ASEG": True,
            "JUMP": True,
            "JUMP0": True,
            "JUMPN": True,
            "ADD": True,
            "SUB": True,
            "MUL": True,
            "DIV": True,
            "LOAD": True,
            "STORE": True,
            "CALL": True,
            "RTN": True,
            "STOP": True,
            "EQU": True
        }
        retorno = switcher.get(mnemonico)
        if retorno == None:
            return False
        else:
            return retorno

    # Retorna Verdadeiro se o mnemonico tem operando
    def acceptsOperando(self, mnemonico):
        switcher = {
            "ORG": True,
            "END": True,
            "DB": True,
            "DW": True,
            "DA": True,
            "NAME": True,
            "ENTRY": True,
            "EXTERNAL": True,
            #"CSEG": True,
            #"DSEG": True,
            #"ASEG": True,
            "JUMP": True,
            "JUMP0": True,
            "JUMPN": True,
            "ADD": True,
            "SUB": True,
            "MUL": True,
            "DIV": True,
            "LOAD": True,
            "STORE": True,
            "CALL": True,
            "RTN": False,
            "STOP": False,
            "EQU": True
        }
        retorno = switcher.get(mnemonico)
        if retorno == None:
            return False
        else:
            return retorno
    
    # Retorna verdadeiro se o mnemonico aceita operando simbólico
    def acceptsSymbol(self, mnemonico):
        switcher = {
            "JUMP": True,
            "JUMP0": True,
            "JUMPN": True,
            "ADD": True,
            "SUB": True,
            "MUL": True,
            "DIV": True,
            "LOAD": True,
            "STORE": True,
            "CALL": True,
            "RTN": False,
            "STOP": False,
            "DB": False, # Apesar de DB, DW e DA serem pseudoinstruções, elas têm tamanho
            "DW": False,
            "DA": False
        }
        retorno = switcher.get(mnemonico)
        if retorno == None:
            return False
        else:
            return retorno
