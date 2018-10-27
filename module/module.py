import platform

from requests import Session, exceptions

from shinken.basemodule import BaseModule
from shinken.log import logger

properties = {
    'daemons': ['broker'],
    'type': 'http',
    'external': False
}


def get_instance(plugin):
    name = plugin.get_name()
    logger.info("[alerta] Get a broker for plugin %s" % (name))

    # Get configuration values, if any
    endpoint = getattr(plugin, 'endpoint', 'http://localhost:8080')
    key = getattr(plugin, 'key', None)
    environment = getattr(plugin, 'environment', 'Production')
    customer = getattr(plugin, 'customer', None)
    debug = getattr(plugin, 'debug', False)

    instance = AlertaBroker(plugin, endpoint, key, environment=environment, customer=customer, debug=debug)
    return instance


class AlertaBroker(BaseModule):

    def __init__(self, modconf, endpoint=None, key=None, environment=None, customer=None, debug=False):
        BaseModule.__init__(self, modconf)

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


    def init(self):
        logger.info("[alerta] Initialization...")

    def manage_brok(self, brok):

        if brok.type in ['service_check_result', 'host_check_result', 'update_service_status', 'update_host_status']:
            if self.debug:
                logger.info('[alerta]: %s' % brok.data)

            data = brok.data

            if brok.type in ['service_check_result', 'update_service_status']:
                check_type = 'Service Check'
            else:
                check_type = 'Host Check'

            state = data.get('state', None)

            if state == 'CRITICAL':
                severity = 'critical'
            elif state == 'DOWN':
                severity = 'major'
            elif state in ['UP', 'OK']:
                severity = 'ok'
            elif state == 'PENDING':
                severity = 'indeterminate'
            else:
                severity = 'warning'

            payload = {
                'resource': data['host_name'],
                'event': data.get('service_description', check_type),
                'environment': self.environment,
                'severity': severity,
                'service': ['Platform'],
                'group': 'Shinken',
                'value': '%s (%s)' % (data['state'], data['state_type']),
                'text': data['long_output'] or data['output'],
                'tags': [],
                'attributes': {},
                'origin': 'shinken/%s' % platform.uname()[1],
                'type': brok.type,
                'rawData': data,
                'customer': self.customer
            }

            if data['problem_has_been_acknowledged']:
                payload['status'] = 'ack'

            try:
                url = self.endpoint + '/alert'
                response = self.session.post(url, json=payload, headers=self.headers)
                if self.debug:
                    logger.info('[alerta]: %s' % response.text)
            except exceptions.RequestException as e:
                logger.error(str(e))

    def manage_signal(self, sig, frame):
        logger.info("[alerta] Received signal: %s" % sig)
