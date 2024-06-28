import logging
from logging.handlers import SMTPHandler, QueueHandler, QueueListener
import queue

# Charger les variables d'environnement




# Configuration du logger SMTP
smtp_logger = logging.getLogger('smtp_logger')
smtp_logger.setLevel(logging.ERROR)

# Configuration du SMTPHandler
smtp_handler = SMTPHandler(
    mailhost=("smtp.freesmtpserver.com", int(587)),
    fromaddr="noreply@company.com",
    toaddrs=["admin@company.com"],
    subject='Application Error',
    secure= None
)
formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
smtp_handler.setFormatter(formatter)

# Créer une queue et un queuehandler
log_queue = queue.Queue()
qh = QueueHandler(log_queue)

# Ajouter le queuehandler au logger
smtp_logger.addHandler(qh)

# Créer un QueueListener pour écouter les messages de la queue et les envoyer via SMTPHandler
listener = QueueListener(log_queue, smtp_handler)
listener.start()
