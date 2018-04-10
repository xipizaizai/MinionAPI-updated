import logging


class Config():
    DEBUG = False
    TESTING = False
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
    DB_URI = '127.0.0.1'
    DATABASE = 'minion'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL = logging.DEBUG
    MONGODB = {
        'name': 'minion',
        'host': '127.0.0.1',
        'port': 27017
    }


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE = 'minion-test',
    MONGODB = {
        'name': 'minion-test',
        'host': 'mongodb://hgao:FEbRA3fXkRvkzuzW@minioncluster-shard-00-00-sddfy.mongodb.net:27017,minioncluster-shard-00-01-sddfy.mongodb.net:27017,minioncluster-shard-00-02-sddfy.mongodb.net:27017/minion-test?ssl=true&replicaSet=MinionCluster-shard-0&authSource=admin',
        'username': 'hgao',
        'password': 'FEbRA3fXkRvkzuzW'
    }

