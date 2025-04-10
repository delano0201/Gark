import discord
import os
from discord.ext import commands
from transformers import pipeline
from PIL import Image
from io import BytesIO
from nudity import Nudity

# Load models
classifier = pipeline("text-classification", model="unitary/toxic-bert")
nsfw_detector = Nudity()

# Set up the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Text moderation
    results = classifier(message.content)
    for result in results:
        if result['label'] == 'toxic' and result['score'] > 0.8:
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message was removed due to toxic content.")
            return

    # Image moderation
    for attachment in message.attachments:
        if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp')):
            img_bytes = await attachment.read()
            img = Image.open(BytesIO(img_bytes)).convert("RGB")
            if nsfw_detector.detect(img):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, your image was removed due to inappropriate content.")
                return

    await bot.process_commands(message)

bot.run(os.getenv("MTM1OTg4Mzg5MTE1MzgzMDE2OQ.GNZp3Z.ctWm7XntZ743EbZlqXteuLNbU0u0a9JnnO6IqA"))
