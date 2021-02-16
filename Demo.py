import os
import smtplib
from email.message import EmailMessage

def x():
    Email_Adress = 'andy.btc.profit@gmail.com'
    Email_Password = 'sgijlrmqtkskkabi'

    msg = EmailMessage()
    msg['Subject'] = 'Michaels New Weight!!'
    msg['From'] = Email_Adress
    msg['to'] = 'andy.btc.profit@gmail.com'
    msg.set_content("x")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Email_Adress, Email_Password)
        smtp.send_message(msg)
x()
