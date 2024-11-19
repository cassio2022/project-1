from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
import pandas as pd
import qrcode
import os
from datetime import datetime

# Tela Inicial
class TelaInicial(MDScreen):
    pass

# Tela de Login
class TelaLogin(MDScreen):
    def validar_login(self):
        usuario = self.ids.entry_usuario.text.strip()
        senha = self.ids.entry_senha.text.strip()

        if usuario and senha:
            if os.path.exists('usuarios.csv'):
                df_usuario = pd.read_csv('usuarios.csv')
                if 'Usuario' in df_usuario.columns and 'Senha' in df_usuario.columns:
                    if usuario in df_usuario['Usuario'].values:
                        senha_cadastrada = df_usuario.loc[df_usuario['Usuario'] == usuario, 'Senha'].values
                        if len(senha_cadastrada) > 0 and str(senha_cadastrada[0]).strip() == senha:
                            Snackbar(text="Login realizado com sucesso!").open()
                            self.manager.current = 'cadastro_animal'
                        else:
                            self.mostrar_popup("Senha inválida.")
                    else:
                        self.mostrar_popup("Usuário não encontrado.")
                else:
                    self.mostrar_popup("Arquivo de usuários inválido.")
            else:
                self.mostrar_popup("Nenhum usuário cadastrado.")
        else:
            self.mostrar_popup("Preencha todos os campos.")

    def mostrar_popup(self, mensagem):
        Snackbar(text=mensagem).open()

# Tela de Cadastro de Usuário
class TelaCadastroUsuario(MDScreen):
    def cadastrar_usuario(self):
        usuario = self.ids.entry_usuario.text.strip()
        senha = self.ids.entry_senha.text.strip()

        if usuario and senha:
            if os.path.exists('usuarios.csv'):
                df_usuario = pd.read_csv('usuarios.csv')
                if usuario in df_usuario['Usuario'].values:
                    Snackbar(text="Usuário já cadastrado.").open()
                    return

            df_usuario = pd.DataFrame({'Usuario': [usuario], 'Senha': [senha]})
            if os.path.exists('usuarios.csv'):
                df_usuario.to_csv('usuarios.csv', mode='a', header=False, index=False)
            else:
                df_usuario.to_csv('usuarios.csv', mode='w', header=True, index=False)

            Snackbar(text="Usuário cadastrado com sucesso!").open()
            self.manager.current = 'cadastro_animal'
        else:
            Snackbar(text="Preencha todos os campos.").open()

# Tela de Cadastro de Animal
class TelaCadastroAnimal(MDScreen):
    vacina_status = "pendente"
    data_cadastro = datetime.now().strftime("%Y-%m-%d")

    def cadastrar_animal(self):
        nome = self.ids.entry_nome.text.strip()
        peso = self.ids.entry_peso.text.strip()
        sexo = self.ids.entry_sexo.text.strip()
        altura = self.ids.entry_altura.text.strip()
        raca = self.ids.entry_raca.text.strip()
        preco = self.ids.entry_preco.text.strip()

        if nome and peso and sexo and altura and raca and preco:
            try:
                preco = float(preco)
            except ValueError:
                Snackbar(text="Insira um valor numérico para o preço.").open()
                return

            df = pd.DataFrame({
                'Nome': [nome],
                'Peso': [peso],
                'Sexo': [sexo],
                'Altura': [altura],
                'Raça': [raca],
                'Vacina': [self.vacina_status],
                'Preço': [preco],
                'Data de Cadastro': [self.data_cadastro]
            })

            if os.path.exists('animais.csv'):
                df.to_csv('animais.csv', mode='a', header=False, index=False)
            else:
                df.to_csv('animais.csv', mode='w', header=True, index=False)

            info_animal = (
                f"Nome: {nome}\nPeso: {peso}\nSexo: {sexo}\nAltura: {altura}\nRaça: {raca}\n"
                f"Vacina: {self.vacina_status}\nPreço: {preco}\nData de Cadastro: {self.data_cadastro}"
            )
            qr = qrcode.make(info_animal)
            qr_filename = f'{nome}_qr.png'
            qr.save(qr_filename)

            Snackbar(text=f"Animal cadastrado com sucesso! QR Code salvo: {qr_filename}").open()
            self.limpar_campos()
        else:
            Snackbar(text="Preencha todos os campos.").open()

    def limpar_campos(self):
        self.ids.entry_nome.text = ""
        self.ids.entry_peso.text = ""
        self.ids.entry_sexo.text = ""
        self.ids.entry_altura.text = ""
        self.ids.entry_raca.text = ""
        self.ids.entry_preco.text = ""

# Tela de Faturamento
class TelaFaturamento(MDScreen):
    def calcular_faturamento_total(self):
        if os.path.exists('animais.csv'):
            df = pd.read_csv('animais.csv')
            if 'Preço' in df.columns:
                faturamento_total = df['Preço'].sum()
                Snackbar(text=f"Faturamento Total: R$ {faturamento_total:.2f}").open()
            else:
                Snackbar(text="Coluna 'Preço' não encontrada.").open()
        else:
            Snackbar(text="Nenhum registro de animais encontrado.").open()

# App Principal
class AnimalApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        sm = ScreenManager()
        sm.add_widget(TelaInicial(name='inicial'))
        sm.add_widget(TelaLogin(name='login'))
        sm.add_widget(TelaCadastroUsuario(name='cadastro_usuario'))
        sm.add_widget(TelaCadastroAnimal(name='cadastro_animal'))
        sm.add_widget(TelaFaturamento(name='faturamento'))
        return sm

if __name__ == '__main__':
    AnimalApp().run()
class AnimalApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("animalapp.kv")
