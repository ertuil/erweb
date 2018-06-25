import sys
sys.path.append('../')
from erweb import erweb_config as app_config

def config_callback_example():
    print('Changing Configuration.')

app_config.add_callback(config_callback_example)

app_config.upload({'SECRET_KEY':'Hello,World'})

app_config.get('SECRET_KEY')

app_config.get('Not Exist',1)

app_config.get('Not Exist')