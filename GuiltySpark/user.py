import regex
import discord
import functools

MANAGE_REGEX = r'(add|remove) role "(.+)"'


def get_id(mention: str):
    re = r'<\@\!(?P<id>\d)+>'
    match = regex.match(re, mention)
    groups = match.capturesdict()

    if len(groups['id']) == 1:
        return int(groups['id'][0])
    else:
        raise ValueError('Cannot process id from ' + mention)


def check_permission(guild: discord.Guild, id: int, permission: str):
    member = guild.get_member(id)
    permissions = member.guild_permissions

    for (perm, val) in permissions:
        if perm == permission:
            return val

# def requires(permission: str):
#     def dec_requires(func):
#         @functools.wraps(func)
#         def wrapper_requires(*args, **kwargs):
#
