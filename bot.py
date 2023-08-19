import discord
import json

# Opening JSON file
f = open('config.json')
config = json.load(f)
f = open('commands.json')
commands = json.load(f)
f.close()

# triggerChar = '!'
# for key, value in commands.items():
#     newCommands = []
#     for command in value:
#         commands[key] = newCommands.append('!'+command)

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
        self.characters = {}
        print(f'Logged on as {self.user}!')
        

    async def on_message(self, message):
        channel = message.channel
        if (not channel.id in channels) or (message.author == self.user) or (not message.content[0] == '!'):
            return
        print(
            f'Message from {message.author} in {message.channel.name} ({message.channel.id}): {message.content}')

        if message.author.display_name in self.characters.keys() and self.characters[message.author.display_name] == "":
            self.characters[message.author.display_name] = message.author.display_name
            await message.add_reaction(emojis['person'])

        # check for commands
        segments = message.content.split()
        # print(f'segments: {segments}')
        # print(f'displayname: {message.author.display_name}')

        # [!add, init/roll?, name?, value]
        if segments[0] in commands['add']:

            # [!add, value](assumes init)
            if len(segments) == 2:
                if message.author.display_name in self.characters.keys():
                    if self.characters[message.author.display_name].init == -99:
                        self.characters[message.author.display_name].init = int(
                            segments[1])
                        await message.add_reaction(emojis['plus'])
                    else:
                        self.characters[message.author.display_name].init = int(
                            segments[1])
                        await message.add_reaction(emojis['cycle'])
                else:
                    self.characters[message.author.display_name] = CharacterData(
                        message.author, False, init=int(segments[1]))
                    await message.add_reaction(emojis['person'])

            # [!add, init/roll, value] or [!add, name, value](assumes init)
            elif len(segments) == 3:
                if segments[1] in self.characters.keys():
                    if self.characters[segments[1]].init == -99:
                        self.characters[segments[1]].init = int(segments[2])
                        await message.add_reaction(emojis['plus'])
                    else:
                        self.characters[segments[1]].init = int(segments[2])
                        await message.add_reaction(emojis['cycle'])
                elif segments[1] == 'init':
                    if message.author.display_name in self.characters.keys():
                        if self.characters[message.author.display_name].init == -99:
                            self.characters[message.author.display_name].init = int(
                                segments[2])
                            await message.add_reaction(emojis['plus'])
                        else:
                            self.characters[message.author.display_name].init = int(
                                segments[2])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        self.characters[message.author.display_name] = CharacterData(
                            message.author, False, init=int(segments[2]))
                        await message.add_reaction(emojis['thumbsdown'])
                elif segments[1] == 'roll':
                    if message.author.display_name in self.characters.keys():
                        if self.characters[message.author.display_name].roll == -99:
                            self.characters[message.author.display_name].roll = int(
                                segments[2])
                            await message.add_reaction(emojis['plus'])
                        else:
                            self.characters[message.author.display_name].roll = int(
                                segments[2])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        self.characters[message.author.display_name] = CharacterData(
                            message.author, False, roll=int(segments[2]))
                        await message.add_reaction(emojis['thumbsdown'])
                else:
                    self.characters[segments[1]] = CharacterData(
                        message.author, False, init=int(segments[2]))
                    await message.add_reaction(emojis['person'])

            # [!add, init/roll, name, value]
            elif len(segments) == 4:
                if segments[1] == 'init':
                    if segments[2] in self.characters.keys():
                        if self.characters[segments[2]].init == -99:
                            self.characters[segments[2]].init = int(
                                segments[3])
                            await message.add_reaction(emojis['plus'])
                        else:
                            self.characters[segments[2]].init = int(
                                segments[3])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        self.characters[segments[2]] = CharacterData(
                            message.author, False, init=int(segments[3]))
                        await message.add_reaction(emojis['person'])
                if segments[1] == 'roll':
                    if segments[2] in self.characters.keys():
                        if self.characters[segments[2]].roll == -99:
                            self.characters[segments[2]].roll = int(
                                segments[3])
                            await message.add_reaction(emojis['plus'])
                        else:
                            self.characters[segments[2]].roll = int(
                                segments[3])
                            await message.add_reaction(emojis['cycle'])
                    else:
                        self.characters[segments[2]] = CharacterData(
                            message.author, False, roll=int(segments[3]))
                        await message.add_reaction(emojis['person'])

        # [!change, init/roll?, name?, value]
        elif segments[0] in commands['change']:
            # same as add but won't add new self.characters

            if len(segments) == 2:
                if message.author.display_name in self.characters.keys():
                    self.characters[message.author.display_name].init = int(
                        segments[1])
                    await message.add_reaction(emojis['cycle'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])
            elif len(segments) == 3:
                if segments[1] in self.characters.keys():
                    self.characters[segments[1]].init = int(segments[2])
                    await message.add_reaction(emojis['cycle'])
                elif segments[1] == 'init':
                    if message.author.display_name in self.characters.keys():
                        self.characters[message.author.display_name].init = int(
                            segments[2])
                        await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                elif segments[1] == 'roll':
                    if message.author.display_name in self.characters.keys():
                        self.characters[message.author.display_name].roll = int(
                            segments[2])
                        await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])
            elif len(segments) == 4:
                if segments[1] == 'init':
                    if segments[2] in self.characters.keys():
                        self.characters[segments[2]].init = int(
                            segments[3])
                        await message.add_reaction(emojis['cycle'])
                    else:
                        await message.add_reaction(emojis['thumbsdown'])
                if segments[1] == 'roll':
                    if segments[2] in self.characters.keys():
                        self.characters[segments[2]].roll = int(
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
                for key, value in self.characters.items():
                    if not value.init in initList:
                        initList.append(value.init)
                initList.sort(reverse=True)
                output += '**Initiative Order**:\n'
                for init in initList:
                    for key, value in self.characters.items():
                        if init == -99:
                            if value.init == init:
                                unenteredOutput += (f'{key}, ')
                        else:
                            if value.init == init:
                                output = output + (f'{key}: {init}\n')

            # [!view, init/roll/all]
            elif len(segments) == 2:
                if segments[1] == 'init':
                    initList = []
                    for key, value in self.characters.items():
                        if not value.init in initList:
                            initList.append(value.init)
                    initList.sort(reverse=True)
                    output += '**Initiative Order**:\n'
                    for init in initList:
                        for key, value in self.characters.items():
                            if init == -99:
                                if value.init == init:
                                    unenteredOutput += (f'{key}, ')
                            else:
                                if value.init == init:
                                    output = output + (f'{key}: {init}\n')
                elif segments[1] == 'roll':
                    rollList = []
                    for key, value in self.characters.items():
                        if not value.roll in rollList:
                            rollList.append(value.roll)
                    rollList.sort(reverse=True)
                    output += "**Roll Order**:\n"
                    for roll in rollList:
                        for key, value in self.characters.items():
                            if roll == -99:
                                if value.roll == roll:
                                    unenteredOutput += (f'{key}, ')
                            else:
                                if value.roll == roll:
                                    output = output + (f'{key}: {roll}\n')
                elif segments[1] == 'all':
                    output += '**Characters**:\n'
                    for key, value in self.characters.items():
                        if value.init == -99 and value.roll == -99:
                            unenteredOutput += (
                                f'{key}:\n\tisCharacter:{value.isCharacter}\n\tuser:{value.user}\n')
                        else:
                            output += (
                                f'{key}:\n\tisCharacter:{value.isCharacter}\n\tuser:{value.user}\n\tinit:{value.init}\n\troll:{value.roll}\n')

            if unenteredOutput == '\n**Pending**:\n':
                unenteredOutput = ''
            await channel.send(output+unenteredOutput[:-1])

        # [!delete, name?]
        elif segments[0] in commands['delete']:

            # [!delete](assumes display_name)
            if len(segments) == 1:
                if message.author.display_name in self.characters.keys():
                    self.characters.pop(message.author.display_name)
                    await message.add_reaction(emojis['minus'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])

            # [!delete, name]
            elif len(segments) == 2:
                if segments[1] in self.characters.keys():
                    self.characters.pop(segments[1])
                    await message.add_reaction(emojis['minus'])
                else:
                    await message.add_reaction(emojis['thumbsdown'])
            else:
                await message.add_reaction(emojis['thumbsdown'])

        # [!clear, all/init/roll?]
        elif segments[0] in commands['clear']:  # not working

            # [!clear](assumes non-self.characters)
            if len(segments) == 1:
                for key in list(self.characters.keys()):
                    if self.characters[key].isCharacter:
                        self.characters[key].init = -99
                        self.characters[key].roll = -99
                    else:
                        self.characters.pop(key)
                await message.add_reaction(emojis['minus'])

            # [!clear, all/init/roll]
            elif len(segments) == 2:
                if segments[1] == 'all':
                    for key in list(self.characters.keys()):
                        self.characters.pop(key)
                    await message.add_reaction(emojis['minus'])
                elif segments[1] == 'init':
                    for key, value in self.characters.items():
                        value.init = -99
                    await message.add_reaction(emojis['cycle'])
                elif segments[1] == 'roll':
                    for key, value in self.characters.items():
                        value.roll = -99
                    await message.add_reaction(emojis['cycle'])

        # [!help, all?]
        elif segments[0] in commands['help']:

            #[!help]
            if len(segments) == 1:
                with open('basicinstructions.txt', 'r') as f:
                    helpMessage = ''.join(f.readlines())
            #[!help all]
            elif len(segments) == 2:
                with open('instructions.txt', 'r') as f:
                    helpMessage = ''.join(f.readlines())
            else:
                helpMessage = 'Sorry. Can\'t help you right now. There is an error.'

            await channel.send(helpMessage)

        # [!create, name?]
        elif segments[0] in commands['create']:

            # [!create](assumes display_name)
            if len(segments) == 1:
                self.characters[message.author.display_name] = CharacterData(
                    message.author, True)
                await message.add_reaction(emojis['person'])
            # [!create, name]
            elif len(segments) > 1:
                self.characters[" ".join(segments[1:])] = CharacterData(
                    message.author, True)
                await message.add_reaction(emojis['person'])
            else:
                await message.add_reaction(emojis['thumbsdown'])
        # [!save]
        elif segments[0] in commands['save']:

            try:
                fileName = ''

                # [!save]
                if len(segments) == 1:
                    fileName = 'players'
                
                # [!save, fileName](fileName may have spaces)
                if len(segments) > 1:
                    fileName = " ".join(segments[1:])

                fileName = fileName + '.txt'

                with open(fileName, 'w') as f:
                    f.flush()
                    f.write('\n'.join(self.characters.keys()))
                await message.add_reaction(emojis["thumbsup"])
            except:
                await message.add_reaction(emojis["thumbsdown"])
        

        # [!load]
        elif segments[0] in commands['load']:

            names = []
            fileMessage = "Characters added:" + " (use '!clear all' to remove)\n"

            try:
                # [!load]
                if len(segments) == 1:
                    with open('players.txt', 'r') as f:
                        names = f.readlines()

                # [!load, file]
                if len(segments) > 1:
                    with open(" ".join(segments[1:])+'.txt', 'r') as f:
                        names = f.readlines()

                self.characters = {}
                for name in names:
                    if name[-1] == '\n':
                        name = name[:-1]
                    if name == "":
                        continue

                    self.characters[name] = CharacterData('file', True)
                
                await message.add_reaction(emojis["thumbsup"])
                await channel.send(fileMessage + ', '.join(self.characters.keys()))
            except Exception:
                self.characters = {}
                await message.add_reaction(emojis["thumbsdown"])

        else:
            await message.add_reaction(emojis['thumbsdown'])

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(config['token'])
