class TabelaEquivalencias:
    tabela = {}
    
    # Verifica se equivalência já está na tabela
    def inTabela(self, equivalencia):
        for i in self.tabela:
            if i == equivalencia:
                return True
            else:
                pass
        return False

    # Insere equivalência na tabela, se ele não estiver lá, e atualiza, caso esteja
    def insertOrUpdate(self, **attributes):
        for i in self.tabela:
            if i == attributes['equivalencia']:
                attributes.pop('equivalencia')
                for j in attributes:
                    self.tabela[i][j] = attributes[j]
                return
            else:
                pass
        equivalencia_nova = attributes['equivalencia']
        self.tabela[equivalencia_nova] = {}
        attributes.pop('equivalencia')
        for j in attributes:
            self.tabela[equivalencia_nova][j] = attributes[j]
        return
    
    
    def __str__(self):
        return self.tabela