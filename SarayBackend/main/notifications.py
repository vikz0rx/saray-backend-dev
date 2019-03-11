import smtplib
import requests

def send_mail(message, user_email):
    EMAIL = 'vikz0rx.test@gmail.com'
    PASSWORD = '123987Zz'

    SERVER = 'smtp.gmail.com'
    PORT = 587

    session = smtplib.SMTP(SERVER, PORT)        
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(EMAIL, PASSWORD)
    session = session

    headers = [
        'From: ' + EMAIL,
        u'Subject: SARAY PHOTOSTUDIO - Уведомление о заказе',
        'To: ' + user_email,
        'MIME-Version: 1.0',
        'Content-Type: text/html'
    ]
    headers = '\r\n'.join(headers)

    return session.sendmail(EMAIL, user_email, headers + '\r\n\r\n' + message)

def send_sms(message, user_phone):
    API = '8BF374E2-915E-C59E-28D3-DA429B13E441'
    
    req = 'https://sms.ru/sms/send?api_id={}&to={}&msg={}'.format(API, user_phone, message)

    return requests.get(req)