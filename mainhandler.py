import logging
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv
from websocket import WebSocketConnectionClosedException
import command_handler
from slackclient import SlackClient
class MainHandler(object):
    global dotenv_path
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(filename='swapbot.log', level=logging.DEBUG, format=FORMAT)
    global SLACK_TOKEN
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

    @staticmethod
    def parse_output(slack_output):
        output_list = slack_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and (output['text'].encode('utf8')).startswith('.') and 'subtype' not in output:
                    return output['text'][1:], \
                            output['channel'], None
                if output and 'file' in output and 'comment' in output:
                    return output['comment']['comment'][1:], \
                            output['channel'], output['file']['url_private']

    def main(self):
        date_string = "%Y-%m-%d %H:%M:%S"
        READ_WEBSOCKET_DELAY = 1
        global slack_client
        slack_client = SlackClient(SLACK_TOKEN)
        if slack_client.rtm_connect():
            while True:
                try:
                    command, channel, args = self.parse_output(slack_client.rtm_read())
                    if command and channel:
                        command = command.encode("utf8")
                        handler = command_handler.CommandHandler()
                        handler.get_integration(command, channel, slack_client, args)
                        time.sleep(READ_WEBSOCKET_DELAY)
                except WebSocketConnectionClosedException as e:
                    logging.exception(e)
                    time.sleep(READ_WEBSOCKET_DELAY)
                    slack_client.rtm_connect()
                except Exception as e:
                    if (type(e).__name__ != 'TypeError'):
                        logging.exception(e)
                    time.sleep(READ_WEBSOCKET_DELAY)

        else:
            logging.debug("Connection Failed.")

if __name__ == '__main__':
    MainHandler().main()
