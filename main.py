#Imports
import discord
import os
import requests
import json
import urllib
import random
from replit import db
from keep_alive import keep_alive
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO


#Variables
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


bad_words = [
    "Fuck", "fuck", "Fuck You", "Shit", "Piss off", "Fuck off", "Dick head",
    "Asshole", "Son of a bitch", "Bastard", "Bitch", "Wanker"
]

sad_words = [
    "error", "build failed", "not working", "bug", "failed", "err", "buggy"
]

warning = [
    ">>> ⚠ Please avoid using Swear Words it is against our server policy!",
    ">>> ⚠ Use of Swear Words are against our server policy!",
    ">>> ⚠ Bullying someone using Swear Words are against our server policy!"
]

solution = [
    ">>> 🤔 I think you should find something on stackoverflow !\n💡 Tip: Sharing your project link is also helpful"
]

core_team_1 = [
    ">>> **Core Team** \n1. Lead: Random Name\n2. Co Lead: Random Name\n3. Web Lead: Random Name"
]

help_data = [
     ">>> **Help Commands** \n\nThese are the available commands:\n\n1. `!pdc help` - Dailogue of all commands\n2. `!pdc info` -  Gives info of bot\n3. `!pdc about` -  Returns server information\n4. `!pdc discord` - Provides invitation link for the discord server\n5. `!pdc github` - Provides link to the github organisation\n6. `!pdc core team` - Returns current Core Member\n7. `!pdc list projects` - Returns active projects\n8. `!pdc quote`s - Returns random quote\n9. `!pdc events` - Returns upcoming events\n10. `!pdc new-event` - Add new event\n11. `!pdc delete-event` - Delete an event\n12. `!pdc list-events` - List all events\n13. `!pdc event-syntax` - List all syntax for events command\n14. `!pdc new project` - add new project to the list\n15. `!pdc delete project` - delete a project from the list\n16. `!pdc meme` - Returns meme\n17. `!pdc joke` - Returns a joke\n18. `!pdc search github` - get the github url of a user\n\n _Our bot is Open Source_"
]

event_syntax = [
    "`!pdc new-event | <event-title> | <event_time>`\n`!php delete index_value`"
]

#Setting up function for Quotes
def get_quote():
    response = requests.get(
        "https://zenquotes.io/api/random")  #API uses Random Quotes
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)

#Setting up funcyion for adding events
def new_event(event_title, event_date, event_time):
  new_event = event_title, event_date, event_time
  if "events" in db.keys():
    events = db["events"]
    events.append(new_event)
    db["events"] = events
  else:
    db["events"] = [(new_event)]

def remove_event(index):
  events = db["events"]
  if len(events) > index:
    del events[index]
    db["events"] = events

#Setting up function for adding projects
def newProject(projectTitle, projectType):
  new_project = projectTitle, projectType
  if "projects" in db.keys():
    projects = db["projects"]
    projects.append(new_project)
    db["projects"] = projects
  else:
    db["projects"] = projects

def removeProject(index):
  projects = db["projects"]
  if len(projects) > index:
    del projects[index]
    db["projects"] = projects

#Function to return random meme images URL
def random_meme():
  url =  "https://some-random-api.ml/meme"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  path = data["image"]
  return path

#Function to return random jokes 
def random_joke():
  url = "https://some-random-api.ml/joke"
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  joke = data["joke"]
  return joke

#Setting up fuction for github search
def github_search_user(user_name_to_search):
  response = urllib.request.urlopen("https://api.github.com/users/" + user_name_to_search )
  data = json.loads(response.read())
  #All data from github json
  git_url = data["html_url"]
  github_repos = data["public_repos"]
  user_name = data["login"]
  github_avatar_url = data["avatar_url"]
  github_follower = data["followers"]
  github_bio = data["bio"]
  github_following = data["following"]


  github_resource = [github_url,github_repos,user_name,github_avatar_url,github_follower,github_bio,github_following]
  return github_resource

#Creating Login message
@client.event
async def on_ready():
    print('Bot is now live as {0.user}'.format(client) +
          (' at PHP-DC Discord Server'))


@client.event
async def on_message(message):
    #Variables Ease
    msg = message.content

    #Condition for self texting
    if message.author == client.user:
        return

#Condition help
    if msg.startswith('!pdc help'):
        await message.channel.send(''.join(help_data))

#Condition info
    if msg.startswith('!pdc info'):
        await message.channel.send('>>> PDC Bot v1.0.0')

#Condition about
    if msg.startswith('!pdc about'):
        await message.channel.send(
            '>>> **About** \nPDC is an university based community group for students interested in computer technology. \nStudents from any undergraduate or graduate programs with an interest in growing as a developer can join. \nWe aim in growing knowledge in a peer-to-peer learning environment and build solutions for local businesses and  community.'
        )

#Condition discord
    if msg.startswith('!pdc discord'):
        await message.channel.send('https://discord.gg/Gbanp7fYCZ')

#Condition github
    if msg.startswith('!pdc github'):
        await message.channel.send('https://github.com/PH-DC')

#Condition core team
    if msg.startswith('!pdc core team'):
        await message.channel.send(''.join(core_team_1))

#Condition requesting Quotes
    if msg.startswith('!pdc quote'):
        quote = get_quote()
        await message.channel.send('>>> ' + '_' + quote + '_')

#Condition for using bad words
    if any(word in msg for word in bad_words):
        await message.channel.send(random.choice(warning))

#Condition for using sad words
    if any(word in msg for word in sad_words):

        await message.channel.send(''.join(solution))

#Condition to view all the events currently in the database
    if msg.startswith("!pdc list events"):
        events = db["events"].value
        for event_title, event_date, event_time in events:
          await message.channel.send(" {} | {} | {} ".format(event_title, event_date, event_time))

#Condition for adding an event
    if msg.startswith("!pdc new event"):
        msg_array = msg.split("|")
        event_title = msg_array[1]
        event_date = msg_array[2]
        event_time = msg_array[3]
        new_event(event_title, event_date, event_time)
        await message.channel.send(">>> New event added!")

#Condition for deleting events
    if msg.startswith("!pdc delete event"):
      index = int(msg.split("!pdc delete event",1)[1])
      remove_event(index)
      await message.channel.send(">>> Event Deleted")

#Condition to view all event related syntax
    if msg.startswith("!pdc event-syntax"):
        await message.channel.send('>>> '.join(event_syntax))

#Condition to view projects
    if msg.startswith("!pdc list projects"):
      projects = db["projects"].value
      for projectTitle, projectType in projects:
        await message.channel.send("{} | {} ".format(projectTitle, projectType))

#Condition to Add Projects
    if msg.startswith("!pdc new project"):
      project_msg_array = msg.split("|")
      projectTitle = project_msg_array[1]
      projectType = project_msg_array[2]
      newProject(projectTitle, projectType)
      await message.channel.send(">>> Project Added")

#Condition to Delete Project
    if msg.startswith("!pdc project completed"):
      index = int(msg.split("!pdc project completed",1)[1])
      removeProject(index)
      await message.channel.send(">>> Project Completed")

#Condition to return random meme
    if msg.startswith('!pdc meme'):
      meme = random_meme()
      await message.channel.send(meme)

#Condition to return random jokes
    if msg.startswith('!pdc joke'):
      joke = random_joke()
      await message.channel.send(">>> " + joke)

#Condition to search a user in github
    if msg.startswith('!pdc search github'):
      user_to_be_searched = msg.split(" ",3)[3]
      git_result = github_search_user(user_to_be_searched)

      github_url = git_result[0]
      github_repo_size = str(git_result[1])
      github_user_name = str(git_result[2])
      github_avatar_url = git_result[3]
      github_followers = str(git_result[4])
      github_dis = str(git_result[5])
      github_following = str(git_result[6])
      # Embed for discord
      embed=discord.Embed(description=github_dis, color=0xff1095 )
      embed.set_author(name = github_user_name, url=github_url, icon_url = github_avatar_url)
      embed.add_field(name = "Repository", value = github_repo_size,inline = False)
      embed.add_field(name = "Followers", value=github_followers,inline = True)
      embed.add_field(name = "Following", value=github_following,inline = True)
    
      await message.channel.send(embed=embed)


@client.event
async def on_member_join(member):
  
# server Id 
  guild = client.get_guild(791606163954991144) #(726038923410669578 )
# welcome channel id
  channel = guild.get_channel(791606163954991146 ) #(834028832729858069)

  new_user = member.name

# Opening the welcome banner
  img = Image.open("welcome-04.png")

# Getting the avatar of the currently joined user
  avatar_image = member.avatar_url
  data = BytesIO(await avatar_image.read())
  pfp = Image.open(data)

# Drawing the text to display on the welcome banner, i.e , new user name
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype('Bangers-Regular.ttf',224)
  text = str(new_user)
  draw.text((965, 650),text, (255, 255, 255), font = font)

# creating an mask for avatar to look like a circel cropped image
  size = (512, 512)
  mask = Image.new('L', size, 255)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((0, 0) + size, fill=0)

# Masking out the new user pfp with a circle 
  output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
  output.paste(0, mask=mask)
  output.convert('P', palette=Image.ADAPTIVE)

# Combining the pfp with the banner
  img.paste(output, (337,530))
  img.save('welcome_banner.gif')

# sending the banner in welcome channel
  await channel.send(file = discord.File('welcome_banner.gif'))

# embed to display what they have to do
  embed = discord.Embed(title = "H E Y !  " + new_user, description="Introduce yourself in #🥰-introduce-yourself channel", color=0xff1095)
  embed.set_author(name="PDC", icon_url="https://i.ibb.co/25bJnkk/1.png")

  await channel.send(embed=embed)

#Keep Alive
keep_alive()

client.run(os.getenv('botTOKEN'))
