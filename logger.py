import logging
import sys
import os
from dotenv import load_dotenv
from logtail import LogtailHandler

load_dotenv()

token = os.getenv('TOKEN_LOGGER')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
better_handler = LogtailHandler(source_token=token, )

formatter = logging.Formatter(fmt ='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [handler, file_handler, better_handler]

