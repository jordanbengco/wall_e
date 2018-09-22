import discord
import asyncio
import random
import json
import requests
import sys
from testing_files.HealthChecks_Test import testPing, testEcho, testHelp
client = discord.Client()



async def background_loop():
	#print(1)
	await client.wait_until_ready()
	#print(2)
	#print(client)
	keepLooping=True
	exit = 0
	while not client.is_closed() and keepLooping:
		#print(3)
		channel = client.get_channel(478433247643303938)
		#print("channel="+str(channel))
		exit = await testPing(channel)
		newExit = await testEcho(channel, client)
		if exit == 1 and newExit == 0:
			exit = 1
		else:
			exit = newExit

		newExit = await testHelp(channel)
		if exit == 1 and newExit == 0:
			exit = 1
		else:
			exit = newExit


		#print("closing client")
		keepLooping = False
		#print("client closed")
	channel = client.get_channel(478433247643303938)
	await channel.send("All tests completed")
	if exit == 0:
		await channel.send("All Tests Passed :)")
	else:
		await channel.send("Failures Detected :|")

client.loop.create_task(background_loop())
client.run('NDkyNzgwNTIyMTg4MDQ2MzM2.DobZMQ.AerseNsCf4dk9qd8gUEt7zXEWOc')


# https://discordpy.readthedocs.io/en/rewrite/api.html#discord.abc.Messageable.history
# https://discordpy.readthedocs.io/en/rewrite/api.html#discord.utils.get
# https://discordpy.readthedocs.io/en/rewrite/migrating.html
# https://discordpy.readthedocs.io/en/rewrite/migrating.html
# https://discordpy.readthedocs.io/en/rewrite/api.html#client