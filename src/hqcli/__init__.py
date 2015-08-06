import hqcli.parser
import logging
from schematics.exceptions import ModelValidationError, ModelConversionError
from schematics.models import Model
from schematics.types import StringType, URLType
import yaml
import os
import getpass
import requests
import json
import sys
from yaml import YAMLError

config = None

parent_logger = logging.getLogger("hq")
parent_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

parent_logger.addHandler(ch)

logger = logging.getLogger("hq.cli")


def main():
    global config

    logger.info("Herqles CLI")

    class ConfigClass(Model):
        username = StringType()
        password = StringType()
        manager_url = URLType(required=True)
        framework_url = URLType(required=True)

    config_dir = os.path.expanduser("~")+"/.herq"
    config_path = os.getenv("HERQ_CONFIG", config_dir+"/config.yaml")
    plugins_dir = os.getenv("HERQ_PLUGINS", config_dir+"/plugins")

    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    if not os.path.isdir(plugins_dir):
        os.makedirs(plugins_dir)

    if not os.path.isfile(config_path):
        logger.error("Base config does not exist in "+config_path)
        sys.exit(1)

    with open(config_path) as f:
        try:
            config = ConfigClass(yaml.load(f), strict=False)
        except ModelConversionError as e:
            logger.error("Could not create base config "+json.dumps(e.message))
            sys.exit(1)
        except YAMLError as e:
            logger.error("Could not load base config "+str(e))
            sys.exit(1)

    try:
        config.validate()
    except ModelValidationError as e:
        logger.error("Error validating base config "+json.dumps(e.message))
        sys.exit(1)

    # Load plugins
    plugins = []

    from hqcli.plugins.task import Plugin as TaskPlugin
    from hqcli.plugins.user import Plugin as UserPlugin
    from hqcli.plugins.worker import Plugin as WorkerPlugin
    from hqcli.plugins.job import Plugin as JobPlugin

    task_plugin = TaskPlugin()
    task_plugin.validate_config({})
    task_plugin.parser(hqcli.parser.subparsers)
    plugins.append(task_plugin)

    user_plugin = UserPlugin()
    user_plugin.validate_config({})
    user_plugin.parser(hqcli.parser.subparsers)
    plugins.append(user_plugin)

    worker_plugin = WorkerPlugin()
    worker_plugin.validate_config({})
    worker_plugin.parser(hqcli.parser.subparsers)
    plugins.append(worker_plugin)

    job_plugin = JobPlugin()
    job_plugin.validate_config({})
    job_plugin.parser(hqcli.parser.subparsers)
    plugins.append(job_plugin)

    for config_name in os.listdir(plugins_dir):

        if config_name.endswith(".yaml") is False:
            continue

        with open(plugins_dir+"/"+config_name) as f:
            try:
                plugin_config = yaml.load(f)
                if plugin_config is None:
                    plugin_config = {}
            except YAMLError as e:
                logger.error("Could not load "+config_name+" config "+str(e))
                sys.exit(1)

        if 'module' not in plugin_config:
            logger.error("Plugin config "+config_name+" does not have a module key.")
            sys.exit(1)

        modules = plugin_config['module'].split(".")
        module = __import__(plugin_config['module'])
        modules.pop(0)
        for m in modules:
            module = getattr(module, m)
        plugin = getattr(module, 'Plugin')

        plugin = plugin()

        if not plugin.validate_config(plugin_config):
            logger.error("Error loading plugin "+plugin.name)
            sys.exit(1)

        plugin.parser(hqcli.parser.subparsers)
        plugins.append(plugin)

    if len(plugins) == 0:
        logger.error("No plugins loaded")
        sys.exit(1)

    logger.info("Loaded " + str(len(plugins)) + " plugin(s)")

    args = hqcli.parser.parser.parse_args()

    if config.username is None:
        config.username = getpass.getuser()

    if not authenticate():
        logger.error("Error Authenticating")
        sys.exit(1)

    logger.info("Authenticated")

    args.func(args)


def authenticate(tries=5, recreate=False):

    if tries == 0:
        logger.error("Could not get a valid token after 5 tries")

    token = get_auth_token()

    if recreate or token is None:
        if config.password is None:
            config.password = getpass.getpass()
        data = {"username": config.username, "password": config.password}
        r = requests.put(config.manager_url+"/user/token", headers={"Content-Type": "application/json"},
                         data=json.dumps(data))
        response = json.loads(r.text)

        if r.status_code != 200:
            logger.error(r.text)
            return False

        token = response['token']
        set_auth_token(token)
        return authenticate(tries=tries-1)

    r = requests.get(config.manager_url+"/user/"+config.username, headers={"X-Auth-Token": token})

    if r.status_code == 403:
        logger.error("Invalid Token. Trying to get another")
        return authenticate(tries=tries-1, recreate=True)
    elif r.status_code != 200:
        logger.error(r.text)
        return False

    return True


def get_auth_token():

    token_path = os.path.expanduser("~")+"/.herq/token"

    if not os.path.isfile(token_path):
        return None

    with open(token_path) as f:
        return f.read()


def set_auth_token(token):

    token_path = os.path.expanduser("~")+"/.herq/token"

    with open(token_path, "w") as f:
        f.write(token)


def get_config():
    global config
    return config
