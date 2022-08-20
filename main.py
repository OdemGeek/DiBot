import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
from HelpCommand import CustomHelpCommand
from spamCheck import SpamChecker
import data

import json
import requests

import datetime  #НЕ МЕШАЕТ? НЕ ТРОГАЙ!
#help_command = commands.DefaultHelpCommand(no_category='Commands')
import aiohttp

#variables start
help_command = CustomHelpCommand()

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'),
                   description='Hey, I\'m Dio or you can call me Di!',
                   help_command=help_command,
                   intents=intents)
bot.session = aiohttp.ClientSession()

botColor = 0x5d45a0
amethystColor = 0x8080ff
greenColor = 0x24f20e
redColor = 0xf60b0b

latLetters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
cyrLetters = [chr(i) for i in range(ord('а'), ord('я') + 1)]
allLetters = latLetters + cyrLetters
'''
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None, amount=1):
    #mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await ctx.channel.purge(limit=int(amount))
    await member.ban(reason=reason)
    await ctx.send(f'ban user {member.mention}')
'''

userTimeoutTime = 1  #in minutes


#bot doing
async def warningBot(member: discord.Member, channel, cause, warn=False):
    print("testing")
    embed = discord.Embed(
        color=0xff9900,
        title=f'Warning {dataManager.getViolation(member)}/{warningLimit}'
    )  # Создание Embed'a
    #await ctx.message.author.send(f'**Server**: {ctx.message.guild.name}')
    #await ctx.message.author.send(f'**Cause**: {cause}')
    await channel.send(embed=embed)  # Отправляем Embe
    embedUser = discord.Embed(
        color=0xff9900,
        title='Warning',
        description=
        f'```fix\n**{member.name}** attention **{bot.user.name}** warned you!```'
    )  # Создание Embed'a для пользователя
    embedUser.add_field(name='**Server:**',
                        value=f'`{channel.guild.name}`',
                        inline=False)
    embedUser.add_field(name='**Cause:**', value=f'`{cause}`', inline=False)

    await member.send(embed=embedUser)  # Отправляем Embed пользователю
    if dataManager.getViolation(member) >= warningLimit:
        handshake = await timeout_user(user_id=member.id,
                                       guild_id=channel.guild.id,
                                       until=userTimeoutTime)
        if handshake:
            await channel.send(
                f"Successfully timed out {member.mention} for {userTimeoutTime} minutes."
            )
        else:
            await channel.send("Something went wrong")
        dataManager.deleteViolation(member)


warningLimit = 5
dataManager = data.dataManagment(warningLimit, warningBot)

#variables end


#commands start
#return true if have rights for bot
def HaveRights(member: discord.Member) -> bool:
    return any(role.name == "DiB" for role in member.roles)

    #simple method
    #for role in member.roles:
    #    if role.name == "Dib":
    #        return True
    #return False


@bot.command(name='test',
             help='Just test command to develop bot',
             brief='Just test')
async def roll(ctx):
    #if doesn't have right return
    if not HaveRights(ctx.message.author):
        return
    await ctx.reply('Well, I\'m here')


'''
@bot.command(name="statm", help='', brief='')
async def memberStat(ctx, member):
    if not HaveRights(ctx.message.author):
        return
    await ctx.reply(f'У {member.name} {db[f"violations{member.id}"]} нарушений'
                    )
'''


@bot.command(name='stat',
             help='Shows server/member statistics - [!stat @name]',
             brief='Shows server/member statistics')
async def stat(ctx, arg: discord.Member = None):
    #if doesn't have right return
    if not HaveRights(ctx.message.author):
        return
    print(type(arg))
    if type(arg) is discord.Member:
        embed = discord.Embed(color=amethystColor,
                              title='Member statistics',
                              description=f'')
        embed.add_field(name="Violations", value=dataManager.getViolation(arg))
        await ctx.reply(embed=embed)
        return

    #удаляю сообщение пользователя
    #await bot.delete_message(ctx.message)
    #берем массив пользователей исключая ботов
    #membersArray = [x for x in ctx.guild.members if not x.bot]
    embedStatVar = discord.Embed(title=f'Server statistics',
                                 color=amethystColor)
    membersCount = 0
    countOff = 0
    #проходим по массиву пользователкй проверяя кто в сети (предлагаю сделать это вписанным в embed)
    for member in ctx.guild.members:
        membersCount = membersCount + 1
        if member.status is discord.Status.offline:
            countOff = countOff + 1

    embedStatVar.add_field(name="Members", value=membersCount, inline=False)
    embedStatVar.add_field(name="Online",
                           value=str(membersCount - countOff),
                           inline=True)
    embedStatVar.add_field(name="Offline", value=countOff, inline=True)

    await ctx.reply(embed=embedStatVar)


@bot.command(name="img",
             help='Sends a picture on your topic [!img |your topic|]',
             brief='Return a random fox image')
async def randImg(ctx, *arg):
    target = "%20".join(arg)

    embed = discord.Embed(title='Random Image 😺',
                          description='Random',
                          colour=amethystColor)
    embed.set_image(url=f'https://source.unsplash.com/1280x720/?"{target}"')
    embed.set_footer(text="")
    await ctx.reply(embed=embed)


@bot.command(name='fox',
             help='Send a random fox image',
             brief='Return a random fox image')
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900,
                          title='Random Fox')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.reply(embed=embed)  # Отправляем Embed


@bot.command(name='wink',
             help='Send a random wink image',
             brief='Return a random wink image')
async def wink(ctx):
    response = requests.get(
        'https://some-random-api.ml/animu/wink')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Wink')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.reply(embed=embed)  # Отправляем Embed


@bot.command(name='pat',
             help='Send a random pat image',
             brief='Return a random pat image')
async def pat(ctx):
    response = requests.get(
        'https://some-random-api.ml/animu/pat')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Pat')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.reply(embed=embed)  # Отправляем Embed


@bot.command(name='hug',
             help='Send a random hug image',
             brief='Return a random hug image')
async def hug(ctx):
    response = requests.get(
        'https://some-random-api.ml/animu/hug')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Hug')  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.reply(embed=embed)  # Отправляем Embed


@bot.command(name='quote',
             help='Submit a random anime quote',
             brief='Send a random quote image')
async def quote(ctx):
    response = requests.get(
        'https://some-random-api.ml/animu/quote')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON

    embed = discord.Embed(color=0xff9900, title='Quote')  # Создание Embed'a
    embed.add_field(
        name=json_data['sentence'],
        value=
        f"`Character`:  `{json_data['character']}` \n`Anime`: `{json_data['anime']}`",
        inline=False)  # Устанавливаем картинку Embed'a
    await ctx.reply(embed=embed)  # Отправляем Embed


@bot.command(name='hi', help='Reply hello', brief='Greet the bot')
async def hello(ctx):
    await ctx.reply('hello')


async def timeout_user(*, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {bot.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() +
               datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}

    async with bot.session.patch(url, json=json, headers=headers) as session:
        if session.status in range(200, 299):
            return True
        return False


@bot.command(name='timeout',
             help='Sends to timeout - [!timeout @name time(minutes)]',
             brief='Sends the user to a timeout')
async def timeout(ctx: commands.Context, member: discord.Member, until: int):
    if not HaveRights(ctx.message.author):
        return
    handshake = await timeout_user(user_id=member.id,
                                   guild_id=ctx.guild.id,
                                   until=until)
    if handshake:
        return await ctx.send(
            f"Successfully timed out {member.mention} for {until} minutes.")
    await ctx.send("Something went wrong")


@bot.command(
    name='clearv',
    help=
    'Сleared user violation(s) - [!clearViolation @name all/one]\n\'all\' - clear all user violations\n\'all\' - clear one user violation',
    brief='Сleared user violation(s)')
async def clearViolation(ctx, member: discord.Member, clearType):
    if not HaveRights(ctx.message.author):
        return
    if dataManager.getViolation(member) <= 0:
        embed = discord.Embed(color=greenColor,
                              title='He is clean',
                              description='The user has no violations')
        await ctx.reply(embed=embed)
    elif clearType.isdigit():
        countToClear = int(clearType)
        if dataManager.getViolation(member) <= countToClear:
            dataManager.deleteViolation(member)
            print('all clear')
            embed = discord.Embed(
                color=greenColor,
                title='Сleared all violations',
                description=
                f'{ctx.message.author.mention} cleared all violations from {member.mention}'
            )
            await ctx.reply(embed=embed)
        else:
            dataManager.substructViolation(member, countToClear)
            print(f'cleared {countToClear} violations')
            embed = discord.Embed(
                color=greenColor,
                title=f'cleared {countToClear} violations',
                description=
                f'{ctx.message.author.mention} cleared {countToClear} violations from {member.mention}'
            )
            await ctx.reply(embed=embed)
    elif clearType == 'all':
        dataManager.deleteViolation(member)
        print('all clear')
        embed = discord.Embed(
            color=greenColor,
            title='Сleared all violations',
            description=
            f'{ctx.message.author} cleared all violations from {member.name}')
        await ctx.reply(embed=embed)
    elif clearType == 'one':
        dataManager.substructViolation(member)
        print('one clear')
        embed = discord.Embed(
            color=greenColor,
            title='Сleared one violation',
            description=
            f'{ctx.message.author} cleared one violations from {member.name}')
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(color=redColor,
                              title='Error clear violation',
                              description='Wrong argument was given!')
        embed.set_footer(text='Try "!help clearv" to get help')
        await ctx.reply(embed=embed)


#commands end
@bot.command(name='warning',
             help='Warn the user - [!warnig @name cause]',
             brief='Warn the user')
async def warning(ctx, member: discord.Member, *arg):
    if not HaveRights(ctx.message.author):
        return
    cause = ' '.join(arg)  #соединяем оставшиеся аргументы
    await dataManager.addViolation(member, ctx.channel, cause)
    embed = discord.Embed(
        color=0xff9900,
        title=f'Warning {dataManager.getViolation(member)}/{warningLimit}'
    )  # Создание Embed'a
    #await ctx.message.author.send(f'**Server**: {ctx.message.guild.name}')
    #await ctx.message.author.send(f'**Cause**: {cause}')
    #await ctx.reply(embed=embed)  # Отправляем Embe
    embedUser = discord.Embed(
        color=0xff9900,
        title='Warning',
        description=
        f'```fix\n**{member.name}** attention **{ctx.message.author.name}** warned you!```'
    )  # Создание Embed'a для пользователя
    embedUser.add_field(name='**Server:**',
                        value=f'`{ctx.message.guild.name}`',
                        inline=False)
    embedUser.add_field(name='**Cause:**', value=f'`{cause}`', inline=False)
    #await member.send(embed=embedUser)  # Отправляем Embed пользователю


#custom commands start


#check messages start
async def checkCurse(msg):
    if not msg:
        return
    if SpamChecker.GetPercentage(msg.content) >= 0.8:
        #await msg.delete()
        await msg.channel.send(
            f"{msg.author.mention} you can't use these words here.")
        await dataManager.addViolation(msg.author, msg.channel,
                                       'Bad word usage')


    #для тестов бот будет говорить на сер  вер, после можно заменить, так легче дебажить систему
    #await msg.author.send(f"{msg.author.mention} you can't use these words here.")
async def checkSpam(msg):
    filtered = ''.join(
        filter(
            (''.join(allLetters) + ''.join(allLetters).upper()).__contains__,
            msg.content))

    countLettersAll = len(filtered)
    if countLettersAll == 0:
        return
    countLettersUpper = 0
    for i in filtered:
        if i.isupper():
            countLettersUpper = countLettersUpper + 1

    percentUpper = countLettersUpper / countLettersAll
    print(percentUpper)

    counterAll = 0
    #oneDay = datetime.datetime.utcnow() - datetime.timedelta(hours = 1)
    async for message in msg.channel.history(limit=200):
        if message.author.id == msg.author.id:
            counterAll += 1
    if percentUpper > 0.35 and len(msg.content) > 5:
        await msg.channel.send(
            f"{msg.author.mention} you can't use caps lock words here.")
        await dataManager.addViolation(msg.author, msg.channel,
                                       'Using caps lock')


async def checkMessage(msg):
    await checkCurse(msg)
    await checkSpam(msg)


#check messages end

#custom commands end


#при старте пишем что бот зашёл в аккаунт
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


#делаем что-то при входящем сообщении
@bot.event
async def on_message(message):
    #если это наше сообщение то игнорируем
    if message.author == bot.user:
        return

    if "soiamtheprogrammerdeletemyinfo" in message.content and HaveRights(
            message.author):
        dataManager.deleteViolation(message.author)
        await message.channel.send('Ok, your desire is the law.')
    await checkMessage(message)
    await bot.process_commands(message)


#вызываем этот метод из файла чтобы бот оставался в сети
keep_alive()
#запускаем клиента дискод бота с помощью токена спрятаного в переменных
bot.run(os.environ['TOKEN'])
