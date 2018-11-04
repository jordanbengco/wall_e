from discord.ext import commands
import logging
import requests as req
import aiohttp
from helper_files.embed import embed 
from helper_files.Paginate import paginateEmbed
import helper_files.settings as settings
import json
from main import wolframAPI, wolframClient
import discord.client
import urllib.parse

logger = logging.getLogger('wall_e')


class Misc():

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def poll(self, ctx, *questions):
		logger.info("[Misc poll()] poll command detected from user "+str(ctx.message.author))
		name = ctx.author.display_name
		ava = ctx.author.avatar_url

		if len(questions) > 12:
			logger.info("[Misc poll()] was called with too many options.")
			eObj = embed(title='Poll Error', author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description='Please only submit a maximum of 11 options for a multi-option question.')
			await ctx.send(embed=eObj)
			return
		elif len(questions) == 1:
			logger.info("[Misc poll()] yes/no poll being constructed.")
			eObj = embed(title='Poll', author=name, avatar=ava, description=questions[0])
			post = await ctx.send(embed=eObj)
			await post.add_reaction(u"\U0001F44D")
			await post.add_reaction(u"\U0001F44E")
			logger.info("[Misc poll()] yes/no poll constructed and sent to server.")
			return
		if len(questions) == 2:
			logger.info("[Misc poll()] poll with only 2 arguments detected.")
			eObj = embed(title='Poll Error', author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description='Please submit at least 2 options for a multi-option question.')
			await ctx.send(embed=eObj)
			return
		elif len(questions) == 0:
			logger.info("[Misc poll()] poll with no arguments detected.")
			eObj = embed(title='Usage', author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description='.poll <Question> [Option A] [Option B] ...')
			await ctx.send(embed=eObj)
			return
		else:
			logger.info("[Misc poll()] multi-option poll being constructed.")
			questions = list(questions)
			optionString = "\n"
			numbersEmoji = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
			numbersUnicode = [u"0\u20e3", u"1\u20e3", u"2\u20e3", u"3\u20e3", u"4\u20e3", u"5\u20e3", u"6\u20e3", u"7\u20e3", u"8\u20e3", u"9\u20e3", u"\U0001F51F"]
			question = questions.pop(0)
			options = 0
			for m, n in zip(numbersEmoji, questions):
				optionString += m + ": " + n +"\n"
				options += 1
			
			content = [['Options:', optionString]]
			eObj = embed(title='Poll:', author=name, avatar=ava, description=question, content=content)
			pollPost = await ctx.send(embed=eObj)

			logger.info("[Misc poll()] multi-option poll message contructed and sent.")
			for i in range(0, options):
				await pollPost.add_reaction(numbersUnicode[i])
			logger.info("[Misc poll()] reactions added to multi-option poll message.")

	@commands.command()
	async def urban(self, ctx, *arg):
		logger.info("[Misc urban()] urban command detected from user "+str(ctx.message.author)+" with argument =\""+str(arg)+"\"")
		logger.info("[Misc urban()] query string being contructed")
		queryString = ''
		for x in arg:
			queryString += x + '%20'
		queryString = queryString[:len(queryString)-3]
		
		url = 'http://api.urbandictionary.com/v0/define?term=%s' % queryString
		logger.info("[Misc urban()] following url  constructed for get request =\""+str(url)+"\"")
		

		res = req.get(url)
		logger.info("[Misc urban()] Get request made =\""+str(res)+"\"")
		
		if(res.status_code != 404):
			logger.info("[Misc urban()] Get request successful")			
			data = res.json()
		else:
			logger.info("[Misc urban()] Get request failed, 404 resulted")
			data = ''

		data = data['list']
		if not data:
			logger.info("[Misc urban()] sending message indicating 404 result")
			eObj = embed(title="Urban Results", author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, colour=0xfd6a02, description=":thonk:404:thonk:You searched something dumb didn't you?")
			await ctx.send(embed=eObj)
			return
		else:
			logger.info("[Misc urban()] constructing embed object with definition of \"" + queryString+"\"")
			urbanUrl = 'https://www.urbandictionary.com/define.php?term=%s' % queryString
			content = [
				['Definition', data[1]['definition']], 
				['Link', '[here](%s)' % urbanUrl]
				]
			eObj = embed(title='Results from Urban Dictionary', author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, colour=0xfd6a02, content=content)
			await ctx.send(embed=eObj)

	@commands.command()
	async def wolfram(self, ctx, *arg):
		arg = " ".join(arg)
		logger.info("[Misc wolfram()] wolfram command detected from user "+str(ctx.message.author)+" with argument =\""+str(arg)+"\"")
		logger.info("[Misc wolfram()] URL being contructed")

		inputs = [
			('appid', wolframAPI),
			('input', arg),
			('format', 'plaintext'), # no images
			('output', 'json'), # json rather than xml
			('latlong', '49.276765,-122.917957') # for a location-based question, use SFU location
		]

		human_input = [('i', arg)] # build the link that will be displayed in the message
		human_query = urllib.parse.urlencode(human_input)
		human_url = 'https://www.wolframalpha.com/input/?' + human_query

		async with aiohttp.ClientSession() as session:
			async with session.get(
					'https://api.wolframalpha.com/v2/query',
					params=inputs) as res:
				if res.status == 200:
					json_res = await res.json(content_type=None) # bypass check: wolfram doesnt set content-type to json
					text_res = '\n'.join([
                        subpod['plaintext']
                        for pod
                        in json_res['queryresult']['pods']
                        if pod['title'] == 'Result' or pod['primary'] == True
                        for subpod
                        in pod['subpods']
                    ])
					text = "`" + text_res + "`" + "\n\n[Link](%s)" % human_url
					logger.info("[Misc wolfram()] result found for %s" % arg)
				else:
					text = "No results found. :thinking: \n\n[Link](%s)" % human_url
					logger.info("[Misc wolfram()] result NOT found for %s (Status Code %s)" % (arg, res.status))
				content = [['Results from Wolfram Alpha', text]]
				eObj = embed(author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, colour=0xdd1100, content=content)
				await ctx.send(embed=eObj)

	@commands.command()
	async def help(self, ctx):
		numberOfCommandsPerPage=5
		await ctx.send("     help me.....")
		logger.info("[Misc help()] help command detected from "+str(ctx.message.author))
		logger.info("[Misc help()] attempting to load command info from help.json")
		with open('commands_to_load/help.json') as f:
			helpDict = json.load(f)
		logger.info("[Misc help()] loaded commands from help.json=\n"+str(json.dumps(helpDict, indent=3)))
		
		# determing the number of commands the user has access to.
		numberOfCommands=0
		for entry in helpDict['commands']:
			if entry['access'] == "role": ## if the access for the command is determined on the role of the user
				if entry['role'] == "Bot_manager" and ctx.message.author in discord.utils.get(ctx.guild.roles, name="Bot_manager").members:
					if 'Class' not in entry['name']:
						numberOfCommands += 1
				elif entry['role'] == "Minions" and (ctx.message.author in discord.utils.get(ctx.guild.roles, name="Bot_manager").members or ctx.message.author in discord.utils.get(ctx.guild.roles, name="Minions").members):
					if 'Class' not in entry['name']:
						numberOfCommands += 1					
				elif entry['role'] == "public":
					if 'Class' not in entry['name']:
						numberOfCommands += 1
			elif entry['access'] == "channel": ## if the access for the command is determined on permissions
			## in the channel that the help comamnd was called from, rather than generic role permissions
				if entry['channel'] in (item[0] for item in list(ctx.channel.permissions_for(ctx.message.author))):
					if 'Class' not in entry['name']:
						numberOfCommands += 1	

		logger.info("[Misc help()] numberOfCommands set to "+str(numberOfCommands))
		descriptionToEmbed=[""]
		x, page = 0, 0;
		for entry in helpDict['commands']:
			if entry['access'] == "role":
				if entry['role'] == "Bot_manager" and ctx.message.author in discord.utils.get(ctx.guild.roles, name="Bot_manager").members:
					if 'Class' in entry['name']:
						logger.info("[Misc help()] adding "+str(entry)+" to page "+str(page)+" of the descriptionToEmbed")
						descriptionToEmbed[page]+="\n**"+entry['name']+"**: "+"\n"
					else:
						logger.info("[Misc help()] adding "+str(entry)+" to page "+str(page)+" of the descriptionToEmbed")					
						descriptionToEmbed[page]+="*"+entry['name']+"* - "+entry['description']+"\n\n"
						x+=1
						if x == numberOfCommandsPerPage:
							descriptionToEmbed.append("")
							page+=1
							x = 0					
				elif entry['role'] == "Minions" and (ctx.message.author in discord.utils.get(ctx.guild.roles, name="Bot_manager").members or ctx.message.author in discord.utils.get(ctx.guild.roles, name="Minions").members):
					if 'Class' in entry['name']:
						logger.info("[Misc help()] adding "+str(entry)+" to page "+str(page)+" of the descriptionToEmbed")
						descriptionToEmbed[page]+="\n**"+entry['name']+"**: "+"\n"					
					else:
						logger.info("[Misc help()] adding "+str(entry)+" to page "+str(page)+" of the descriptionToEmbed")
						descriptionToEmbed[page]+="*"+entry['name']+"* - "+entry['description']+"\n\n"
						x+=1
						if x == numberOfCommandsPerPage:
							descriptionToEmbed.append("")
							page+=1
							x = 0
				elif entry['role'] == "public":
					logger.info("[Misc help()] adding "+str(entry)+" to page "+str(page)+" of the descriptionToEmbed")
					if 'Class' in entry['name']:
						logger.info("[Misc help()] adding "+str(entry)+" to page "+str(page)+" of the descriptionToEmbed")
						descriptionToEmbed[page]+="\n**"+entry['name']+"**: "+"\n"
					else:
						descriptionToEmbed[page]+="*"+entry['name']+"* - "+entry['description']+"\n\n"
						x+=1
						if x == numberOfCommandsPerPage:
							descriptionToEmbed.append("")
							page+=1
							x = 0
			elif entry['access'] == "channel":
				if entry['channel'] in (item[0] for item in list(ctx.channel.permissions_for(ctx.message.author)) if item[1]):
					logger.info("[Misc help()] adding "+str(entry)+" to page "+str(page)+" of the descriptionToEmbed")					
					descriptionToEmbed[page]+="*"+entry['name']+"* - "+entry['description']+"\n\n"
					x+=1
					if x == numberOfCommandsPerPage:
						descriptionToEmbed.append("")
						page+=1
						x = 0				
			else:
				logger.info("[Misc help()] "+str(entry)+" has a wierd access level of "+str(entry['access'])+"....not sure how to handle it so not adding it to the descriptionToEmbed")
		logger.info("[Misc help()] transfer successful")

		await paginateEmbed(self.bot, ctx, descriptionToEmbed, title="Help Page" )

def setup(bot):
	bot.add_cog(Misc(bot))
