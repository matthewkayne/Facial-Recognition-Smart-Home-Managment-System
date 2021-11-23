import smtplib

def sendData(recipientEmail,recipientData):
    gmail_user = 'ALevelProject1@gmail.com'
    gmail_password = 'Password12!'


    to = [recipientEmail]
    subject = 'Your Private Data'
    body = recipientData

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (gmail_user, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(gmail_user, to, email_text)
        smtp_server.close()
    except Exception as ex:
        print ("Something went wrong….",ex)