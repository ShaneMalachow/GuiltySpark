import asyncio
import datetime
import re

import discord
import typing
import dateutil.parser
from discord.ext import commands
from discord.utils import get
from discord.ext import timers
import GuiltySpark.dice as dice


def log(s):
    print('[%s] %s' % (str(datetime.datetime.now()), s))


def prefix(bot, message):
    return '/gs', '<@!%d>' % bot.user.id, '<@%d>' % bot.user.id


async def get_perms(guild, user):
    return guild.get_member(user.id).guild_permissions


def run(token):
    log('Initializing bot...')
    bot = commands.Bot(command_prefix=commands.when_mentioned_or('/gs '))
    bot.timer_manager = timers.TimerManager(bot)
    log('Setting up commands...')

    @bot.command()
    async def roll(ctx: discord.ext.commands.Context, arg):
        log('Roll command from %s: %s' % (ctx.author, arg))
        await ctx.send('%s %s' % (ctx.author.mention, dice.roll(arg)))

    @bot.command()
    async def user(ctx: discord.ext.commands.Context, member: discord.Member, *args):
        if args[0].lower() == 'role':
            if not (await get_perms(ctx.guild, ctx.author)).manage_roles:
                await ctx.send("%s You don't have manage_roles permissions." % ctx.author.mention)
            else:
                if args[1].lower() in ['add']:
                    await member.add_roles(get(ctx.guild.roles, name=args[2]))
                elif args[1].lower() in ['remove', 'rm', 'delete']:
                    await member.remove_roles(get(ctx.guild.roles, name=args[2]))

    @bot.command(name="remind")
    async def remind(ctx, who: typing.Union[discord.Member, str], s, cls, *, time):
        if isinstance(who, str) and who.lower() == 'me':
            who = ctx.author
        text = '%s %s' % (who.mention, s)
        if cls.lower() == 'on':
            date = dateutil.parser.parse(time)
            log('Will remind "%s" on %s' % (text, date))
            bot.timer_manager.create_timer("reminder", date, args=(ctx.channel.id, ctx.author.id, text))
        elif cls.lower() == 'in':
            reg = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
            parts = reg.match(time)
            if not parts:
                log('Error parsing time')
            parts = parts.groupdict()
            time_params = {}
            for (name, param) in parts.items():
                if param:
                    time_params[name] = int(param)
            delta = datetime.timedelta(**time_params)
            date = datetime.datetime.now() + delta
            log('Will remind "%s" on %s' % (text, date))
        else:
            return
        while True:
            if datetime.datetime.now() >= date:
                log('Reminding ' + str(ctx.author))
                await ctx.send(text)
                return
            else:
                await asyncio.sleep(1)

    @bot.event
    async def on_reminder(channel_id, author_id, text):
        channel = bot.get_channel(channel_id)
        await channel.send(text)

    @bot.event
    async def on_ready():
        log('Ready to go!')

    log('Starting bot...')
    bot.run(token)
    log('Shutting down...')
