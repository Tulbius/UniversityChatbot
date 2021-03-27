import discord
import re
import univ as univ
import random
import recommender as reco


default_intents = discord.Intents.default()
default_intents.members = True
client = discord.Client(intents=default_intents)
countries = univ.get_countries()
universities = univ.get_universities()

@client.event
async def on_ready():
    print("Universe is ready for you !")

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(825429594248314970)
    await general_channel.send(f"Welcome on this server **{member.display_name}** ! 🤖\n "
                               "\n"
                               f"I can help you find information about any **universities** in the world 🎓🌎 \n "
                               "\n"
                               f"You can either look for a specific **country** or name. "
                               f"I can also **recommend** you universities according to your profile, I am happy to help 😇"
                               "\n"
                               "\n"
                               f"Universe ❤"
                               )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    else:
        msgText = message.content.lower()
        if re.search("hello|hi|hey|salut|bonjour|morning|evening", message.content.lower()):
            await message.channel.send("Hello dear friend ! Tell me what you need 👂")

        elif re.search("bye|see|thanks", message.content.lower()):
            await message.channel.send("You are leaving so soon 🥺 \n"                    
                                       "Thank you for having me ! Always a pleasure to help 🥰")

        elif re.search("help|lost|bug", message.content.lower()):
            await message.channel.send("Hey don't worry, here is what I can do for you : \n"
                                       "\n"
                                       "1 - If you type a **country** name, I'll give you 5 random universities of this country (as you understand, if you type the same country several times, you'll get different results every time 😉)\n"
                                       "2 - If you type a **university** name, I'll give you the following information : Name,Country,Domains,Website (you have to give the exact name 🙃)\n"
                                       "3 - If you type **recommender**, follow my lead ! 😏")

        elif re.search("searching|information|find|looking", message.content.lower()):
            await message.channel.send("Of course ! Are you looking for a specific **country**, a **university** name or are you lost and need my **help** ? 😉")

        elif re.search("country", message.content.lower()):
            await message.channel.send("Which **country** is it ? 🧐")

        elif re.search("univ|university|universities|school", message.content.lower()):
            await message.channel.send("Which **university** is it ? 🧐")

        elif msgText in countries:
            randomlist = [random.randint(1, len(univ.search_by_country(msgText))) for i in range(0, 5)]
            for i in randomlist:
                await message.channel.send(univ.search_by_country(msgText)[i].name)
        elif msgText.lower() in universities:
            await message.channel.send(univ.search_by_univ(msgText))

        elif re.search("recommender", message.content.lower()):
            reco.delete(reco.authentication())
            await message.channel.send("https://forms.gle/CgjzjjjnPC6cTfsQ7")
            await message.channel.send("Once it's done type **done**, **finish** or **result** !!")

        elif re.search("done|finish|result", message.content.lower()):
            result = reco.result()
            for item in result:
                await message.channel.send(item)
            await message.channel.send("If you want another recommendation, please type again **recommender** ! 🔁")

        else:
            await message.channel.send("Sorry I don't understand you 🥴\nPlease type **help** if you need ! ")