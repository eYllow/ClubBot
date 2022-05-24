import discord
from discord.ext import commands
import json
import os
import random

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('ready')


@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amount = users[str(user.id)]['wallet']
    bank_amount = users[str(user.id)]['bank']

    em = discord.Embed(title=f"{ctx.author.name}'s Balance", color=discord.Color.red())
    em.add_field(name='Wallet', value=wallet_amount)

    await ctx.send(embed=em)
    pass


@client.command()
async def earn(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    earnings = random.randint(0, 100)

    await ctx.send(f"Earned: {earnings}")
    users[str(user.id)]['wallet'] += earnings
    with open('bank.json', 'w') as f:
        json.dump(users, f)
    await ctx.send(f'New balance: {users[str(user.id)]["wallet"]}')


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        print('found data')
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
        print('money set to zero')

    with open('bank.json', 'w') as f:
        json.dump(users, f)
    return


async def get_bank_data():
    with open('bank.json', 'r') as f:
        users = json.load(f)

    return users


async def on_command_error(ctx):
    await ctx.send('this command does not exist')


client.run(hiddentoken)
