
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


class Telas(ScreenManager):
    pass



class ImageButton(ButtonBehavior, Image):
    pass



class FirstLayout(Screen,ImageButton):

    ListadeDicas = ["Inseto", "Fruta", "Nome", "seleção", "Natureza", "Animal", "Doce", "País",
                    "Time de Futebol", "Banda Musical"]
    ListadePalavras = ["formiga", "morango", "alice", "afeganistao", "chuva", "girafa", "goiabada", "alemanha",
                       "palmeiras",
                       "coldplay"]

    numero = randint(0, len(ListadePalavras) - 1)
    var = 0
    letra = ""
    # Gera os tracinhos para descobrir a palavra
    num = numero
    linha = []
    for i in range(len(ListadePalavras[numero])): linha.append(" _ ")
    path = 'erro0.png'

    def gerar_linhas(self):
        self.linha = []
        for i in range(len(self.ListadePalavras[self.num])): self.linha.append(" _ ")
        return self.linha


    def gerar_numero(self):
        #Gera um numero aleatorio
        numero = randint(0, len(self.ListadePalavras) - 1)
        return numero


    def gera_dica(self):
        #Gera uma dica para o jogo
        dica = self.ListadeDicas[self.num]
        return dica


    def gera_palavra(self):
        # Gera uma palavra para o jogo
        palavra = self.ListadePalavras[self.num]
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



    def identifica_letra(self):
        linha = self.linha
        palavra = self.gera_palavra()
        if self.letra in palavra:
            for i in range(len(palavra)):
                if self.letra == palavra[i]:
                    linha[i] = palavra[i]

        else:
            self.var += 1
        self.ids.box1.text = "Dica: " + self.gera_dica().upper()
        self.ids.box3.text = "".join(linha)
        self.forca()
        if " _ " not in self.linha:
        	self.open_popup()
       
        elif self.var == 6:
            self.open_popup()

    def reinicia_jogo(self):
        self.num = self.gerar_numero()
        self.gerar_linhas()
        self.var = 0
        self.on_pre_enter()


    def restart_game(self):
        self.num = self.gerar_numero()
        self.gerar_linhas()
        self.var = 0
        self.ids.box1.text = "Dica:   " + self.gera_dica().upper()
        self.ids.box3.text = "".join(self.linha)
        self.forca()
        return True



class Menu(Screen):
    pass


class CustomPopup(Popup):
    def __init__(self, FirstLayout, **kwargs):
        super(CustomPopup,self).__init__(**kwargs)
        self.FirstLayout = FirstLayout
        self.title= ''
        if ' _ ' not in self.FirstLayout.linha:
        	self.title = "Você Perdeu, deseja jogar novamente?"
        else: 
            self.title = "Você Venceu, deseja jogar novamente?"
        
    
    def restart(self):
        self.FirstLayout.reinicia_jogo()
        self.FirstLayout.restart_game()
        
class Principal(App):
    def build(self):
        return Telas()

if __name__ == "__main__":
    Principal().run()
