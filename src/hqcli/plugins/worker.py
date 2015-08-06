from hqcli.plugins import AbstractPlugin
import logging
import sys
import json


class Plugin(AbstractPlugin):

    def __init__(self):
        super(Plugin, self).__init__("worker")
        self.logger = logging.getLogger("hq.cli.plugin.worker")

    def setup_parser(self, parser):
        subparsers = parser.add_subparsers(help="worker command to run", dest='command')

        list_parser = subparsers.add_parser('list')
        list_parser.add_argument('-f', '--framework', default=None, type=str, help='The framework to filter by')
        list_parser.add_argument('-t', '--target', default=None, type=str, help='The target to filter by')
        list_parser.set_defaults(func=self.list)

        list_parser = subparsers.add_parser('delete')
        list_parser.add_argument('worker_id', type=int, help='The worker id to delete')
        list_parser.set_defaults(func=self.delete)

    def list(self, args):
        url = self.config.manager_url+"/worker"

        if args.framework is not None:
            url += "?framework="+args.framework+"&"

        if args.target is not None:
            if url[-1:] != '&':
                url += '?'
            url += "target="+args.target

        if url[-1:] == '&':
            url = url[:-1]

        r = self.api_call_get(url)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info("Workers\n"+json.dumps(json.loads(r.text), indent=2))

    def delete(self, args):
        while True:
            s = raw_input("Are you sure you want to delete the worker "+str(args.worker_id)+" (Y/N)? ")
            if s == 'Y':
                break

            if s == 'N':
                sys.exit(1)

        r = self.api_call_delete(self.config.manager_url+"/worker/"+str(args.worker_id))

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info(r.text)
