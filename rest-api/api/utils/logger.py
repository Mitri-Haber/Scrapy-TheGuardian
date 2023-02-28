import logging

logging_context='articles'

logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} - {levelname:<8} # {message}",
    style='{',
    filename='{}.log'.format(logging_context),
    filemode='a',
    )

logger = logging.getLogger('{}-logging'.format(logging_context))