import webserver
import discord
import requests
import github_api
from discord.ext import commands
import os

client = commands.Bot(command_prefix="?")

token = os.environ['token']

@client.event
async def on_ready():
    print('Bot online')


@client.command()
async def hello(ctx):
    await ctx.send("Hi")

@client.command()
async def detailu(ctx, question):
    user = question
    print(user)
    about = github_api.user_data(user)
    if about:
        about_embed = discord.Embed(title="About " + user, desc="Here is some data about about " + user, color=0x3498db)
        about_embed.add_field(name="Public Repositories", value=f"The user has {about['repos']} public repositories")
        about_embed.add_field(name="Public Gists", value=f"The user has {about['gists']} public gists")
        about_embed.add_field(name="User Bio", value=about['bio'])
        about_embed.add_field(name="Avatar", value="Here is the avatar", inline=False)
        about_embed.set_image(url=about['url'])
        await ctx.send(embed=about_embed)

    else:
        await ctx.send('No such user')


@client.command()
async def repos(ctx, question):
    username = question
    data = github_api.repos(username)
    if data:
        repos_embed = discord.Embed(title=f"Repositories of {username}",  desc="These are therepository of the user", color=0x3498db)
        for i in data:
            name = i['name']
            description = i['desc']
            clone_url = i['clone']
            lang = i['lang']
            forks = i['forks']
            repos_embed.add_field(name=name, value=f"The name of this repo is {name} and its description is {description}. The clone url for this repo is {clone_url}. The language of this repo is {lang}.It has {forks} forks")
        try:
            await ctx.send(embed=repos_embed)      

        except Exception as e:
            print(e)
            await ctx.send("Message too long cannot send it. Sorry 😞😞😞😞")
    else:
        await ctx.send("No such user")

@client.command()
async def download(ctx, question):
    url = question + "/archive/refs/heads/master.zip"
    
    response = requests.get(url)
    if int(response.status_code) == 404:
        url = question + "/archive/refs/heads/main.zip"
        
        response = requests.get(url)
        
    print(response.status_code)
    
    if int(response.status_code) != 404:
        with open('repo.zip', 'wb') as file:
            file.write(response.content)
            file.close()
            await ctx.send(file=discord.File('repo.zip'))
    
    else:
           
        await ctx.send("Wrong link provided. Try another")
webserver.keep_alive()
client.run(token)