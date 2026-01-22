import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def fetch_news():
    urls = [
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}",
        f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API_KEY}"
    ]
    headlines = []
    for url in urls:
        response = requests.get(url).json()
        if response.get("status") == "ok":
            for article in response.get("articles", [])[:5]:
                headlines.append(article.get("title", "No title"))
    return headlines

def create_email_content(headlines):
    today = datetime.now().strftime("%d-%m-%Y")
    content = f"📰 Daily News Digest - {today}\n\n"
    for i, headline in enumerate(headlines, start=1):
        content += f"{i}. {headline}\n"
    return content

def send_email(content):
    msg = MIMEText(content)
    msg["Subject"] = "🌍 Daily News Digest"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

if __name__ == "__main__":
    news = fetch_news()
    if news:
        send_email(create_email_content(news))
        print("Email sent successfully")
