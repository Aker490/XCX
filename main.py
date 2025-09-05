import discord
from discord.ui import Button, View, Modal, TextInput
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import datetime
import pytz
import os
from dotenv import load_dotenv

# โหลด TOKEN จาก .env
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

class SlipWalletModal(Modal, title="SLIPWALLET"):
    name_user = TextInput(label="USERNAME", placeholder="ชื่อผู้โอน", required=True, max_length=50)
    name_me = TextInput(label="NAME", placeholder="ชื่อผู้รับเงิน", required=True, max_length=50)
    phone_me = TextInput(label="PHONE", placeholder="เบอร์ผู้รับ", required=True, max_length=10)
    money = TextInput(label="MONEY", placeholder="จำนวนเงิน", required=True, max_length=4)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        # ข้อมูลที่กรอก
        name_user_id = self.name_user.value 
        name_me_id = self.name_me.value
        phone_me_id = self.phone_me.value
        money_id = self.money.value

        # เวลาปัจจุบัน (Asia/Bangkok)
        thailand_timezone = pytz.timezone('Asia/Bangkok')
        current_time_thailand = datetime.datetime.now(thailand_timezone)
        time = current_time_thailand.strftime("%H:%M:%S")
        day, month, year = current_time_thailand.strftime("%d"), current_time_thailand.strftime("%m"), current_time_thailand.strftime("%Y")

        # โหลดภาพ
        image = Image.open("truemoney.png")
        draw = ImageDraw.Draw(image)

        # โหลดฟอนต์
        font_money = ImageFont.truetype("Lato-Heavy.ttf", 87)
        font_user = ImageFont.truetype("Kanit-ExtraLight.ttf", 48)
        font_me = ImageFont.truetype("Kanit-ExtraLight.ttf", 48)
        font_phone = ImageFont.truetype("Prompt-Light.ttf", 40)
        font_time = ImageFont.truetype("Kanit-Light.ttf", 37)

        # เขียนข้อความลงในภาพ
        draw.text((560, 270), f"{money_id}.00", font=font_money, fill=(44, 44, 44))
        draw.text((302, 485), name_user_id, font=font_user, fill=(0, 0, 0))
        draw.text((302, 648), name_me_id, font=font_me, fill=(0, 0, 0))
        draw.text((302, 720), f"{phone_me_id[:3]}-xxx-{phone_me_id[6:]}", font=font_phone, fill=(80, 80, 80))
        draw.text((781, 885), f"{day}/{month}/{year} {time}", font=font_time, fill=(60, 60, 60))

        # บันทึกไฟล์
        image.save("truemoney_with_text.png")

        # ส่งไฟล์กลับไปยังผู้ใช้
        file = discord.File("truemoney_with_text.png")
        embed = discord.Embed(title="✅ สร้างสลีปปลอมสำเร็จ",description=f"นี่เป็นสลีปปลอมจากข้อมูลที่คุณกรอก",color=0xFCE5CD)
        await interaction.followup.send(embed=embed, file=file, ephemeral=True)

@client.command()
async def slip_wallet(ctx):
    username = ctx.author.display_name  # กำหนดค่าก่อนใช้

    button = Button(label="สลิปวอเล็ท", style=discord.ButtonStyle.grey, emoji="📃")

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(SlipWalletModal())

    button.callback = button_callback
    view = View()
    view.add_item(button)

    embed = discord.Embed(title="\nSLIPWALLET", description=f"**บริการปลอมสลิปวอเล็ท !**", color=0x000000)
    embed.set_author(name=username)
    embed.add_field(name="- 📄 __EXAMPLE ( ตัวอย่าง )__", value="กรอกข้อมูลปลอมเเปลงที่คุณต้องการที่จะกรอกลงไหนช่องกรอก ผู้ใช้จ่ายเงิน,ผู้รับเงิน,เบอร์ผู้รับเงิน,จำนวนเงิน\nเวลากรอกชื่อให้เว้นวรรคชื่อเเละนามสกุลของคุณด้วย ",inline=False)
    embed.set_image(url="https://www.icegif.com/wp-content/uploads/2023/04/icegif-627.gif")

    await ctx.send(embed=embed, view=view)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Streaming(name='ระบบปลอมสลิปวอเล็ท', url='https://www.twitch.tv/kerlf'))

client.run(TOKEN)
