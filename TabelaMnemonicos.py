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
        try:
            return switcher.get(mnemonico)
        except:
            raise Exception("Mnemonico não está na Tabela de Mnemônicos (ou é pseudoinstrução)")
    
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
            "STOP": 1
        }
        try:
            return switcher.get(mnemonico)
        except:
            raise Exception("Mnemonico não está na Tabela de Mnemônicos (ou é pseudoinstrução)")
    
    # Testa se a instrução é pseudo
    def isPseudo(self, mnemonico):
        switcher = {
            "ORG": True,
            "END": True,
            "DB": True,
            "DW": True,
            "DA": True,
            "NAME": True,
            "ENTRY": True,
            "EXTERNAL": True,
            "CSEG": True,
            "DSEG": True,
            "ASEG": True
        }
        try:
            return switcher.get(mnemonico)
        except:
            return False

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
            "CSEG": True,
            "DSEG": True,
            "ASEG": True,
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
            "STOP": True
        }
        try:
            return switcher.get(mnemonico)
        except:
            return False

    # Testa se o mnemonico tem operando
    def acceptsOperando(self, mnemonico):
        switcher = {
            "ORG": True,
            "END": False,
            "DB": True,
            "DW": True,
            "DA": True,
            "NAME": True,
            "ENTRY": True,
            "EXTERNAL": True,
            "CSEG": True,
            "DSEG": True,
            "ASEG": True,
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
            "STOP": False
        }
        try:
            return switcher.get(mnemonico)
        except:
            return False
