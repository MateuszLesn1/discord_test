import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from time import sleep

import random
import requests


uberduck_auth = ("pub_hokfowvgtdcouysula", "pk_b5b69421-017b-4d98-bbb6-739eba9c1753") #uberudck auth
print(requests.get("https://api.uberduck.ai/status").json())
voicemodel_uuid = "30b67b62-51a8-43db-a1b4-edafd5b4cfea" #voice model


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
         
    @commands.Cog.listener()
    async def on_ready(self):
        print("commands.py is ready!")
       
    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
        
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def ping(self, ctx):
        to = ctx.author
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong you too {to}, my latency is {bot_latency} ms")
        
    @commands.command(aliases=["8ball","question","8"])
    async def magic_eightball(self, ctx):
        with open("responses.txt", "r") as file:
            random_responses = file.readlines()
        response = random.choice(random_responses)     
        await ctx.send(response)
    
    @commands.command()
    async def voice(self, ctx, *, text="hello, how are you"):# tts message when user forgets and argument, sadly can't make it longer, API seems to not pick up voice messages longer than 2 or 3 secs   
        audio_uuid = requests.post(
            "https://api.uberduck.ai/speak",
        json=dict(speech=text, voicemodel_uuid=voicemodel_uuid),
        auth=uberduck_auth).json()["uuid"]
        for t in range(10):
            sleep(1) # check status every second for 10 seconds.
            output = requests.get(
                "https://api.uberduck.ai/speak-status",
                params=dict(uuid=audio_uuid),
                auth=uberduck_auth,
                                 ).json()
            print(output)
            if "path" in output:
                audio_url = output["path"]
                print(audio_url)
                break
        source = FFmpegPCMAudio(audio_url, executable="ffmpeg")
        ctx.voice_client.play(source, after=None)

    #@commands.command()
    #async def embed(self, ctx):
    #    embed_message = discord.Embed(title="title of embed", description="Desciption of embed", color=discord.Color.green())
    #    embed_message.set_author(name=f"Requested by {ctx.author.mention}", icon_url=ctx.author.avatar)
    #    embed_message.set_thumbnail(url=ctx.guild.icon)
    #    embed_message.set_image(url=ctx.guild.icon)
    #    embed_message.add_field(name="Field name", value="Field value", inline=False)
    #    embed_message.set_footer(text="This is a footer")   
    #    await ctx.send(embed = embed_message)
       
class Welcome(commands.Cog) :
    def __init__(self, bot):
        self.client=bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome: ON")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(member)
        await member.send(f"hello {member} ! If you have any questions, hit me up! I can't answer them, but at least i'll listen in silence!")
        guild = self.client.get_guild(764422667901861898)
        channel = discord.utils.get(member.guild.channels, id=1122864989900918795)
        if guild:
            print("guild ok")
        else:
            print("guild not found")
        
        if channel is not None:
                await channel.send(f'Welcome to the {guild.name} Discord Server, {member.mention} !  :partying_face:')
        else:
            print("wrong id channel")
        

async def setup(bot):
    await bot.add_cog(Commands(bot))
    await bot.add_cog(Welcome(bot))
