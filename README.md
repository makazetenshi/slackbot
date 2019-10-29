# Slackbot

Written in Python 3.5 (was ported from 2.7)

## Getting Started

First off you're going to need to create a `.env` file.

The bot reads off of this file whenever any form of token is needed, which is useful for not only slack but also for any integration you implement later on.

You are going to need a token for the bot issued from Slack ([details here](https://api.slack.com/bot-users#)).

This token should be defined in the `.env` file as:
 
        SLACK_TOKEN=xxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
 
Running the bot is as simple as running `python mainhandler.py`.

Or alternatively `nohup python mainhandler.py &` to avoid interrupting the bot on hangup.

#### Dependencies

Running `pip install -r requirements.txt` should install all needed dependencies.

Currently needed:

    certifi==2018.8.24
    chardet==3.0.4
    idna==2.7
    imgurpython==1.1.7
    python-dotenv==0.9.1
    PyYAML==3.13
    requests==2.19.1
    six==1.11.0
    slackclient==1.3.0
    urllib3==1.23
    websocket-client==0.53.0
    
#### Integrations

The idea behind the bot was that you should be able to add integrations easily so in this section we will look into how you add an integration to the bot.

The format of the integrations defined in `integrations.yaml` is:
    
    command: {module: filename, class: classname}

Where command is you would type (prefixed with a dot, eg `.img`) as a command, and filename and classname are self-explanatory.

The requirements of an integration is that it has the following method: 

    def parse_command(self, command, channel, args):
    
with command being the command parsed, channel being the origin(and destination) of any output and args being any arguments passed along, in case your command has any options. An integration also needs to implement the `IntegrationInterface` which for now only contains the `parse_command` method, but more might come in the future. This was made to ensure that all required methods have been implemented.


For an idea of how integrations work, have a look at `urban.py` and `imgur.py`.

_Currently loading of files via absolute filepath is not supported, but could be added using importlib.util_
