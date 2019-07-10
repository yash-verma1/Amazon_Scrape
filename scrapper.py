# Imports
import requests
from bs4 import BeautifulSoup
import smtplib
import config

# URL I want to check price difference for
url = 'https://www.amazon.in/Logitech-MK345-Wireless-Keyboard-Mouse/dp/B00PFFCMV0/ref=sr_1_3?keywords=logitech+mk&qid=1562687938&s=gateway&sr=8-3'

# User agent
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0"}


def price_check():
    # Loading web page
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    # prettify() gets the entire web page
    # print(soup.prettify())

    # Product title
    title = soup.find(id='productTitle').get_text().strip()

    # Debugging
    print(title)

    # Product price, in string format
    price = soup.find(id='priceblock_ourprice').get_text()
    price = price.replace(',', '')
    # Converting price into float without the rupee symbol
    num_price = float(price[2:7])

    # Debugging
    print(num_price)

    if num_price < 2000:
        send_mail()


def send_mail():
    # Defining server for Gmail for a TLS connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Server user credentials
    username = config.login['username']
    password = config.login['password']
    server.login(username, password)

    # Mail body
    subject = 'Price fell down'
    body = 'Check Amazon Link : ' + url
    msg = f"Subject: {subject}\n\n{body}"

    # Sending email
    to_email = config.emails['to']
    from_email = config.emails['from']

    server.sendmail(
        from_email,
        to_email,
        msg
    )

    # Debugging message
    print("An email has been sent!")

    # End server connection
    server.quit()


price_check()
