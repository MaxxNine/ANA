from gtts import gTTS
from pygame import mixer
from random import randint
import control.acessos as acessos
import control.spotifyConnect as sptfy
import control.browserSearch as pesquisar
import control.modoDigitar as digitar
import control.enviarEmail as email
import json
import pickle
import subprocess
import os


class Chatbot():

    def __init__(self, nome):

        memoria = acessos.get_nomes(nome)
        comandos = acessos.get_comandos(nome)
        comandosF = acessos.get_comandosF(nome)
        respostas = acessos.get_respostas(nome)
        locais = acessos.get_locais()
        locaisF = acessos.get_locaisF()

        self.locais = pickle.load(locais)
        self.locaisF = pickle.load(locaisF)
        self.comandosF = json.load(comandosF)
        self.conhecidos = json.load(memoria)
        self.comandos = json.load(comandos)
        self.frases = pickle.load(respostas)

        self.nome = nome
        self.nomeUsuario = ""
        self.historico = []
        self.lastPerg = ""

    def escuta(self, frase):
        # frase = input("-> ")
        frase = frase.lower()
        return frase

    def pensa(self, frase, opc):

        # IDENTIFICAR COMANDO

        if opc == 1:
            return sptfy.do_something_at_spotify(frase)

        if opc == 2:
            return pesquisar.pesquisar(frase, opc)

        if opc == 3 or opc == 4:
            return self.aprenda(frase, opc)

        if opc == 5:
            return digitar.digitar(frase, opc)

        if opc == 6 or opc == 7 or opc == 8:
            return email.enviar(frase, opc)

        if 'música' in frase:
            return sptfy.do_something_at_spotify(frase)

        if 'pesquisar' in frase:
            opc = 3
            return pesquisar.pesquisar(frase, opc)

        if frase == "enviar email":
            return email.enviar(frase, opc)

        if frase == 'digitar':
            return digitar.digitar(frase, opc)

        msg = self.pegar_comando(frase)

        # ENSINAR RESPOSTAS

        if frase == 'aprenda':
            return 'Por favor, diga qual será a frase que servirá de gatilho!', 3

        if frase == "mostrar lista":
            for local in self.locais:
                    print(local.title())
            return "Isto é tudo!", 0

        if frase == "desligar computador":
            os.system('shutdown -s -t 00')

        # RESPONDER FRASE
        elif frase in self.frases:
            if frase == 'oi' and self.nomeUsuario != "":
                rep = 'Olá ' + str(self.nomeUsuario)
                return rep, 0
            else:
                return self.frases[frase], 0


        try:
            resp = eval(frase)
            return str(resp), 0
        except:
            pass

        if 'durma' == frase:
            return 'dormi', 1

        if "tchau".find(frase) == -1:
            pass
        else:
            return "Adeus!", 0

        return msg, 0

#       APRENDER NOVA INTERAÇÃO

    def aprenda(self, frase, opc):
        if opc == 3:
            frase = frase.lower()
            self.lastPerg = frase
            return "Diga agora, qual deverá ser a minha resposta", 4

        if opc == 4:
            self.frases[self.lastPerg] = frase
            respostas = open("databases/" + self.nome + "Respostas" + '.pickle', 'wb')
            pickle.dump(self.frases, respostas, protocol=0)
            respostas.close()
            return "Interação aprendida!", 0

#       VOZ DA A.N.A.

    def fala(self, frase):
        print("A.N.A.: " + frase)
        talkToMe(frase)
        self.historico.append(frase)


#       SELECIONAR COMANDO

    def pegar_comando(self, frase):
        for comando in self.comandos:
            if frase.find(comando) == -1:
                pass
            else:
                for local in self.locais:
                    if frase.find(local) == -1:
                        pass
                    else:
                        os.startfile(str(self.locais[local]))
                        return "Aberto"
                return "Abre o quê?"

        for comando in self.comandosF:
            if frase.find(comando) == -1:
                pass
            else:
                for local in self.locaisF:
                    if frase.find(local) == -1:
                        pass
                    else:
                        try:
                            DETACHED_PROCESS = 0x00000008
                            subprocess.call('TASKKILL /F /IM ' + str(self.locaisF[local])
                                            + ".exe", creationflags=DETACHED_PROCESS)
                            return "Fechei"
                        except:
                            return "Não há nenhum processo com esse nome"
                return "Fechar o quê?"

        return "Não entendi"

#       FAZER VOZ


def talkToMe(audio):
    tts = gTTS(text=audio, lang='pt-br')
    r1 = randint(1, 10000000)
    r2 = randint(1, 10000000)
    randfile = str(r2) + "audionumber" + str(r1) + ".mp3"
    tts.save("./audios/"+randfile)
    mixer.init()
    mixer.music.load("./audios/" + randfile)
    mixer.music.play()
    while mixer.music.get_busy():  # check if the file is playing
        pass
    os.remove("./audios" + randfile)
