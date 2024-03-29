from kivy.app import App
from random import randint
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.button import Button
import re, os



class Telas(ScreenManager):
    pass



class ImageButton(ButtonBehavior, Image):
    pass

class SmoothButton(Button):
    pass

class FirstLayout(Screen,ImageButton, SmoothButton):
    
    #Ler de um arquivo txt as dicas e as palavras e adicionam em uma lista
    font = r'fonts\appleberry.ttf'
    bg_color = (1,1,1,0)
    font_sz = '50dp'
    dicas = open(r"JogodaForca\arquivo_dicas.txt", 'r', encoding='utf-8')
    palavras = open(r"JogodaForca\arquivo_palavras.txt", 'r',encoding='utf-8')
    lista_de_palavras = [re.sub("\n","",i) for i in list(palavras)]
    lista_de_dicas = [re.sub("\n","",i) for i in list(dicas)]

    
    
    #Setando as variaveis auxiliares
    var = 0
    letra = ""
    num = randint(0, len(lista_de_palavras) - 1)
    lista_de_erro = []
    linha = [" _ " for i in range(len(lista_de_palavras[num]))]

    def gerar_linhas(self):
        # Gera os tracinhos para descobrir a palavra
        self.linha = []
        for i in range(len(self.lista_de_palavras[self.num])): self.linha.append(" _ ")
        return self.linha


    def gerar_numero(self):
        #Gera um numero aleatorio
        numero = randint(0, len(self.lista_de_palavras) - 1)
        return numero

    def gera_dica(self):
        #Gera uma dica para o jogo
        dica = self.lista_de_dicas[self.num]
        return dica


    def gera_palavra(self):
        # Gera uma palavra para o jogo
        palavra = self.lista_de_palavras[self.num]
        return palavra.upper()


    def forca(self):
        if self.var == 0:
            self.ids.forca.source = ("forca/erro0.png")
        elif self.var == 1:
            self.ids.forca.source = ("forca/erro1.png")
        elif self.var == 2:
            self.ids.forca.source = ("forca/erro2.png")
        elif self.var == 3:
            self.ids.forca.source = ("forca/erro3.png")
        elif self.var == 4:
            self.ids.forca.source = ("forca/erro4.png")
        elif self.var == 5:
            self.ids.forca.source = ("forca/erro5.png")
        elif self.var == 6:
            self.ids.forca.source = ("forca/erro6.png")


    def on_pre_enter(self, *args):
        self.ids.box1.text = "Dica:   " + self.gera_dica().upper()
        self.ids.box3.text = "".join(self.linha)
        
        self.forca()
        return True

    def open_popup(self):
        pop = CustomPopup(self)
        pop.open()

    def desistir(self):
        sair = Sair_popup(self)
        sair.open()

    def identifica_letra(self):
        linha = self.linha
        palavra = self.gera_palavra()

        if self.letra in self.lista_de_erro:
            return None #Inserir um textbox informando que o usuario já escolheu essa letra

        elif self.letra in palavra:
            for i in range(len(palavra)):
                if self.letra == palavra[i]:
                    linha[i] = " {} ".format(palavra[i])

        else:
            self.lista_de_erro.append(self.letra)
            self.ids[self.letra.lower()].my_color = 1,0,0,1
            # for letra in self.lista_de_erro:
            #     self.ids[letra.lower()].source = "ALPHABET ERRORS/"+ letra.lower() +" - errado.png"
            self.var += 1
        self.ids.box1.text = "Dica: " + self.gera_dica().upper()
        self.ids.box3.text = "".join(linha)
        self.forca()
        
        if self.var >= 6 or " _ " not in self.linha:
            self.open_popup()

        


    def reinicia_jogo(self):
        self.num = self.gerar_numero()
        self.gerar_linhas()
        self.var = 0
        self.on_pre_enter()
        self.lista_de_erro = []
        for id, widget in self.ids.items():
            if isinstance(widget,SmoothButton) == True:
                self.ids[id].my_color = 0,0,0,0
                print("EEEIII")


    def restart_game(self):
        self.num = self.gerar_numero()
        self.gerar_linhas()
        self.var = 0
        self.lista_de_erro = []
        self.ids.box1.text = "Dica:   " + self.gera_dica().upper()
        self.ids.box3.text = "".join(self.linha)
        self.forca()
        for id, widget in self.ids.items():
            if isinstance(widget,SmoothButton) == True:
                self.ids[id].my_color = 0,0,0,0
                print("err")
        return True

    
class Menu(Screen):
    pass

class CustomPopup(Popup):
    def __init__(self, FirstLayout, **kwargs):
        super(CustomPopup,self).__init__(**kwargs)
        self.FirstLayout = FirstLayout
        self.title= ''
        if ' _ ' not in self.FirstLayout.linha:
        	self.title = "Você Venceu :) , deseja jogar novamente?"
        else: 
            self.title = "Você Perdeu :( , deseja jogar novamente?"
    
    def restart(self):
        self.FirstLayout.reinicia_jogo()
        self.FirstLayout.restart_game()

class Sair_popup(Popup):
    def __init__(self, FirstLayout, **kwargs):
        super(Sair_popup,self).__init__(**kwargs)
        self.FirstLayout = FirstLayout
        self.title= 'Deseja Sair?'
        
    def restart(self):
        self.FirstLayout.reinicia_jogo()
        self.FirstLayout.restart_game()

    # def animar(self, popup, *args):
    #     animar = Animation(size_hint=(.2,.8))
    #     animar.start(popup)
        
class Principal(App):
    def build(self):
        return Telas()

if __name__ == "__main__":
    Principal().run()
