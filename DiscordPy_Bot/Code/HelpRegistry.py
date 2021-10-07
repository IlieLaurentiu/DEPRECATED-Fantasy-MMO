from DiscordPy_Bot.Code.MainClient import client

category = []
command = []

#make a get method name method

def RegisterCommand(commandName):
    command.append(str(commandName.__name__))
    print(command)


def RegisterCategory(categoryName):
    category.append(str(categoryName.__name__))
    print(category)


def CategoryHelp():
    print("category help")


def CommandHelp():
    print("command help")
