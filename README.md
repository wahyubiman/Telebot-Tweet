# Telebot Tweet
---
Scrape tweet from twitter user that contain specific keyword, you can add/delete/view keyword & twitter username inside bot

> this bot only send message to channel provided in setting.ini file, not inside bot it self

---
### Install Dependency
- Clone project & install dependency
```bash
git clone https://github.com/wahyubiman/Telebot-Tweet.git
cd Telebot-Tweet
pip install -r requirements.txt
```
- Edit setting.ini
```bash
[main]
### Telegram channel username with '@' for bot to send message, ex : @ChannelUser
channel = "@tweetairdrop"

### Duration for scraping tweet, ex : m5 for 5 minute or h1 for 1 hour
duration = "m30" # m for minute, h for hour, ex : m30, h6, m45

[webhook]
### domain for receive webhook without http/https, if dont have domain just pass your machine ip, ex : domain.com | 123.456.78.90
domain = "" # my.example.com, example.com or use machine ip 123.456.78.90

### port fot bot to receive webhook, default 7000
port = 7000

### certificate location
cert = ""
```
- Get bot token from [botfather](https://t.me/botfather) or [click here](https://core.telegram.org/bots#6-botfather) for detailed instruction

### Run Bot
```bash
python main.py --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  polling  bot mode polling
  webhook  bot mode webhook
```
---
- Run bot in polling mode
```bash
python main.py polling TOKEN
```
---
- Run bot in webhook mode
Before run bot in webhook mode, please fill requirement field in setting.ini file, or [click this](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks) for detailed instruction how to set webhook

```bash
python main.py webhook TOKEN
```
---

### Extras
- Create self signed certificate using openssl
```bash
openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem
```
- Example nginx config
```
server {
    listen              443 ssl;
    listen              [::]:443 ssl;
    server_name         example.com;
    ssl_certificate     cert.pem;
    ssl_certificate_key private.key;

    location /TOKEN1 {
        proxy_pass http://127.0.0.1:5000/TOKEN1/;
    }

    location /TOKEN2 {
        proxy_pass http://127.0.0.1:5001/TOKEN2/;
    }
}
```
> if you run on aws/gcp enable port 443 in security group
---