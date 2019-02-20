'''
try:
    if self.historico[-1] == 'Olá, qual o seu nome?':
        nome = self.pega_nome(frase)
        frase = self.responde_nome(nome)
        return frase
except IndexError:
    pass


    def pega_nome(self, nome):
        nome = nome.title()
        return nome

#       RECEPCIONAR NOME

    def responde_nome(self, nome):
        if nome in self.conhecidos:
            frase = 'Bem-vindo de volta '
        else:
            frase = 'Muito prazer '
            self.conhecidos.append(nome)
            memoria = open("databases/" + self.nome + "Nomes" + '.json', 'w')
            json.dump(self.conhecidos, memoria)
            memoria.close()

        self.nomeUsuario = nome
        return frase + nome
'''
