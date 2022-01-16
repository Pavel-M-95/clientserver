import logging

logging.basicConfig(
    filename="messenger.log",
    format="%(name)s: %(levelname)-10s %(asctime)s %(message)s",
    level=logging.INFO
)
