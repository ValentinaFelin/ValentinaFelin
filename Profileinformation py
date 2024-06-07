import discord
from discord.ext import commands
import aiohttp

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='search')
async def check_account_info(ctx, username):
    if not username:
        await ctx.send("Please provide a username.")
        return

    account_info = await get_account_info(ctx, username)
    if account_info:
        embed = discord.Embed(title=f'Profile information for {username}')
        embed.add_field(name="Username", value=account_info.get('username', 'Not available'), inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("User not found.")

async def get_account_info(ctx, username):
    url = f"https://auth.roblox.com/v2/usernames?username={username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await ctx.send(f"Failed to fetch data from Roblox API. Status code: {response.status}")
                return None

            data = await response.json()
            usernames = data.get('usernames', [])
            if usernames:
                account_info = {}
                account_info['username'] = usernames[0]
                return account_info
            else:
                return None



bot.run('  ที่นี้ ')
