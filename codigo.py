# ==========================================
# AUTOMAÇÃO DE CADASTRO DE PRODUTOS
# Projeto de automação usando PyAutoGUI
# ==========================================

# Importar as bibliotecas necessárias
import pyautogui
import time
import pandas as pd
import pyperclip
import platform
import os

# ==========================
# CONFIGURAÇÃO INICIAL
# ==========================

# Configurar o PyAutoGUI
pyautogui.FAILSAFE = True  # Mover mouse para canto superior esquerdo para parar
pyautogui.PAUSE = 0.3  # Pausa maior para dar tempo do Mac processar

# Detectar qual sistema operacional está sendo usado
sistema_operacional = platform.system()

# Definir qual tecla usar baseado no sistema
# No Mac usa "command", no Windows usa "ctrl"
if sistema_operacional == "Darwin":  # Darwin é o nome do sistema do Mac
    tecla_modificadora = "command"
    e_mac = True
    e_windows = False
elif sistema_operacional == "Windows":
    tecla_modificadora = "ctrl"
    e_mac = False
    e_windows = True
else:
    # Se for Linux ou outro sistema, usa ctrl
    tecla_modificadora = "ctrl"
    e_mac = False
    e_windows = False

print("Sistema detectado:", sistema_operacional)
print("Usando a tecla:", tecla_modificadora)
print("\nATENÇÃO: O script vai começar em 10 segundos!")
print("NÃO mexa no teclado ou mouse durante a execução!")
time.sleep(10)

# ==========================
# ABRIR O NAVEGADOR CHROME
# ==========================

# Tentar abrir o Chrome de diferentes formas dependendo do sistema
if e_mac:
    # No Mac, usa o Spotlight (Command + Space)
    pyautogui.hotkey("command", "space")
    time.sleep(1)
    pyautogui.write("chrome", interval=0.1)
    pyautogui.press("enter")
    time.sleep(6)
elif e_windows:
    # No Windows, usa Win + R para abrir executar
    pyautogui.hotkey("win", "r")
    time.sleep(0.5)
    pyperclip.copy("chrome")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(6)
else:
    # No Linux, tenta Alt + F2
    pyautogui.hotkey("alt", "f2")
    time.sleep(0.5)
    pyperclip.copy("google-chrome")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    time.sleep(6)

# ==========================
# ABRIR O SITE
# ==========================

# Focar na barra de endereço do navegador
if e_mac:
    pyautogui.hotkey("command", "l")
else:
    pyautogui.hotkey("ctrl", "l")

time.sleep(0.5)

# Copiar e colar o endereço do site
url = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"
pyperclip.copy(url)
pyautogui.hotkey(tecla_modificadora, "v")
pyautogui.press("enter")
time.sleep(4)

# ==========================
# COORDENADAS DOS CAMPOS
# ==========================
# Essas coordenadas foram obtidas usando o script pegar_posicao.py
# Você pode ajustar essas coordenadas se necessário

CAMPO_EMAIL_X = 2532
CAMPO_EMAIL_Y = 380
CAMPO_PRODUTO_X = 2524
CAMPO_PRODUTO_Y = 264

# ==========================
# FAZER LOGIN
# ==========================

# Clicar no campo de email
pyautogui.click(x=CAMPO_EMAIL_X, y=CAMPO_EMAIL_Y)
time.sleep(0.5)

# Limpar o campo antes de escrever
pyautogui.hotkey(tecla_modificadora, "a")
time.sleep(0.2)
pyautogui.press("backspace")
time.sleep(0.3)

# Preencher o email usando pyperclip (resolve problema do @)
email = "pythonimpressionador@gmail.com"
pyperclip.copy(email)
pyautogui.hotkey(tecla_modificadora, "v")
time.sleep(0.3)

# Ir para o campo de senha (pressiona Tab)
pyautogui.press("tab")
time.sleep(0.5)

# Limpar o campo de senha
pyautogui.hotkey(tecla_modificadora, "a")
time.sleep(0.2)
pyautogui.press("backspace")
time.sleep(0.3)

# Preencher a senha usando pyperclip
senha = "123456789"
pyperclip.copy(senha)
pyautogui.hotkey(tecla_modificadora, "v")
time.sleep(0.3)

# Clicar em entrar (pressiona Enter)
pyautogui.press("enter")
time.sleep(4)

# ==========================
# LER O ARQUIVO CSV
# ==========================

# Pegar o caminho da pasta onde está o script
pasta_do_script = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(pasta_do_script, "produtos.csv")

# Verificar se o arquivo existe
if not os.path.exists(caminho_csv):
    print("ERRO: Arquivo produtos.csv nao encontrado!")
    print("Certifique-se de que o arquivo esta na mesma pasta do script.")
    exit()

# Ler o arquivo CSV usando pandas
tabela = pd.read_csv(caminho_csv)
total_produtos = len(tabela)
print("CSV importado com sucesso!")
print("Total de produtos:", total_produtos)

# ==========================
# CADASTRAR OS PRODUTOS
# ==========================

print("\nIniciando cadastro de produtos...\n")

# Contadores para saber quantos produtos foram cadastrados
produtos_cadastrados = 0
produtos_com_erro = 0

# Loop para cadastrar cada produto da tabela
for linha in tabela.index:
    
    # Pegar o código do produto para mostrar qual está sendo cadastrado
    codigo_produto = tabela.loc[linha, "codigo"]
    print("Cadastrando produto", produtos_cadastrados + 1, "de", total_produtos, "-", codigo_produto)
    
    # Clicar no campo de produto
    pyautogui.click(x=CAMPO_PRODUTO_X, y=CAMPO_PRODUTO_Y)
    time.sleep(0.2)
    
    # Preencher o código do produto
    pyautogui.hotkey(tecla_modificadora, "a")
    time.sleep(0.05)
    codigo = str(tabela.loc[linha, "codigo"])
    pyperclip.copy(codigo)
    pyautogui.hotkey(tecla_modificadora, "v")
    pyautogui.press("tab")
    time.sleep(0.05)
    
    # Preencher a marca
    pyautogui.hotkey(tecla_modificadora, "a")
    time.sleep(0.05)
    marca = str(tabela.loc[linha, "marca"])
    pyperclip.copy(marca)
    pyautogui.hotkey(tecla_modificadora, "v")
    pyautogui.press("tab")
    time.sleep(0.05)
    
    # Preencher o tipo
    pyautogui.hotkey(tecla_modificadora, "a")
    time.sleep(0.05)
    tipo = str(tabela.loc[linha, "tipo"])
    pyperclip.copy(tipo)
    pyautogui.hotkey(tecla_modificadora, "v")
    pyautogui.press("tab")
    time.sleep(0.05)
    
    # Preencher a categoria
    pyautogui.hotkey(tecla_modificadora, "a")
    time.sleep(0.05)
    categoria = str(tabela.loc[linha, "categoria"])
    pyperclip.copy(categoria)
    pyautogui.hotkey(tecla_modificadora, "v")
    pyautogui.press("tab")
    time.sleep(0.05)
    
    # Preencher o preço unitário
    pyautogui.hotkey(tecla_modificadora, "a")
    time.sleep(0.05)
    preco = str(tabela.loc[linha, "preco_unitario"])
    pyperclip.copy(preco)
    pyautogui.hotkey(tecla_modificadora, "v")
    pyautogui.press("tab")
    time.sleep(0.05)
    
    # Preencher o custo
    pyautogui.hotkey(tecla_modificadora, "a")
    time.sleep(0.05)
    custo = str(tabela.loc[linha, "custo"])
    pyperclip.copy(custo)
    pyautogui.hotkey(tecla_modificadora, "v")
    pyautogui.press("tab")
    time.sleep(0.05)
    
    # Preencher observações (se houver)
    obs = tabela.loc[linha, "obs"]
    # Verificar se a observação não está vazia
    if pd.isna(obs) == False:
        obs_texto = str(obs)
        if obs_texto.strip() != "":
            pyautogui.hotkey(tecla_modificadora, "a")
            time.sleep(0.05)
            pyperclip.copy(obs_texto)
            pyautogui.hotkey(tecla_modificadora, "v")
    
    # Enviar o formulário
    pyautogui.press("tab")
    time.sleep(0.05)
    pyautogui.press("enter")
    time.sleep(0.5)
    
    # Aumentar o contador de produtos cadastrados
    produtos_cadastrados = produtos_cadastrados + 1

# ==========================
# MOSTRAR RESULTADO FINAL
# ==========================

print("\n" + "="*50)
print("CADASTRO CONCLUIDO!")
print("="*50)
print("Produtos cadastrados:", produtos_cadastrados)
if produtos_com_erro > 0:
    print("Produtos com erro:", produtos_com_erro)
print("="*50)
