import logging
import sys
import os
from dotenv import load_dotenv
from logtail import LogtailHandler

# Charger les variables d'environnement
load_dotenv()

# Obtenir les valeurs des variables d'environnement
token = os.getenv('TOKEN_LOGGER')

# Configuration du logger principal
logger = logging.getLogger('main_logger')
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
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.addHandler(logtail_handler)
