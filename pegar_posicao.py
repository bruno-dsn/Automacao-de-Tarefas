# ==========================================
# FERRAMENTA PARA PEGAR COORDENADAS
# Este script ajuda a descobrir as coordenadas X e Y de um ponto na tela
# ==========================================

import pyautogui
import time
import platform

# Detectar qual sistema operacional está sendo usado
sistema = platform.system()
print("Sistema detectado:", sistema)
print()

print("="*50)
print("PEGAR COORDENADAS DO MOUSE")
print("="*50)
print()
print("Voce tem 5 segundos!")
print("Posicione o mouse no campo que deseja obter as coordenadas")
print("(Por exemplo, no primeiro campo do formulario - codigo)")
print()

# Contagem regressiva de 5 segundos
for i in range(5, 0, -1):
    print(i, "...", end="\r")
    time.sleep(1)

print()
print("="*50)

# Pegar a posição atual do mouse
posicao = pyautogui.position()

# Separar as coordenadas X e Y
x = posicao[0]
y = posicao[1]

# Mostrar as coordenadas encontradas
print()
print("COORDENADAS CAPTURADAS:")
print("X =", x)
print("Y =", y)
print()
print("Use essas coordenadas no codigo principal:")
print("CAMPO_X =", x)
print("CAMPO_Y =", y)
print()
print("="*50)
