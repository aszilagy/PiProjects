import pydle
import configparser as cf
import asyncio
import requests

configParser = cf.ConfigParser()
configParser.read('config.ini')
clientId = configParser['API']['CLIENT_ID']
oauthToken = configParser['API']['OAUTH_TOKEN']

class MyBot(pydle.Client):
    async def on_connect(self):
        print("ONCONNECT")
        await self.join('#risky9')

    async def on_raw_004(self, message):
        print("NEW OVERRIDE", message)
        target, hostname = message.params[:2]
        #ircd, user_modes, channel_modes

        self._channel_modes = 'a'
        self._user_modes = 'b'

    # async def on_message(self, target, source, message):
    #     print(target, source, message)
    #
    # async def on_private_message(self, target, by, message):
    #     if by != self.nickname:
    #         print("PRIVATE", target, by, message)

    async def on_channel_message(self, target, by, message):
        print("CHANNEL", target, by, message)
        if by != 'random': #self.nickname:
            response = "You're a loser " + "@" + by
            #TODO: Add rate limiting
            #await self.message("#risky9", response)
            keywordList = ['blue', 'red', 'white', 'green']
            for key in keywordList:
                if(key in message):
                    url = 'http://192.168.86.145:5000/leds'
                    requests.post(url, data={'message': message})


def main():
    client = MyBot(nickname="risky9")
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(client.connect(hostname='irc.chat.twitch.tv', port='6697', password=oauthToken, tls=True, tls_verify=False), loop=loop)
    loop.run_forever()
    

if __name__ == '__main__':
    main()