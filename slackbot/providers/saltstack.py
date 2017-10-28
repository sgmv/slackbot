import requests
import logging
import shlex
from slackbot.settings import SALTSTACK_URL, SALTSTACK_USER, SALTSTACK_PASSWORD
from slackbot.bot import BotResponse


class SaltstackResponse:

    SALT_ONLY_TARGET = "This command contains only target nodes"



class Saltstack:

    SLACK_COMMANDS = [
        "get_info"
    ]

    logger = logging.getLogger('slackbot')

    HEADERS = {}

    def _get_headers(self):
        data = {
            "username": SALTSTACK_USER,
            "password": SALTSTACK_PASSWORD,
            "eauth": "pam"
        }
        r = requests.post(SALTSTACK_URL+'/login', json=data)
        self.HEADERS['X-Auth-Token'] = r.json()['return'][0]['token']
        self.logger.debug(self.HEADERS)

    def get_info(self, params):
        #TODO: ADD error handler
        if not self.HEADERS:
            self._get_headers()

        data = {
            "client": "local",
            "tgt": "*",
            "fun": "test.ping"
        }
        r = requests.post(SALTSTACK_URL, headers=self.HEADERS, json=data)
        if not r.ok:
            return "Saltsatck not response"
        return str(r.json()['return'])


    def salt(self, params):
        """
        This method eq command line, parse params, create json and return response from saltstack
        :param params:
        :return:
        """
        if not self.HEADERS:
            self._get_headers()

        arg = []
        kwargs = {}

        #TODO: Add handler for parser params, if params None we must first check it

        if not params:
            return BotResponse.SLACK_PARAMS_REQUIRE

        if len(params.split(maxsplit=1)) == 1:
            return SaltstackResponse.SALT_ONLY_TARGET
        else:
            target, params_line = params.split(maxsplit=1)
            if target.startswith("<http://"):
                target = target.strip("<>").split("|")[1]
            self.logger.debug("{} {}".format(target, params_line))

        if len(params_line.split(maxsplit=1)) > 1:
            fun, arg_kwarg = params_line.split(maxsplit=1)
            if fun.startswith("<http://"):
                fun = fun.strip("<>").split("|")[1]
            arg = shlex.split(arg_kwarg)
        else:
            fun = params_line
            if fun.startswith("<http://"):
                fun = fun.strip("<>").split("|")[1]

        data = {
            "client": "local",
            "tgt": target,
            "fun": fun
        }
        if arg:
            data.update({"arg": arg})
        if kwargs:
            data.update({"kwargs": kwargs})
        self.logger.debug(data)
        r = requests.post(SALTSTACK_URL, headers=self.HEADERS, json=data)

        text = []
        for server in r.json()['return']:
            for server_name, server_response in server.items():
                text.append("Server: {}\nData: {}\n".format(server_name, server_response))
        return "\n"+"\n".join(text)






