from requests import Session, exceptions

from shinken.basemodule import BaseModule
from shinken.log import logger

properties = {
    'daemons': ['broker'],
    'type': 'http',
    'external': False,
    'phases': ['running'],
}


def get_instance(plugin):
    name = plugin.get_name()
    logger.info("Get a Syslog broker for plugin %s" % (name))

    # defaults
    endpoint = 'http://localhost:8080'
    key = None
    environment = 'Production'
    customer = None

    # Get configuration values, if any
    if hasattr(plugin, 'endpoint'):
        endpoint = plugin.endpoint
    if hasattr(plugin, 'key'):
        key = plugin.key

    instance = Syslog_broker(plugin, endpoint, key, environment=environment, customer=customer, debug=True)
    return instance


class Syslog_broker(BaseModule):

    def __init__(self, modconf, endpoint=None, key=None, environment=None, customer=None, debug=False):

        self.name = 'Alerta Module'
        self.endpoint = endpoint

        self.headers = {
            'X-API-Key': key,
            'Content-Type': 'application/json'
        }
        self.session = Session()

        self.environment = environment
        self.customer = customer

        self.debug = debug

        BaseModule.__init__(self, modconf)

    def manage_log_brok(self, b):

        if self.debug:
            print(b)
        data = b.data

        payload = {
            'foo': 'foo',
            'rawData': data['log'].encode('UTF-8')
        }

        try:
            response = self.session.post(self.endpoint, json=payload, headers=self.headers)
        except exceptions.RequestException as e:
            response = str(e)

        if self.debug:
            print(response)
