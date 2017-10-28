import logging
import importlib

from slackbot.settings import LOG_FILE, LOG_LEVEL, LOG_REQUESTS


def define_log():
    if LOG_REQUESTS:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger('slackbot')
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_console = logging.StreamHandler()
    logger_console.setLevel(LOG_LEVEL)
    logger_console.setFormatter(formatter)
    logger_file = logging.FileHandler(filename=LOG_FILE)
    logger_file.setLevel(LOG_LEVEL)
    logger_file.setFormatter(formatter)
    logger.addHandler(logger_console)
    logger.addHandler(logger_file)
    return logger


class BotResponse:
    """Class for all response."""
    SLACK_ENTER_COMMAND = "Please enter command."
    SLACK_ENTER_SERVICE_COMMAND = "Please enter service command."
    SLACK_UNIVERSAL_ANSWER = "I know answer to your question. It's 42!"
    SLACK_DONT_UNDERSTAND = "Sorry, i don't understand."
    SLACK_UNKNOWN_PROVIDER = "This provider unknown."
    SLACK_PARAMS_REQUIRE = "This command require params."
    SLACK_PROVIDER_UNKNOWN_COMMAND = "Sorry, i don't understand command"

class Bot:
    """
    Main bot class
    """

    RESPONSE = BotResponse()

    def __init__(self):
        self.name = ''
        self.logger = define_log()
        # self.logger = logging.getLogger('slackbot')

    def just_do_it(self, provider, message):

        params = ''
        command_line = message.split(maxsplit=1)
        if len(command_line) > 1:
            command, params = command_line
        else:
            command = command_line[0]
        try:
            provider_class = importlib.import_module('slackbot.providers.{}'.format(provider))
            provider_obj = getattr(provider_class, provider.capitalize())()
            provider_func = getattr(provider_obj, command)
        except AttributeError:
            return "Unknown command"

        data = provider_func(params)
        return data
