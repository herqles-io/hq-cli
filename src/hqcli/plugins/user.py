from hqcli.plugins import AbstractPlugin
import logging
import sys


class Plugin(AbstractPlugin):

    def __init__(self):
        super(Plugin, self).__init__("user")
        self.logger = logging.getLogger("hq.cli.plugin.user")

    def setup_parser(self, parser):
        subparsers = parser.add_subparsers(help="user command to run", dest='command')

        add_user_parser = subparsers.add_parser('add')
        add_user_parser.add_argument('username', type=str, help="The user's username")
        add_user_parser.add_argument('-p', '--password', default='', type=str, help="The user's password")
        add_user_parser.set_defaults(func=self.add_user)

        get_user_parser = subparsers.add_parser('get')
        get_user_parser.add_argument('username', type=str, help="The user's username")
        get_user_parser.set_defaults(func=self.get_user)

        delete_user_parser = subparsers.add_parser('delete')
        delete_user_parser.add_argument('username', type=str, help="The user's username")
        delete_user_parser.set_defaults(func=self.delete_user)

        change_password_parser = subparsers.add_parser('password')
        change_password_parser.add_argument('-u', '--username', default=None, type=str, help="The user's username")
        change_password_parser.add_argument('password', type=str, help="The user's password")
        change_password_parser.set_defaults(func=self.change_password)

        add_permission_parser = subparsers.add_parser('addperm')
        add_permission_parser.add_argument('username', type=str, help="The user's username")
        add_permission_parser.add_argument('permission', type=str, help="The permission to add")
        add_permission_parser.set_defaults(func=self.add_permission)

        remove_permission_parser = subparsers.add_parser('removeperm')
        remove_permission_parser.add_argument('username', type=str, help="The user's username")
        remove_permission_parser.add_argument('permission', type=str, help="The permission to remove")
        remove_permission_parser.set_defaults(func=self.remove_permission)

    def add_user(self, args):
        data = {"username": args.username, "password": args.password}
        r = self.api_call_post(self.config.manager_url+"/user/add", data=data)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info(r.text)

    def get_user(self, args):
        r = self.api_call_get(self.config.manager_url+"/user/"+args.username)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info(r.text)

    def delete_user(self, args):

        while True:
            s = raw_input("Are you sure you want to delete the user "+args.username+" (Y/N)? ")
            if s == 'Y':
                break

            if s == 'N':
                sys.exit(1)

        r = self.api_call_delete(self.config.manager_url+"/user/"+args.username)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info(r.text)

    def change_password(self, args):
        data = {"password": args.password}

        if args.username is not None:
            data['username'] = args.username

        r = self.api_call_put(self.config.manager_url+"/user/password", data=data)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info(r.text)

    def add_permission(self, args):
        data = {"username": args.username, "permission": args.permission}
        r = self.api_call_put(self.config.manager_url+"/user/permission", data=data)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info(r.text)

    def remove_permission(self, args):
        data = {"username": args.username, "permission": args.permission}
        r = self.api_call_delete(self.config.manager_url+"/user/permission", data=data)

        if r.status_code != 200:
            self.logger.error(r.text)
            sys.exit(1)

        self.logger.info(r.text)
