import os

from kivy.app import App

from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

import model.VoiceRec as vr
from model.Chatbot import Chatbot
import control.enviarEmail as email

from win10toast import ToastNotifier

import threading
import pickle
import sys

#   MODELO DO BOT
Bot = Chatbot('Max')

def ana():
    toaster = ToastNotifier()
    toaster.show_toast("A.N.A.", "Estou aqui!!!")
    code = ""
    opc = 0
    # frase = ""
    while code != 'tchau':

        try:
            code = vr.myCommand()
            frase = Bot.escuta(code)
            resp, opc = Bot.pensa(frase, opc)
            Bot.fala(resp)
            if resp == 'Adeus!':
                continue
        except:
            pass
    if code == 'tchau':
        App.get_running_app().stop()
        sys.exit(0)


#   TELA INICIAL

class StartScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def tam(self):
        Window.size = (500, 500)

    pass


#   TELA DE CHAT MANUAL

class ChatScreen(Screen):
    opc = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def enviar(self):
        texto = self.ids.msg.text

#       MENSAGEM
        inv = Label(text="Você: " + texto)
        self.ids.conversa.add_widget(inv)

#       ENVIANDO E PROCESSANDO
        frase = Bot.escuta(texto)
        resp, self.opc = Bot.pensa(frase, self.opc)

#       RESPOSTA
        rep = Label(text="A.N.A.: " + resp)
        self.ids.conversa.add_widget(rep)

#       AUTOSCROLL
        self.ids.scroll.scroll_y = 0
        self.ids.msg.text = ""
        self.ids.msg.focus = True

        if frase == 'tchau':
            App.get_running_app().stop()
            sys.exit(0)


    def mudarTamanho(self):
        Window.size = (1000, 773)

    def tam(self):
        Window.size = (500, 500)

    pass


#   TELAS DA EXPLICAÇÃO DOS COMANDOS

class CodeScreen(Screen):
    com = ["Abrir ou fechar", "M\u00FAsica", "Pesquisar", "Conversa", "Digitar", "Enviar e-mail"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add)

    def print_it(self, value, look):
        self.manager.current = look.lower()

    def add(self, *args):
        for c in self.com:
            l = Label(text='[color=fff][ref='+c+']'+c+'[/ref][/color]', markup=True)
            l.bind(on_ref_press=self.print_it)
            self.ids.commands.add_widget(l)
    pass


class AbrirScreen(Screen):

    locais = Bot.locais
    locaisF = Bot.locaisF
    locaisUsados = []

#   VARIÁVEL PRA CHECAR ITERAÇÃO DO LOOP AO VERIFICAR ARQUIVO
    verif = 0
    cont = 0

#   POPUP
    janela = ObjectProperty(None)
    janela2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.listar_progs)

    def listar_progs(self, *args):
        for loc in self.locais:
            for l in self.locaisUsados:

                if loc == l:
                    self.cont = 1
                    break
                else:
                    self.cont = 0

            if self.cont == 0:

                texto = loc.title()
                texto = self.procurar_apelidos(texto)

                lab = Label(text='[color=fff]'+texto+'[/color]\n[color=00c0f0][ref='+loc+']' + self.locais[loc] +
                            '[/ref][/color]', markup=True, halign='center')
                lab.bind(on_ref_press=self.arrumar_caminho)
                self.ids.locais.add_widget(lab)

#   PROCURAR SINÔNIMOS DO PROGRAMA
    def procurar_apelidos(self, texto):
        loc = texto.lower()
        for loc2 in self.locais:
            if self.locais[loc] == self.locais[loc2] and loc != loc2:
                texto = texto + ", " + loc2.title()
                self.locaisUsados.append(loc2)
        return texto

    def window_add_item(self):
        obj = InputDialog(self.janela2)
        obj.open()
        pass

    def add_item(self, text, *args):
        text = text.lower()
        self.locais[text] = ""
        lab = Label(text='[color=fff]' + text + '[/color]\n[color=00c0f0][ref=' + text + ']' + "" +
                         '[/ref][/color]', markup=True, halign='center')
        lab.bind(on_ref_press=self.arrumar_caminho)
        self.ids.locais.add_widget(lab)
        self.arrumar_caminho(lab, text)
#   JANELA DE PROCURAR CAMINHO PARA ALTERAR OU INSERIR NOVO PROGRAMA NA LISTA

    def arrumar_caminho(self, obj, value):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.janela = Popup(title="Destino de: " + value.title(), content=content,
                            size_hint=(0.9, 0.9), id=value)
        self.janela.open()
#       CRIANDO OBJETO PRA MODIFICAR TEXTO DA LABEL
        self.objeto = obj


#   FECHAR JANELA

    def dismiss_popup(self):
        self.janela.dismiss()

    #   ALTERAR CAMINHO

    def load(self, path, filename):
        count_name = 0
        try:
            with open(os.path.join(path, filename[0]), encoding="Latin-1"):
                word = filename[0]
                for letter in filename[0]:
                    if letter == "\\":
                        count_name +=1
                        word = word.replace(letter, "/")

                file_name = word.split("/")
                file_name = file_name[count_name].split(".")
                file_name = file_name[0]
            #   SALVANDO O DICIONÁRIO
                for loc in self.locais:
                    if self.locais[loc] == self.locais[self.janela.id] and loc != self.janela.id:
                        self.locais[loc] = word
                self.locais[self.janela.id] = word
                self.locaisF[self.janela.id] = file_name
                caminho = open("databases/dicionarioLocais.pickle", "wb")
                caminho_f = open("databases/dicionarioLocaisF.pickle", "wb")
                pickle.dump(self.locais, caminho, protocol=0)
                pickle.dump(self.locaisF, caminho_f, protocol=0)
                caminho.close()
                caminho_f.close()
                self.objeto.text = '[color=fff]'+self.procurar_apelidos(self.janela.id.title())+'[/color]\n[color=00c0f0]' \
                                                                                              '[ref='+self.janela.id+']' + \
                                   word + '[/ref][/color]'
                self.dismiss_popup()
        except:
            self.dismiss_popup()

    pass


# JANELA DE PROCURA DE ARQUIVO

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class InputDialog(Popup):
    error = "A lista ser\u00E1 atualizada quando abrir o programa novamente!"
    def __init__(self, parent, *args):
        super(InputDialog, self).__init__()
        self.parent = parent

    def on_error(self, inst, text):
        if text:
            self.lb_error.size_hint_y = 1
            self.size = (400, 150)
        else:
            self.lb_error.size_hint_y = None
            self.lb_error.height = 1
            self.size = (400, 150)

    def _enter(self, tela):
        if not self.text:
            self.error = "Por favor, insira algum nome"
        else:
            self.dismiss()
            tela.add_item(self.text)

    def _cancel(self):
        self.dismiss()


class MusicaScreen(Screen):
    musicaCom = ["Play - [color=fff]Tocar, Toca, Toque[/color]",
                 "Pause  - [color=fff]Pausar, Parar, Pausa, Para, Stop[/color]",
                 "Aumentar - [color=fff]Aumenta, Aumente, Sobe, Suba, Subir, Up[/color]",
                 "Abaixar - [color=fff]Abaixe, Baixar, Diminue, Diminui, Diminua, Diminuir, Down[/color]",
                 "Mutar - [color=fff]Muta, Mute, Silencia, Silêncio, Silenciar[/color]",
                 "Pular - [color=fff]Próxima, Próximo, Pula, Troca, Avançar, Next, Forward, Avança[/color]",
                 "Voltar - [color=fff]Repete, Volta, Volte, Voltar, Anterior, Previews, Back[/color]"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.listar)

    def listar(self, *args):
        for c in self.musicaCom:
            l = Label(text='[color=00c0f0]' + c + '[/color]', markup=True)
            self.ids.listaPlayer.add_widget(l)
    pass


class PesquisarScreen(Screen):
    pass


class ConversarScreen(Screen):
    pass


class DigitarScreen(Screen):
    pass


class EmailScreen(Screen):
    e_mail_hint = email.email
    passw_hint = email.passw

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.status)

    def confirmar(self, *args):
        email.mudar_email(self.ids.email.text, self.ids.passw.text)
        email.email = self.ids.email.text
        email.passw = self.ids.passw.text
        self.status()

    def status(self, *args):
        if email.email == "" and email.passw == "":
            self.ids.status.text = "Status:[color=ff0000] Em espera[/color]"

        if email.email != "" or email.passw != "":
            self.ids.status.text = "Status:[color=0000ff] Parcial[/color]"

        if email.email != "" and email.passw!= "":
            self.ids.status.text = "Status:[color=00ff00] Disponível[/color]"

pass


#   GERAL

class Geral(ScreenManager):
    def __init__(self, **kwargs):

        #       INICIANDO BOT EM UMA THREAD DIFERENTE

        c_thread = threading.Thread(target=ana)
        c_thread.daemon = True
        c_thread.start()
        super().__init__(**kwargs)

    pass


class InterfaceGeral(App):
    def build(self):
        Config.set('graphics', 'width', 1000)
        Config.set('graphics', 'height', 773)
        Config.write()
        Config.set('graphics', 'resizable', False)
        Config.write()
        self.title = "A.N.A. - Assistente de Navegação Artificial"
        self.icon = "./imagens/icoA.png"
        self.sm = Geral()
        self.some_variable = AbrirScreen()
        return self.sm




