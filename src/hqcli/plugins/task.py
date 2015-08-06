from hqcli.plugins import AbstractPlugin
import logging
import json
import sys


class Plugin(AbstractPlugin):

    def __init__(self):
        super(Plugin, self).__init__("task")
        self.logger = logging.getLogger("hq.cli.plugin.task")

    def setup_parser(self, parser):
        subparsers = parser.add_subparsers(help="task command to run", dest='command')

        list_parser = subparsers.add_parser('list')
        list_parser.add_argument('-p', '--page', default=1, type=int, help='List page')
        list_parser.add_argument('-j', '--job_id', default=0, type=int, help='Job ID to filter tasks by')
        list_parser.set_defaults(func=self.list)

        get_parser = subparsers.add_parser('get')
        get_parser.add_argument('task_id', type=int, help='Task ID')
        get_parser.set_defaults(func=self.get)

    def list(self, args):
        url = self.config.manager_url+"/task?page="+str(args.page)

        if args.job_id != 0:
            url += "&job_id="+str(args.job_id)

        r = self.api_call_get(url)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info("Tasks\n"+json.dumps(json.loads(r.text), indent=2))

    def get(self, args):
        url = self.config.manager_url+"/task/"+str(args.task_id)

        r = self.api_call_get(url)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info("Task "+str(args.task_id)+"\n"+json.dumps(json.loads(r.text), indent=2))
