import json
import requests
class Urban:

    def parse_command(self, command, channel, args):
        parsed_command = command.split(' ', 1)
        return self.perform_lookup(parsed_command[1:])

    @staticmethod
    def perform_lookup(query):
        r = requests.get("http://api.urbandictionary.com/v0/define?term=" + query[0])
        content = r.json()
        if len(content['list']) == 0:
            return 'No results found matching: ' + query[0]
        return content['list'][0]['definition']
