import pyautogui


def pesquisar(frase, opc):
    if opc == 3:
        pyautogui.hotkey('browsersearch')
        if 'youtube' in frase:
            for i in range(0,5):
                pyautogui.hotkey('tab')
        return "Pode falar", 2
    if opc == 2:
        pyautogui.typewrite(frase)
        pyautogui.hotkey('enter')
        return "Feito", 0

