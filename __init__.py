import json
import requests
import pprint

class BotBase():

    PARSE_MODE_MARKDOWN = 'Markdown'
    PARSE_MODE_HTML = 'HTML'

    METHOD_SEND_MESSAGE = 'sendMessage'
    METHOD_GET_UPDATES = 'getUpdates'

    def __init__(self,config):
        self.config = config
        self.updateOffset = 0

    def getUrl(self, method):
        return 'https://api.telegram.org/bot%s/%s' % (self.config['token'], method,)


    def sendMessage(self,text ="", parse_mode = PARSE_MODE_HTML):
        r = requests.post(self.getUrl(self.METHOD_SEND_MESSAGE), json={
            'chat_id': self.config['channelId'],
            'text': text,
            'parse_mode': parse_mode,
        })

        if r.status_code != 200:
            print(r.text)

        return r.json

    def listen(self):
        while True:
            r = requests.post(self.getUrl(self.METHOD_GET_UPDATES), json={
                'offset': self.updateOffset,
                'timeout': 60,
            })
            
            if r.status_code != 200:
                print (r.text)
                return

            received_data = r.json()

            if not received_data['ok']:
                print(r.text)
            else:
                for update in received_data['result']:
                    self.updateOffset = max(self.updateOffset,update['update_id']+1)
                    self.on_update(update)


    def on_update(self):
        pass

class Bot(BotBase):

    def on_update(self,update):
        print(update)
    

def main():
    
    config = {}

    with open('settings.json') as f:
        config = json.load(f)

    if config is None:
        print ('Error getting settings')
        return

    bot = Bot(config)
    
    bot.listen()

    pass


main()
