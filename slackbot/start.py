import json
import requests
import websocket

from slackbot.bot import Bot, define_log
from slackbot.settings import SLACK_API_TOKEN, SLACK_API_URL, SLACK_PROVIDERS


def connect():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data_json = {'token': SLACK_API_TOKEN}
    r = requests.post(SLACK_API_URL + 'rtm.connect', headers=headers, data=data_json)
    return r.json()


def on_message(ws, message):
    bot.logger.debug(message)

    message_json = json.loads(message)
    message_type = message_json.get('type')
    message_user = message_json.get('user')
    message_text = message_json.get('text')
    message_channel = message_json.get('channel')

    answer = {
        "type": "message",
        "channel": message_channel,
        "text": "<@{}>: ".format(message_user)
    }

    if message_type == 'message' and message_text and message_text.startswith('<@{}>'.format(bot.name)):
        if len(message_text.split(maxsplit=1)) == 1:
            answer['text'] += bot.RESPONSE.SLACK_ENTER_COMMAND
        else:
            bot_name, provider_command = message_text.split(maxsplit=1)
            tmp_provider = provider_command.split(maxsplit=1)
            if len(tmp_provider) > 1:
                provider, command = tmp_provider
                if provider not in SLACK_PROVIDERS:
                    answer['text'] += bot.RESPONSE.SLACK_DONT_UNDERSTAND
                else:
                    answer['text'] += bot.just_do_it(provider, command)
            else:
                if tmp_provider[0] not in SLACK_PROVIDERS:
                    answer['text'] += bot.RESPONSE.SLACK_DONT_UNDERSTAND
                else:
                    answer['text'] += bot.RESPONSE.SLACK_ENTER_SERVICE_COMMAND
        ws.send(json.dumps(answer))


def on_close(ws):
    bot.logger.info("Connection closed.")

if __name__ == '__main__':
    bot = Bot()
    bot.logger.info("Slackbot starting")
    try:
        data = connect()
        bot.logger.debug(data)
        if data['self']['id']:
            bot.name = data['self']['id']
        else:
            raise Exception
        ws = websocket.WebSocketApp(data['url'], on_message=on_message)
        ws.run_forever()
    except requests.ConnectionError as e:
        bot.logger.critical("We can't get websocket server address. Reason: {}".format(e))
    except websocket.WebSocketException as e:
        bot.logger.critical("Some problems with websocket server. Error: {}".format(e))
    except Exception as e:
        bot.logger.critical("Unknown error. Error: ".format(e))
