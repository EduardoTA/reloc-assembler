class TabelaSimbolos:
    tabela = {}
    # simbolos = [] # Coluna de símbolos
    # tipoSims = [] # Coluna de tipo de símbolo (external, entry point, interno)

    # enderecos = [] # Coluna de endereços
    # resolvidos = [] # Coluna de símbolo resolvido
    
    # Verifica se símbolo já está na tabela
    def inTabela(self, simbolo):
        for i in self.tabela:
            if i == simbolo:
                return True
            else:
                pass
        return False

    # Insere símbolo na tabela, se ele não estiver lá, e atualiza, caso esteja
    def insertOrUpdate(self, **attributes):
        for i in self.tabela:
            if self.tabela[i] == attributes['simbolo']:
                attributes.pop('simbolo')
                for j in attributes:
                    self.tabela[i][j] = attributes[j]
                return
            else:
                pass
        simbolo_novo = attributes['simbolo']
        self.tabela[simbolo_novo] = {}
        attributes.pop('simbolo')
        for j in attributes:
            self.tabela[simbolo_novo][j] = attributes[j]
        return
    
    def __str__(self):
        return 'Tabela de Símbolos:\n'+str(self.tabela)