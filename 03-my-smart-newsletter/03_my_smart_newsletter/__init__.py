__version__ = '0.1.0'

import openai
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

openai.api_key = "sk-"
openai_model = "text-davinci-002"
url = "https://g1.globo.com/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
articles = soup.find_all("div", class_="feed-post-body")

smtp_server = 'smtp.gmail.com' 
port = 587

#! Preencher as seguintes informações!!!!!
sender_email = ''
password = ''
receiver_email = ''

subject = 'Summary of the article'
msg = MIMEMultipart()
msg['Subject'] = "😨😨 NOTICIAS INSANAS 😨😨 ARRASTA PRA CIMA"
message = "\n"

for article in articles:
    title = article.find("a", class_="feed-post-link")
    where = article.find("span", class_="feed-post-metadata-section")
    excerpt = article.find("div", class_="feed-post-body-resumo")
    prompt = "Gere um resumo desse artigo " + title.text.strip()
    
    response = openai.Completion.create(
        engine=openai_model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=500,
        n = 1,
        stop=None,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )
    
    summary = response.choices[0].text.strip()
    body = 'Resumo gerado:\n' + summary
    message += f"\n 🌟🌟🌟 Titulo da noticia: {title.text.strip()}🌟🌟🌟 \n\n 🌈🌈🌈 {body} 🌈🌈🌈 \n"

body_text = MIMEText(message, 'plain')
msg.attach(body_text)
for i in range(10):
  try:
      server = smtplib.SMTP(smtp_server, port)
      server.starttls()
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, msg.as_string().encode('utf-8'))
      print('Summary sent successfully!')
  except Exception as e:
      print('An error occurred while sending the summary:', e)
  finally:
      server.quit()