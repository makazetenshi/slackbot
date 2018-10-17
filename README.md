###Getting Started
First off you're going to need to create a `.env` file.

The bot reads off of this file whenever any form of token is needed, which is useful for not only slack but also for any integration you implement later on.

You are going to need a token for the bot issued from Slack ([details here](https://api.slack.com/bot-users#)).

This token should be defined in the `.env` file as:
 
        SLACK_TOKEN=xxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
 
Running the bot is as simple as running `python mainhandler.py`.

Or alternatively `nohup python mainhandler.py &` to avoid interrupting the bot on hangup.