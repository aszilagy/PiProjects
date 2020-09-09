import pydle
import configparser as cf
import asyncio
import requests
import time
import random
import re

configParser = cf.ConfigParser()
configParser.read('config.ini')
clientId = configParser['API']['CLIENT_ID']
oauthToken = configParser['API']['OAUTH_TOKEN']
piPrivateIP = configParser['PI']['PRIVATE_IP']

class MyBot(pydle.Client):
    def __init__(self, nickname):
        super().__init__(nickname)
        
        self.rate = 1
        self.per = 5
        self.allowance = self.rate
        self.lastMessageTime = time.time()
        self.joke = self.Joke()

    async def on_connect(self):
        await self.join('#risky9')

    async def on_raw_004(self, message):
        #ircd, user_modes, channel_modes
        target, hostname = message.params[:2]

        self._channel_modes = 'a'
        self._user_modes = 'b'

    async def on_channel_message(self, target, by, message):
        if by != self.nickname:
            helpMessage = ['!help', '!color', '!led']
            strippedMessage = re.sub(r"([!@#$%,.;'?])", r"", message.lower())
            print("CHANNEL", target, by, strippedMessage)
            if strippedMessage in helpMessage:
                await self.helpMessage(target, by)

            elif message == "!joke":
                jokeQuestion = await self.joke.question(by)
                await self.message(target, jokeQuestion, True)

            elif self.joke.isInProgress() and strippedMessage == "whos there":
                jokeAnswer = await self.joke.answer(by)
                await self.message(target, jokeAnswer, True)

            elif self.joke.isInProgress() and strippedMessage == self.joke.jokeAnswer.lower().strip(' ') + " who":
                finalAnswer = await self.joke.answer(by)
                await self.message(target, finalAnswer)

            elif self.joke.isInProgress() and strippedMessage != "whos there" and strippedMessage != self.joke.jokeAnswer.lower().strip(' ') + " who":
                    self.joke.partOfJoke = 0
                    ruinedJoke = await self.joke.answer(by)
                    await self.message(target, ruinedJoke)

        keywordList = ['blue', 'red', 'white', 'green']
        for word in message.split():
            if word.lower() in keywordList:
                url = piPrivateIP
                requests.post(url, data={'message': message})
                break

    async def helpMessage(self, target, by):
        helpResponse = "Welcome @" + by + "! Add any of the following colors to your next message to turn on the LEDS: red, white, blue, green!"
        await self.message("#risky9", helpResponse)

    async def message(self, target, message, override=False):
        print("Sending message %s" % message)
        if override:
            await super().message(target, message)

        else:    
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
                self.allowance -= 1.0

    async def on_join(self, channel, user):
        pass

    class Joke:
        def __init__(self):
            self.partOfJoke = 0
            with open('knock_knock.txt', 'r') as f:
                self.listOfJokes = f.readlines()

        def isInProgress(self):
            if self.partOfJoke > 0:
                return True
            
            return False

        async def question(self, target):
            lineNum = random.randrange(97)
            entireJoke = self.listOfJokes[lineNum].split('.')

            self.jokeQuestion = entireJoke[0]
            self.jokeAnswer = entireJoke[1]
            self.finalAnswer = ' '.join(entireJoke[2:])
            self.partOfJoke += 1

            return self.jokeQuestion

        async def answer(self, target):
            if self.partOfJoke == 1:
                self.partOfJoke += 1
                return self.jokeAnswer
            elif self.partOfJoke == 2:
                self.partOfJoke = 0
                return self.finalAnswer
            else:
                self.partOfJoke = 0
                return "Way to mess up the joke @ %s" % target

def main():
    client = MyBot(nickname="risky9")
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(client.connect(hostname='irc.chat.twitch.tv', port='6697', password=oauthToken, tls=True, tls_verify=False), loop=loop)
    loop.run_forever()
    
if __name__ == '__main__':
    main()
