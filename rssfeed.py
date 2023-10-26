from bs4 import BeautifulSoup
import requests
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def request_call():
    url = requests.get("your_rss_link")

    soup = BeautifulSoup(url.content, features="xml")

    items = soup.find_all("item")

    return items

sent_email = ['']

def send_emails(customers_email, message):
    my_email = "your_email"
    my_password = "your_password"

    # encoding characters like smiley faces
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = customers_email
    msg['Subject'] = "New job on Upwork."

    body = MIMEText(message, 'plain', 'utf-8')
    msg.attach(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, 
                    to_addrs=customers_email, 
                    msg=msg.as_string())


while True:
    # wait 10 seconds until the next call
    time.sleep(5)

    items = request_call()
    
    for item in items[:1]:

        title = item.title.get_text()
        
        if title not in sent_email:
            
            # parse the CDATA content as HTML
            description_html = BeautifulSoup(item.description.text, 'html.parser')

            # find and replace <br> tags in the parsed HTML
            for br in description_html.find_all("br"):
                br.replace_with("\n")
            
            description = description_html
            
            # you can change the string below to whatever you want to get notified for e.g python or bot
            if "scraping" in title.lower():
                # send email
                sent_email.append(title)
                send_emails(customers_email='receivers_email', message=f'Title:\n{title}\n\n\nDescription:\n{description}')
                del sent_email[0]
