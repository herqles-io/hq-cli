from hqcli.plugins import AbstractPlugin
import logging
import json
import sys


class Plugin(AbstractPlugin):

    def __init__(self):
        super(Plugin, self).__init__("job")
        self.logger = logging.getLogger("hq.cli.plugin.job")

    def setup_parser(self, parser):
        subparsers = parser.add_subparsers(help="job command to run", dest='command')

        get_parser = subparsers.add_parser('get')
        get_parser.add_argument('job_id', type=int, help='Job ID')
        get_parser.set_defaults(func=self.get)

    def get(self, args):
        url = self.config.manager_url+"/job/"+str(args.job_id)

        r = self.api_call_get(url)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info("Job "+str(args.job_id)+"\n"+json.dumps(json.loads(r.text), indent=2))
