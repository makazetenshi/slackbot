import yaml
import logging
from io import open
import message_dispatcher as dispatcher
class CommandHandler(object):
    FORMAT = "%(asctime)-15s %(message)s"
    logging.basicConfig(filename='bot.log', level=logging.DEBUG, format=FORMAT)

    @staticmethod
    def handle(integration, command, channel, slack_client, args):
        if integration != None:
            integration_module = __import__(integration['module'])
            integration_class = getattr(integration_module, integration['class'])
            dyn_integration = integration_class()
            message = dyn_integration.parse_command(command, channel, args)
        else:
            message = "Unknown integration/commmand"
        dispatcher.MessageDispatcher().dispatch_message(channel, message, slack_client)

    def get_integration(self, command, channel, slack_client, args):
        with open("integrations.yaml") as stream:
            try:
                parsed_command = command.split()[0]
                integration = yaml.load(stream)[parsed_command]
                self.handle(integration, command, channel, slack_client, args)
            except Exception as e:
                logging.exception(e)
