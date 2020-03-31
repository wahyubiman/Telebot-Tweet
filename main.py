import click
import logging
from configobj import ConfigObj
from app.database import first_db_init
from app.telebot import start_telebot


# Create and configure logger
logging.basicConfig(filename="tele.log",
        format='%(asctime)s, %(levelname)s : %(message)s',
        filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

config = ConfigObj("setting.ini")

@click.group()
def cli():
    first_db_init()
    channel = config['main']['channel']
    duration = config['main']['duration']
    if len(channel) == 0:
        print("Please specify channel username for bot to send message in setting.ini")
        exit()

@cli.command()
@click.argument("token", required=True)
def polling(token):
    '''bot mode polling'''
    start_telebot(token)

@cli.command()
@click.argument("token", required=True)
def webhook(token):
    '''bot mode webhook'''
    domain = config['webhook']['domain']
    port = config['webhook']['port']
    cert = config['webhook']['cert']
    if len(domain) == 0:
        print("Please specify domain for receive webhook in setting.ini")
        exit()
    elif len(cert) == 0:
        print("Please specify certificate location in setting.ini")
        exit()
    print(f"Webhook url : https://{domain}/{path}:{port}")
    print(f"Cert location : {cert}")
    start_telebot(token, mode="webhook")


if __name__ == '__main__':
    cli()

