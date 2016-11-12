import poplib
import smtplib
import urllib.request
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EXTERNAL_IP_URL = 'http://checkip.dyndns.org/'
APP_ENCODING = 'utf-8'
CUBIETRUCK_MAIL_USER = 'cubietruckVG@gmail.com'
CUBIETRUCK_MAIL_PASS = 'cubietruckq2w3e4'

emailFrom = ''
emailTo = ''
sendMail = 0
messages = []


def get_external_ip():
    site = urllib.request.urlopen(urllib.request.Request(EXTERNAL_IP_URL)).read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site.decode(APP_ENCODING))
    address = grab[0]
    return address

pop_conn = poplib.POP3_SSL('pop.gmail.com')
pop_conn.user(CUBIETRUCK_MAIL_USER)
pop_conn.pass_(CUBIETRUCK_MAIL_PASS)


for i in range(1, len(pop_conn.list()[1]) + 1):
    messages.append(pop_conn.retr(i))

for message in messages:
    for element in message[1]:
        elementDecoded = element.decode(APP_ENCODING)
        if 'From:' in elementDecoded:
            emailFrom = elementDecoded.split(':')[1].split('<')[1][:-1].strip()
        elif 'Subject:' in elementDecoded:
            emailTo = elementDecoded.split(':')[1].strip()
            if 'ip request' in emailTo.lower():
                sendMail = 1


if sendMail == 1:
    fromaddr = CUBIETRUCK_MAIL_USER
    toaddr = emailTo
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Cubietruck public IP'

    body = get_external_ip()
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, CUBIETRUCK_MAIL_PASS)
    text = msg.as_string()
    server.sendmail(fromaddr, emailFrom, text)
    server.quit()

pop_conn.quit()



