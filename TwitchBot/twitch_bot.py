import pydle
import configparser as cf
import asyncio
import requests
import time

configParser = cf.ConfigParser()
configParser.read('config.ini')
clientId = configParser['API']['CLIENT_ID']
oauthToken = configParser['API']['OAUTH_TOKEN']

class MyBot(pydle.Client):
    def __init__(self, nickname):
        super().__init__(nickname)
        
        self.rate = 1
        self.per = 5
        self.allowance = self.rate
        self.lastMessageTime = time.time()

    async def on_connect(self):
        await self.join('#risky9')

    async def on_raw_004(self, message):
        #ircd, user_modes, channel_modes
        target, hostname = message.params[:2]

        self._channel_modes = 'a'
        self._user_modes = 'b'

    async def on_channel_message(self, target, by, message):
        print("CHANNEL", target, by, message)
        if by != self.nickname:
            helpMessage = ['!help', '!color', '!led']
            if message.lower() in helpMessage:
                response = 'Type any color from this list to '
                await self.helpMessage(target, by)

        keywordList = ['blue', 'red', 'white', 'green']
        for word in message.split():
            if word.lower() in keywordList:
                url = 'http://192.168.86.147:5000/leds'
                requests.post(url, data={'message': message})
                break

    async def helpMessage(self, target, by):
        helpResponse = "Welcome @" + by + "! Add any of the following colors to your next message to turn on the LEDS: red, white, blue, green!"
        await self.message("#risky9", helpResponse)

    async def message(self, target, message):
        currentTime = time.time()
        timePassed = currentTime - self.lastMessageTime
        self.lastMessageTime = currentTime
        self.allowance += timePassed * (self.rate / self.per)
        if (self.allowance > self.rate):
            self.allowance = self.rate
        if (self.allowance < 1.0):
            pass
        else:
            await super().message(target, message)
            self.allowance -= 1.0;
        
def main():
    client = MyBot(nickname="risky9")
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(client.connect(hostname='irc.chat.twitch.tv', port='6697', password=oauthToken, tls=True, tls_verify=False), loop=loop)
    loop.run_forever()
    
if __name__ == '__main__':
    main()
