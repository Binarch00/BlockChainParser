import logging

DATABASE = {
    "user": 'root',
    "password": '1234567*',
    "host": '127.0.0.1',
    "database": "btc_add"
}

RPC_NODE = {
    "user": "OIDSAHdiasdiosudhasdjoasidjoaiqweoirof",
    "password": "sldkfhsooiAHOIDoIHJSOAKlsdjAOSIDao",
    "server": "127.0.0.1",
    "port": 8332
}



LOGS = {
    "level": logging.DEBUG,
    "file": "parser.log",
    "format": '%(asctime)s - %(filename)s - Line %(lineno)d - %(levelname)s - %(message)s'
}


def setup_logger():
    # create logger
    logger = logging.getLogger('main')
    logger.setLevel(LOGS['level'])
    # create console handler and set level to debug
    ch = logging.FileHandler(LOGS['file'])
    ch.setLevel(LOGS['level'])
    # create formatter
    formatter = logging.Formatter(LOGS['format'])
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


logger = setup_logger()
