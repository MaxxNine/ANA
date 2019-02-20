import json
import pickle


def get_nomes(nome):
    try:
        memoria = open("databases/" + nome + "Nomes" + '.json', 'r')
    except FileNotFoundError:
        memoria = open("databases/" + nome + "Nomes" + '.json', 'w')
        memoria.write('["Will","Alfredo"]')
        memoria.close()
        memoria = open("databases/" + nome + "Nomes" + '.json', 'r')

    return memoria


def get_locais():
    try:
        locais = open("databases/dicionarioLocais.pickle", 'rb')
    except FileNotFoundError:

        locais = open("databases/dicionarioLocais.pickle", 'wb')
        pickle.dump(({'notepad': 'notepad', 'youtube': 'www.youtube.com' ,
                      'chrome' : 'chrome', 'steam': 'steam'}), locais)
        locais.close()
        locais = open("databases/dicionarioLocais.pickle", 'rb')

    return locais

def get_locaisF():
    try:
        locais = open("databases/dicionarioLocaisF.pickle", 'rb')
    except FileNotFoundError:

        locais = open("databases/dicionarioLocaisF.pickle", 'wb')
        pickle.dump(({'notepad': 'notepad', 'bloco': 'notepad' ,
                      'chrome': 'chrome', 'bloco de notas': 'notepad'}), locais)
        locais.close()
        locais = open("databases/dicionarioLocaisF.pickle", 'rb')

    return locais

def get_respostas(nome):
    try:
        respostas = open("databases/" + nome + "Respostas" + '.pickle', 'rb')
    except FileNotFoundError:
        respostas = open("databases/" + nome + "Respostas" + '.pickle', 'wb')
        pickle.dump(({'oi': 'Olá, qual o seu nome?', 'tchau': 'Adeus!',
                      'ana, qual é o seu segundo nome?': 'Sou conhecida por ser Amável!'}), respostas)
        respostas.close()
        respostas = open("databases/" + nome + "Respostas" + '.pickle', 'rb')

    return respostas


def get_comandos(nome):
    try:
        comandos = open("databases/" + nome + "Comandos" + '.json', 'r')
    except FileNotFoundError:
        comandos = open("databases/" + nome + "Comandos" + '.json', 'w')
        comandos.write('["abrir","abra","execute","abra","open","executa","executar"]')
        comandos.close()
        comandos = open("databases/" + nome + "Comandos" + '.json', 'r')

    return comandos


def get_comandosF(nome):
    try:
        comandos = open("databases/" + nome + "ComandosF" + '.json', 'r')
    except FileNotFoundError:
        comandos = open("databases/" + nome + "ComandosF" + '.json', 'w')
        comandos.write('["fechar","feche","close","fecha"]')
        comandos.close()
        comandos = open("databases/" + nome + "ComandosF" + '.json', 'r')

    return comandos


def get_email():
    try:
        email = open("databases/emails.pickle", 'rb')
    except FileNotFoundError:
        email = open("databases/emails.pickle", 'wb')
        pickle.dump(({"": ""}), email)
        email.close()
        email = open("databases/emails.pickle", 'rb')

    return email


def set_email(e_mail, senha):
    try:
        email = open("databases/emails.pickle", 'wb')
        pickle.dump(({e_mail: senha}), email)
        email.close()
    except:
        return "não encontrado"
