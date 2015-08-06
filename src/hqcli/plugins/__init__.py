from abc import abstractmethod, ABCMeta
from schematics.exceptions import ModelValidationError, ModelConversionError
from schematics.models import Model
from schematics.types import URLType
import logging
from hqcli import get_auth_token, get_config
import json
import requests


class AbstractPlugin(object):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger("hq.cli.plugin")
        self.config = None

    def config_class(self):
        class ConfigClass(Model):
            manager_url = URLType(default=get_config().manager_url)
            framework_url = URLType(default=get_config().framework_url)

        return ConfigClass

    def validate_config(self, config_dict):
        try:
            self.config = self.config_class()(config_dict, strict=False)
        except ModelConversionError as e:
            self.logger.error("Could not create config for plugin " + self.name + " "+json.dumps(e.message))
            return False

        try:
            self.config.validate()
        except ModelValidationError:
            self.logger.error("Could not validate config for plugin " + self.name)
            return False

        return True

    def parser(self, subparsers):
        subparser = subparsers.add_parser(self.name)
        self.setup_parser(subparser)

    @abstractmethod
    def setup_parser(self, parser):
        pass

    def api_call_get(self, url):
        r = requests.get(url, headers={"X-Auth-Token": get_auth_token()})

        return r

    def api_call_post(self, url, data=None):
        r = requests.post(url, headers={"X-Auth-Token": get_auth_token(), "Content-Type": "application/json"},
                          data=json.dumps(data))

        return r

    def api_call_put(self, url, data=None):
        r = requests.put(url, headers={"X-Auth-Token": get_auth_token(), "Content-Type": "application/json"},
                         data=json.dumps(data))

        return r

    def api_call_delete(self, url, data=None):
        r = requests.delete(url, headers={"X-Auth-Token": get_auth_token(), "Content-Type": "application/json"},
                            data=json.dumps(data))

        return r
