import datetime

import discord
import regex
import GuiltySpark.dice as dice


def log(s):
    print('[%s] %s' % (str(datetime.datetime.now()), s))


async def reply(message: discord.Message, s):
    await message.channel.send('%s %s' % (message.author.mention, s))
    log('Replied: %s' % s)


class GuiltySpark(discord.Client):

    async def on_ready(self):
        log('Logged in as ' + str(self.user))
        log('ID: ' + str(self.user.id))

    async def on_message(self, message: discord.Message):
        try:
            for user in message.mentions:
                if user == self.user and message.content.strip().startswith('<@!%d>' % self.user.id):
                    log('Mentioned in #%s in %s' % (message.channel, message.guild))
                    log('Message: %s' % message.content)
                    content = message.content.replace('<@!%d>' % self.user.id, '').lower().strip()
                    if 'hello' in content.lower():
                        await message.channel.send("Hello %s! My name is 343 Guilty Spark. Nice to meet you!" %
                                                   message.author.mention)
                    elif content.startswith('roll '):
                        await reply(message, dice.roll(message.content.split()[2]))
                    # elif regex.match(, content):

                    else:
                        await reply(message, "Sorry, I didn't recognize that.")
        except Exception as e:
            await reply(message, "Sorry I couldn't understand that.")
            log(e)
