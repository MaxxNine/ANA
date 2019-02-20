
def aprenda(frase, opc):
    chave = input('Digite a frase: ')
    chave = chave.lower()

    resp = input('Digite a resposta: ')
    self.frases[chave] = resp

    respostas = open("databases/" + self.nome + "Respostas" + '.pickle', 'wb')
    pickle.dump(self.frases, respostas, protocol=0)
    respostas.close()