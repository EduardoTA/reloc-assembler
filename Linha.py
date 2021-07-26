from TabelaMnemonicos import TabelaMnemonicos

class Linha:
    linha = []
    temRotulo = False
    temOperando = False

    tabelaMnemonicos = TabelaMnemonicos()
    # Este método guarda a linha na classe Linha
    def setLinha(self, linha):
        self.temRotulo = False
        self.linha = linha
    
    # Retorna o rótulo da linha, se houver
    def getRotulo(self):
        if not self.tabelaMnemonicos.isValido(self.linha[0]):
            self.temRotulo = True
            return self.linha[0]
        else:
            self.temRotulo = False
            return False

    # Retorna o operador da linha
    def getOperador(self):
        if self.temRotulo:
            return self.linha[1]
        else:
            print()
            return self.linha[0]
    
    # Retorna operando, se houver
    def getOperando(self):
        if self.tabelaMnemonicos.acceptsOperando(self.getOperador()):
            return self.linha[len(self.linha)-1]
        else:
            return False
    
    def printLinha(self):
        print(self.linha)
