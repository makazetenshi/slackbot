import logging
import os
from io import open as iopen
from os.path import join, dirname
from random import randint

import requests
from dotenv import load_dotenv
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

from integration_interface import IntegrationInterface


class Imgur(IntegrationInterface):
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(filename='swapbot.log', level=logging.DEBUG, format=FORMAT)
    global dotenv_path
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    global IMGUR_CLIENT_ID
    IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")
    global IMGUR_CLIENT_SECRET
    IMGUR_CLIENT_SECRET = os.environ.get("IMGUR_CLIENT_SECRET")
    global IMGUR_TOKEN
    IMGUR_TOKEN = os.environ.get("IMGUR_TOKEN")
    global IMGUR_REFRESH_TOKEN
    IMGUR_REFRESH_TOKEN = os.environ.get("IMGUR_REFRESH_TOKEN")
    global SLACK_TOKEN
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    global ALBUM
    ALBUM = os.environ.get("ALBUM")
    global DEFAULT_COMMAND

    def parse_command(self, command, channel, args):
        parsed_command = command.split()
        if len(parsed_command) == 1:
            return self.fetch_image()
        switcher = {
            "-h": "display_commands",
            "-u": "upload_image"
        }
        if parsed_command[1] in switcher:
            function = getattr(self, switcher[parsed_command[1]])
        else:
            return 'Unknown Command.'
        return function(channel, args)

    @staticmethod
    def display_commands(channel, args):
        return "-h: Display Commands\n -u: Upload Image\n None: Display Random Image"

    @staticmethod
    def upload_image(channel, url):
        headers = {"Authorization": "Bearer "+SLACK_TOKEN}
        response = requests.get(url, headers=headers, stream=True)
        parts = url.split("/")
        whitelist = ['jpg', 'png', 'jpeg']
        filename = '/tmp/'+parts[len(parts)-1]
        file_suffix = filename.split('.')[1]
        if file_suffix in whitelist and response.status_code == requests.codes.ok:
            with iopen(filename, 'wb') as file:
                file.write(response.content)
        else:
            return False
        client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, IMGUR_TOKEN, IMGUR_REFRESH_TOKEN)
        config = {
                'album': ALBUM
                }
        try:
            re = client.upload_from_path(filename, config=config, anon=False)
            if re is not None:
                try:
                    response = re['link']
                    os.remove(filename)
                except OSError as e:
                    response = "An error occured."
                    logging.debug(e)
                    pass
        except ImgurClientError as e:
            logging.debug(e)
            print(e.error_message)
            print(e.status_code)
            response = "FAIL"
        return response

    @staticmethod
    def fetch_image():
        try:
            client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, IMGUR_TOKEN, IMGUR_REFRESH_TOKEN)
            album = client.get_album(ALBUM)
            image_count = album.images_count
            images = album.images
        except ImgurClientError as e:
            logging.exception(e)
        return images[randint(0,image_count-1)]['link']
