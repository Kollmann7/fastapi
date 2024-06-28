import logging
import sys
import os
from dotenv import load_dotenv
from logtail import LogtailHandler
from logging.handlers import SMTPHandler, QueueHandler, QueueListener
import time
import queue


# Charger les variables d'environnement
load_dotenv()

# Obtenir les valeurs des variables d'environnement
token = os.getenv('TOKEN_LOGGER')
smtp_host = os.getenv('SMTP_HOST')
smtp_port = os.getenv('SMTP_PORT')
smtp_username = os.getenv('SMTP_USERNAME')
smtp_password = os.getenv('SMTP_PASSWORD')
smtp_from_addr = os.getenv('SMTP_FROM_ADDR')
smtp_to_addr = os.getenv('SMTP_TO_ADDR')

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handlers
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
logtail_handler = LogtailHandler(source_token=token)

# Formatter
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Ajouter les formatters aux handlers
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logtail_handler.setFormatter(formatter)

# Ajouter les handlers au logger
logger.handlers = [stream_handler, file_handler, logtail_handler]

# Configuration du SMTPHandler
smtp_handler = SMTPHandler(
    mailhost=("smtp.freesmtpserver.com", 587),
    fromaddr="noreply@company.com",
    toaddrs=["admin@company.com"],
    subject='Application Error',
    secure=None
)
smtp_handler.setFormatter(formatter)
# logger.addHandler(smtp_handler)

# create a queue and a queuehandler
log_queue = queue.Queue()
qh = QueueHandler(log_queue)
# add the queuehandler to the logger
logger.addHandler(qh)

listener = QueueListener(log_queue, smtp_handler)



