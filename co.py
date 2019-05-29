import discord
import os
import os.path
import glob
from discord.ext import commands as dcmd

import inspect


def get_mod_path():
    filepath = os.path.abspath(__file__)
    dirname, fname = os.path.split(filepath)
    return dirname

client = discord.Client()

audiodir = os.path.join(get_mod_path(), 'sounds')
description = 'test'
bot = dcmd.Bot(command_prefix='!', description=description)

print(audiodir)


if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

@bot.command(description='Send friendly salutations to this bot.')
async def hello(ctx):
    author = ctx.author
    msg = 'Hello {}'.format(author.mention)
    await ctx.send(msg)

@bot.command(description='Solicit some wisdom from the CO.')
async def play(ctx, sound_name=''):
    if sound_name == '':
        msg = 'You must specify a sound. It should be one of the following\n'
        msg += '\n'.join(sounds)
        await ctx.send(msg)
    await play_sound(ctx, sound_name)

@bot.command(description="Join the given voice channel.")
async def join(ctx, *, channel: discord.VoiceChannel):
    """Joins a voice channel"""
    errmsg = "Can't find channel by the name of {}".format(channel)
    if ctx.voice_client is not None:
        try:
            await ctx.voice_client.move_to(channel)
        except dcmd.errors.BadArgument:
            ctx.send(errmsg)
    else:
        try:
            await channel.connect()
        except dcmd.errors.BadArgument:
            ctx.send(errmsg)
            

@bot.command(description="Leave any connected voice channel.")
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(description="Stops any audio being played.")
async def stop(ctx):
    await ctx.voice_client.stop()

async def play_sound(ctx, name):
    try:
        fname = '.'.join([os.path.join(audiodir, name), 'ogg'])
        if not os.path.exists(fname):
            ctx.send("```Can't find audio file '{}'```".format(name))

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(fname))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)



    except Exception as e:
        fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
        await ctx.send(fmt.format(type(e).__name__, e))


# @client.event
# async def on_ready():
#     print("files found: {}".format('\n'.join(commands)))
#     print('Logged in as')
#     print(client.user.name)
#     print(client.user.id)
#     print('------')

@bot.event
async def on_ready():
    global sounds
    file_list = glob.glob('{}/*.ogg'.format(audiodir))
    sounds = [os.path.split(fname)[1][:-4] for fname in file_list]
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run('NDYyMTUxOTIzMDA5NTg1MTgy.DhdsMQ.Uo1INjjLJq74iKDq5DGtFEuNec8')

