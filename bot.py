import discord
import json

# Opening JSON file
f = open('config.json')
config = json.load(f)
f = open('commands.json')
commands = json.load(f)
f.close()

triggerChar = '!'
for key, value in commands.items():
    commands[key] = '!'+commands[key]

channels = [1018330635829530694]
emojis = {'plus': '\u2795', 'person': '👤', 'thumbsup': '👍',
          'thumbsdown': '👎', 'cycle': '\U0001f504', 'minus': '\u2796'}


class CharacterData():
    def __init__(self, user, isCharacter, init=-99, roll=-99):
        self.user = user
        self.isCharacter = isCharacter
        self.init = init
        self.roll = roll

    def changeInit(self, newValue):
        self.init = newValue

    def changeRoll(self, newValue):
        self.roll = newValue


characters = {}


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel
        if (not channel.id in channels) or (message.author == self.user) or (not message.content[0] == '!'):
            return
        print(
            f'Message from {message.author} in {message.channel.name} ({message.channel.id}): {message.content}')

        # check for commands
        segments = message.content.split()
        print(f'segments: {segments}')
        print(f'displayname: {message.author.display_name}')

        # [!add, init/roll?, name?, value]
        if segments[0] in commands['add']:

            # [!add, value](assumes init)
            if len(segments) == 2:
                if message.author.display_name in characters.keys():
                    if characters[message.author.display_name].init == -99:
                        characters[message.author.display_name].init = int(
                            segments[1])
                        await message.add_reaction(emojis['plus'])
                    else:
                        characters[message.author.display_name].init = int(
                            segments[1])
                        await message.add_reaction(emojis['cycle'])
                else:
                    characters[message.author.display_name] = CharacterData(
                        message.author, False, init=int(segments[1]))
                    await message.add_reaction(emojis['person'])

            # [!add, init/roll, value] or [!add, name, value](assumes init)
            elif len(segments) == 3:
                if segments[1] in characters.keys():
                    if characters[segments[1]].init == -99:
                        characters[segments[1]].init = int(segments[2])
                        await message.add_reaction(emojis['plus'])
                    else:
                        characters[segments[1]].init = int(segments[2])
                        await message.add_reaction(emojis['cycle'])
                elif segments[1] == 'init':
                    if message.author.display_name in characters.keys():
                        if characters[message.author.display_name].init == -99:
                            characters[message.author.display_name].init = int(
                                segments[2])
                            await message.add_reaction(emojis['plus'])
                        else:
                            characters[message.author.display_name].init = int(
                                segments[2])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                elif segments[1] == 'roll':
                    if message.author.display_name in characters.keys():
                        if characters[message.author.display_name].roll == -99:
                            characters[message.author.display_name].roll = int(
                                segments[2])
                            await message.add_reaction(emojis['plus'])
                        else:
                            characters[message.author.display_name].roll = int(
                                segments[2])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                else:
                    characters[segments[1]] = CharacterData(
                        message.author, False, init=int(segments[2]))
                    await message.add_reaction(emojis['person'])

            # [!add, init/roll, name, value]
            elif len(segments) == 4:
                if segments[1] == 'init':
                    if segments[2] in characters.keys():
                        if characters[segments[2]].init == -99:
                            characters[segments[2]].init = int(
                                segments[3])
                            await message.add_reaction(emojis['plus'])
                        else:
                            characters[segments[2]].init = int(
                                segments[3])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        characters[segments[2]] = CharacterData(
                            message.author, False, init=int(segments[3]))
                        await message.add_reaction(emojis['person'])
                if segments[1] == 'roll':
                    if segments[2] in characters.keys():
                        if characters[segments[2]].roll == -99:
                            characters[segments[2]].roll = int(
                                segments[3])
                            await message.add_reaction(emojis['plus'])
                        else:
                            characters[segments[2]].roll = int(
                                segments[3])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        characters[segments[2]] = CharacterData(
                            message.author, False, roll=int(segments[3]))
                        await message.add_reaction(emojis['person'])

        # [!change, init/roll?, name?, value]
        elif segments[0] in commands['change']:
            # same as add but won't add new characters

            if len(segments) == 2:
                if message.author.display_name in characters.keys():
                    characters[message.author.display_name].init = int(
                        segments[1])
                    await message.add_reaction(emojis['cycle'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])
            elif len(segments) == 3:
                if segments[1] in characters.keys():
                    characters[segments[1]].init = int(segments[2])
                    await message.add_reaction(emojis['cycle'])
                elif segments[1] == 'init':
                    if message.author.display_name in characters.keys():
                        characters[message.author.display_name].init = int(
                            segments[2])
                        await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                elif segments[1] == 'roll':
                    if message.author.display_name in characters.keys():
                        characters[message.author.display_name].roll = int(
                            segments[2])
                        await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])
            elif len(segments) == 4:
                if segments[1] == 'init':
                    if segments[2] in characters.keys():
                        characters[segments[2]].init = int(
                            segments[3])
                        await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                if segments[1] == 'roll':
                    if segments[2] in characters.keys():
                        characters[segments[2]].roll = int(
                            segments[3])
                        await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])

        # [!view, init/roll/all?]
        elif segments[0] in commands['view']:

            unenteredOutput = '\n**Pending**:\n'
            output = ''

            # [!view](assumes init)
            if len(segments) == 1:
                initList = []
                for key, value in characters.items():
                    if not value.init in initList:
                        initList.append(value.init)
                initList.sort(reverse=True)
                output += '**Initiative Order**:\n'
                for init in initList:
                    for key, value in characters.items():
                        if init == -99:
                            if value.init == init:
                                unenteredOutput += (f'{key} ')
                        else:
                            if value.init == init:
                                output = output + (f'{key}: {init}\n')

            # [!view, init/roll/all]
            elif len(segments) == 2:
                if segments[1] == 'init':
                    initList = []
                    for key, value in characters.items():
                        if not value.init in initList:
                            initList.append(value.init)
                    initList.sort(reverse=True)
                    output += '**Initiative Order**:\n'
                    for init in initList:
                        for key, value in characters.items():
                            if init == -99:
                                if value.init == init:
                                    unenteredOutput += (f'{key} ')
                            else:
                                if value.init == init:
                                    output = output + (f'{key}: {init}\n')
                elif segments[1] == 'roll':
                    rollList = []
                    for key, value in characters.items():
                        if not value.roll in rollList:
                            rollList.append(value.roll)
                    rollList.sort(reverse=True)
                    output += "**Roll Order**:\n"
                    for roll in rollList:
                        for key, value in characters.items():
                            if roll == -99:
                                if value.roll == roll:
                                    unenteredOutput += (f'{key} ')
                            else:
                                if value.roll == roll:
                                    output = output + (f'{key}: {roll}\n')
                elif segments[1] == 'all':
                    output += '**Characters**:\n'
                for key, value in characters.items():
                    if value.init == -99 and value.roll == -99:
                        unenteredOutput += (
                            f'{key}:\n - isCharacter:{value.isCharacter}\n - user:{value.user}\n\n')
                    else:
                        output += (f'{key}:\n - isCharacter:{value.isCharacter}\n - user:{value.user}\n - init:{value.init}\n - roll:{value.roll}\n')

            if unenteredOutput == '\n**Pending**:\n':
                unenteredOutput = ''
            await channel.send(output+unenteredOutput)

        # [!delete, name?]
        elif segments[0] in commands['delete']:

            # [!delete](assumes display_name)
            if len(segments) == 1:
                if message.author.display_name in characters.keys():
                    characters.pop(message.author.display_name)
                    await message.add_reaction(emojis['minus'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])

            # [!delete, name]
            elif len(segments) == 2:
                if segments[1] in characters.keys():
                    characters.pop(segments[1])
                    await message.add_reaction(emojis['minus'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])
            else:
                await message.add_reaction(emojis['thumbsdown'])

        # [!clear, all/init/roll?]
        elif segments[0] in commands['clear']:  # not working

            # [!clear](assumes non-characters)
            if len(segments) == 1:
                for key in list(characters.keys()):
                    if characters[key].isCharacter:
                        characters[key].init = -99
                        characters[key].roll = -99
                    else:
                        characters.pop(key)
                await message.add_reaction(emojis['minus'])

            # [!clear, all/init/roll]
            elif len(segments) == 2:
                if segments[1] == 'all':
                    for key in list(characters.keys()):
                        characters.pop(key)
                    await message.add_reaction(emojis['minus'])
                elif segments[1] == 'init':
                    for key, value in characters.items():
                        value.init = -99
                    await message.add_reaction(emojis['cycle'])
                elif segments[1] == 'roll':
                    for key, value in characters.items():
                        value.roll = -99
                    await message.add_reaction(emojis['cycle'])

        # [!help, all?]
        elif segments[0] in commands['help']:

            #[!help]
            if len(segments) == 1:
                helpMessage = '**Basic Commands:**\n !add [#] => creates/changes temporary initiative value with your display name\n!add [name] [#] => creates/changes temporary initiative value with given name\n!view => view sorted initiative order\n!help all => shows all variants of the different commands'

            #[!help all]
            elif len(segments) == 2:
                helpMessage = '**All Commands:**\n__!add__\n!add [#] => creates/changes temporary initiative value with your display name\n!add init [#] => creates/changes temporary initiative value with your display name\n!add roll [#] => creates/changes temporary roll value with your display name\n!add [name] [#] => creates/changes temporary initiative value with given name\n!add init [name] [#] => creates/changes temporary initiative value with given name\n!add roll [name] [#] => creates/changes temporary roll value with given name\n\n__!change__\nSame as !add except it safeguards from creating unwanted characters in the list\n\n__!view__\n!view => view sorted initiative order\n!view init => view sorted initiative order\n!view roll=> view sorted roll order\n!view all => view unsorted character data for testing\n\n__!clear__\n!clear => reset initiative and roll values and removes temporary characters\n!clear init => reset initiative values of all characters\n!clear roll=> reset roll values of all characters\n!clear all => remove all characters from the list\n\n__!create__\n!create => creates a permanent character with your display name\n!create [name] => creates a permament character with given name\n\n__!delete__\n!delete => deletes the character with your display name\n!delete [name] => deletes the character with given name\n\n__!help__\n!help => shows basic commands\n!help all => shows all variants of the different commands'
            else:
                helpMessage = 'Sorry. Can\'t help you right now. There is an error.'

            await channel.send(helpMessage)

        # [!create, name?]
        elif segments[0] in commands['create']:

            # [!create](assumes display_name)
            if len(segments) == 1:
                characters[message.author.display_name] = CharacterData(
                    message.author, True)
                await message.add_reaction(emojis['person'])
            # [!create, name]
            elif len(segments) == 2:
                characters[segments[1]] = CharacterData(message.author, True)
                await message.add_reaction(emojis['person'])
            else:
                await message.add_reaction(emojis['thumbsdown'])
        else:
            await message.add_reaction(emojis['thumbsdown'])


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(config['token'])
