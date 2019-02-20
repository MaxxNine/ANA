import pyautogui

pause = ['pausar' 'parar', 'pause', 'pausa', 'para', 'stop']
play = ['play', 'tocar', 'toca', 'toque']
mutar = ['muta', 'mute', 'silencia', 'silêncio', 'silenciar']
aumentar = ['aumenta', 'aumentar', 'aumente', 'sobe', 'suba', 'subir', 'up']
tanto = ['bastante', 'pouco', 'tudo', 'mais ou menos', 'médio']
diminuir = ['abaixar', 'abaixe', 'baixar', 'diminue', 'diminui', 'diminua', 'diminuir', 'down']
proxima = ['pular', 'próxima', 'próximo', 'pula', 'troca', 'avançar', 'next', 'forward', 'avança']
anterior = ['repete', 'volta', 'volte', 'voltar', 'anterior', 'previews', 'back']

def do_something_at_spotify(frase):

    for ps in pause:
        if ps in frase:
            pyautogui.hotkey('playpause')
            return "", 1

    for pl in play:
        if pl in frase:
            pyautogui.hotkey('playpause')
            return "", 1

    for prox in proxima:
        if prox in frase:
            if 'tudo' in frase:
                for i in range (0, 10):
                    pyautogui.hotkey('nexttrack')
            else:
                pyautogui.hotkey('nexttrack')
            return "", 1

    for ant in anterior:
        if ant in frase:
            if 'tudo' in frase:
                for i in range (0, 10):
                    pyautogui.hotkey('prevtrack')
            else:
                if ant == 'repete' or ant == 'de novo':
                    pyautogui.hotkey('prevtrack')
                else:
                    for i in range(0, 2):
                        pyautogui.hotkey('prevtrack')
            return "", 1

    for aum in aumentar:
        if aum in frase:
            contador = quantidade(frase)
            while contador >= 0:
                pyautogui.hotkey('volumeup')
                contador -= 1
            return "", 1

    for dim in diminuir:
        if dim in frase:
            contador = quantidade(frase)
            while contador >= 0:
                pyautogui.hotkey('volumedown')
                contador -= 1
            return "", 1

    for mt in mutar:
        if mt in frase:
            pyautogui.hotkey('volumemute')
            return "mutado", 1

    if "sair" == frase:
        return "Pronto!", 0

    return "", 1


def quantidade(frase):
    qnt = 10
    for tnt in tanto:
        if tnt in frase:
            if tnt == 'bastante':
                qnt = 25
            elif tnt == 'pouco':
                qnt = 5
            elif tnt == 'tudo':
                qnt = 50
            elif tnt == 'mais ou menos' or tnt == 'médio':
                qnt = 12
    return qnt
