import time


async def testPing(channel):
	await channel.send(".ping")
	chan_history = channel.history()
	#print ("chan_history="+str(chan_history))
	time.sleep(5)
	async for message in channel.history(limit=1):
		if message.author.id == 481894304214941699:
			#print("message.author="+str(message.author))
			#print("message.author.id="+str(message.author.id))
			#print ("message="+str(message))
			#print ("message.id="+str(message.id))
			msg = await channel.get_message(message.id)
			#print ("msg="+str(msg))
			#print ("msg.content="+str(msg.content))
			if str(msg.content) == '```pong!```':
				await channel.send("pong test successful!")
				return 0
			else:
				await channel.send("pong test failed :(")
				return 1

async def testEcho(channel, client):
	my_message = await channel.send('.echo who the hell am i?')
	#print ("my_message="+str(my_message))
	#print ("my_message.author="+str(my_message.author))
	#print ("my_message.author.name="+str(my_message.author.name))
	#print ("my_message.author.id="+str(my_message.author.id))
	chan_history = channel.history()
	#print ("chan_history="+str(chan_history))
	time.sleep(5)
	async for message in channel.history(limit=1):
		if message.author.id == 481894304214941699:
			#print("message.author="+str(message.author))
			#print("message.author.id="+str(message.author.id))
			#print("client="+str(client))
			#print ("message="+str(message))
			#print ("message.id="+str(message.id))
			msg = await channel.get_message(message.id)
			#print ("msg="+str(msg))
			#print ("msg.content=["+str(msg.content)+"]")

			if str(msg.content) == str(my_message.author.name)+' says: who':
				await channel.send("echo test successful!")
				return 0
			else:
				await channel.send("echo test failed :(")
				return 1

async def testHelp(channel):
	await channel.send(".help")
	print("##########\ntestHelp\n##########\n")
	chan_history = channel.history()
	print ("chan_history="+str(chan_history))
	time.sleep(5)
	async for message in channel.history(limit=1):
		if message.author.id == 481894304214941699:
			print("\tmessage.author="+str(message.author))
			print("\tmessage.author.id="+str(message.author.id))
			print ("\tmessage="+str(message))
			for embed in message.embeds:
				print ("\t\tembed="+str(embed))
				print ("\t\tembed.title="+str(embed.title))
				for field in embed.fields:
					print ("\t\t\tfield="+str(field))	
				print ("\t\tembed.type="+str(embed.type))
				print ("\t\tembed.description="+str(embed.description))
				print ("\t\tembed.url="+str(embed.url))
				print ("\t\tembed.timestamp="+str(embed.timestamp))
				print ("\t\tembed.colour="+str(embed.colour))
				print ("\t\tembed.footer="+str(embed.footer))
				print ("\t\tembed="+str(embed))
			print ("\tmessage.id="+str(message.id))
			msg = await channel.get_message(message.id)
			print ("\tmsg="+str(msg))
			print ("\tmsg.content="+str(msg.content))
			if str(msg.content) == '```pong!```':
				await channel.send("pong test successful!")
				return 0
			else:
				await channel.send("pong test failed :(")
				return 1