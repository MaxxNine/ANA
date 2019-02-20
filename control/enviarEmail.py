import smtplib
import pickle

from control import acessos as acss

get_emails = acss.get_email()
emails = pickle.load(get_emails)
name_destino = ""
email_destino = ""

for em in emails:
    email = em
    passw = emails[em]


def enviar(frase, opc):
    if frase == "cancela":
        return "Cancelado", 0

    if opc == 0:
        return "Qual o nome do destino?", 6

    if opc == 6:
        global name_destino
        name_destino = frase
        return "Qual o e-mail do destino?", 7

    if opc == 7:
        global email_destino
        email_destino = frase
        return "O que devo escrever?", 8

    if opc == 8:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        try:
            mail.login(email, passw)
            mail.sendmail(name_destino, email_destino, frase.encode('utf-8'))
            mail.close()
            return "Enviado", 0

        except:
            return "Parece ter algo errado com algum dos e-mails, por favor, verifique!", 0

    pass


def mudar_email(em, ps):
    acss.set_email(em, ps)
