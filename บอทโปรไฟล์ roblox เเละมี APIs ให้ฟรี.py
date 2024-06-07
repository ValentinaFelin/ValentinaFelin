import discord
from discord.ext import commands
import aiohttp

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(name='search')
@commands.cooldown(1, 20, commands.BucketType.user)
async def check_account_info(ctx, username):
    if not username:
        await ctx.send("กรุณาระบุชื่อผู้ใช้ครับ :blush:")
        return

    account_info = await get_account_info(ctx, username)
    if account_info:
        embed = discord.Embed(title=f'Profile information for {username}')
        embed.add_field(name="Username", value=account_info.get('username', 'Not available'), inline=False)
        embed.add_field(name="Display Name", value=account_info.get('display_name', 'Not available'), inline=False)
        embed.add_field(name="Account Age", value=account_info.get('created_at', 'Not available'), inline=False)
        embed.set_footer(text="By Catno Studio ")
        embed.colour = discord.Color.from_rgb(157, 222, 139)  # Set the color of the embed
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Invalid Roblox Name", description=f"สาเหตุที่เป็นไปได้ระบบมีความล่าช้าอาจจะเกิดข้อผิดพลาดได้โปรดรอไม่เกิน 20 วินาทีและลองอีกครั้ง {ctx.author.mention}", colour=discord.Color.red())
        await ctx.send(embed=embed)


async def get_account_info(ctx, username):
    url = f"https://users.roblox.com/v1/users/search?keyword={username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:

                return None

            data = await response.json()
            users = data.get('data', [])
            if users:
                user_id = users[0]['id']
                account_info = {}
                account_info['username'] = users[0]['name']

                # Get Display Name
                async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as user_response:
                    user_data = await user_response.json()
                    account_info['display_name'] = user_data.get('displayName', 'Not available')

                # Fetch additional user info to get account creation date
                async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as user_response:
                    user_data = await user_response.json()
                    account_info['created_at'] = user_data.get('created', 'Not available')

                return account_info
            else:
                return None




bot.run('  ที่นี้ ')
