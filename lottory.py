import discord
import aiohttp
import json
from discord.ext import commands

bot = commands.Bot(command_prefix = '/')

@bot.event 
async def on_ready() :
	print(f"Bot {bot.user.name} has started")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" /lottory"))

@bot.event
async def on_message(message) :
	await bot.process_commands(message)

async def get_data_url(url) :
	async with aiohttp.ClientSession() as session :
		html = await fetch(session, url)

		return html

async def fetch(session, url) :
	async with session.get(url) as respones :
		return await respones.text()

@bot.command()
async def lottory(ctx) :
	thai = await get_data_url('https://lotto.api.rayriffy.com/latest')
	thai = json.loads(thai)

	e = discord.Embed(
		title = "รายงานผล ฉลากกินแบ่งรัฐบาล (Beta)",
		description = f"ประจำวันที่ {thai['response']['date']}",
		color = 0xFF1493
	)  

	e.add_field(name='รางวัลที่ 1', 
	value=f"{thai['response']['prizes'][0]['number'][0]}")

	e.add_field(name='รางวัลข้างเคียงรางวัลที่ 1', 
	value=f"{thai['response']['prizes'][1]['number'][0]} {thai['response']['prizes'][1]['number'][1]}")

	e.add_field(name='รางวัลที่ 2', 
	value=f"{thai['response']['prizes'][2]['number'][0]} {thai['response']['prizes'][2]['number'][1]} {thai['response']['prizes'][2]['number'][2]} {thai['response']['prizes'][2]['number'][3]} {thai['response']['prizes'][2]['number'][4]}")

	e.add_field(name='เลขหน้า 3 ตัว', 
	value=f"{thai['response']['runningNumbers'][0]['number'][0]} {thai['response']['runningNumbers'][0]['number'][1]}")

	e.add_field(name='เลขท้าย 3 ตัว', 
	value=f"{thai['response']['runningNumbers'][1]['number'][0]} {thai['response']['runningNumbers'][1]['number'][1]}")

	e.add_field(name='เลขท้าย 2 ตัว', 
	value=f"{thai['response']['runningNumbers'][2]['number'][0]}")

	e.set_footer(text=f'📰 ข้อมูลจาก news.sanook.com/lotto\n👨‍💻 พัฒนาบอทโดย Pargorn Ruasijan')

	await ctx.send(embed=e)

bot.run('#ใส่ TOKEN HERE')