import pyautogui
import pyperclip


def digitar(frase, opc):

    if frase == "parar de digitar":
        return "Feito", 0

    if frase == "enviar":
        pyautogui.hotkey("enter")
        return "Enviado", 5

    if opc == 0:
        return "Pode falar", 5

    if opc == 5:
        pyperclip.copy(frase + " ")
        pyautogui.hotkey("ctrl", "v")
        return "", 5




    pass

