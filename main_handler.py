import logging
import os
import time
from os.path import join, dirname
from dotenv import load_dotenv
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
                if output['type'] == 'message' and 'files' not in output:
                    if 'text' in output and (len(output['text']) > 0) and output['text'][0] == '.':
                        return output['text'][1:], \
                            output['channel'], None

    def main(self):
        READ_WEBSOCKET_DELAY = 1
        global slack_client
        slack_client = SlackClient(SLACK_TOKEN)
        if slack_client.rtm_connect():
            while True:
                try:
                    command, channel, args = self.parse_output(slack_client.rtm_read())
                    if command and channel:
                        handler = command_handler.CommandHandler()
                        handler.get_integration(command, channel, slack_client, args)
                        time.sleep(READ_WEBSOCKET_DELAY)
                except Exception as e:
                    logging.exception(e)
                    time.sleep(READ_WEBSOCKET_DELAY)
                    slack_client.rtm_connect()
        else:
            logging.debug("Connection Failed.")

if __name__ == '__main__':
    MainHandler().main()
