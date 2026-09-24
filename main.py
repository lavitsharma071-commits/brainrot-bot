from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Brainrots Data (Name, Raw Value, Display Value, Exist Count, Rarity)
BRAINROTS_DATA = {
    "skibidi toilet": {"val_num": 1000, "value": "1,000", "count": 1500, "rarity": "Common"},
    "grimace shake": {"val_num": 5000, "value": "5,000", "count": 800, "rarity": "Rare"},
    "ohio": {"val_num": 8000, "value": "8,000", "count": 700, "rarity": "Rare"},
    "mewing cat": {"val_num": 12000, "value": "12,000", "count": 500, "rarity": "Epic"},
    "sigma": {"val_num": 18000, "value": "18,000", "count": 400, "rarity": "Epic"},
    "baby gronk": {"val_num": 25000, "value": "25,000", "count": 300, "rarity": "Legendary"},
    "caseoh": {"val_num": 35000, "value": "35,000", "count": 220, "rarity": "Legendary"},
    "kai cenat": {"val_num": 45000, "value": "45,000", "count": 180, "rarity": "Legendary"},
    "livvy dunne": {"val_num": 50000, "value": "50,000", "count": 150, "rarity": "Mythic"},
    "fanum tax": {"val_num": 100000, "value": "100,000", "count": 50, "rarity": "Secret"},
    "rizzler": {"val_num": 250000, "value": "250,000", "count": 10, "rarity": "Godly"},
    "brainrot god": {"val_num": 500000, "value": "500,000", "count": 3, "rarity": "Unique"}
}

user_inventories = {}

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} Slash Command(s)")
    except Exception as e:
        print(f"Syncing Error: {e}")
        
    print(f"✅ Bot Online Ho Gaya Hai: {bot.user.name}")

# --- SLASH COMMAND 1: /brainrots ---
@bot.tree.command(name="brainrots", description="Saare brainrots, unki values aur exist count dekhein")
async def slash_brainrots(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🧠 Steal a Brainrot - Expanded List & Values",
        description="Sabhi brainrots, unki value aur exist count:",
        color=discord.Color.purple()
    )
    for name, info in BRAINROTS_DATA.items():
        embed.add_field(
            name=f"✨ {name.title()}",
            value=f"**Value:** {info['value']} Coins\n**Exist:** {info['count']}\n**Rarity:** {info['rarity']}",
            inline=True
        )
    await interaction.response.send_message(embed=embed)

# --- SLASH COMMAND 2: /exist ---
@bot.tree.command(name="exist", description="Sabhi brainrots ka exist count aur rarity check karein")
async def slash_exist(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📊 Brainrots Exist Count Leaderboard",
        color=discord.Color.dark_teal()
    )
    sorted_items = sorted(BRAINROTS_DATA.items(), key=lambda x: x[1]['count'])
    
    exist_text = ""
    for name, info in sorted_items:
        exist_text += f"• **{name.title()}**: `{info['count']}` exist | Rarity: *{info['rarity']}*\n"
        
    embed.description = exist_text
    await interaction.response.send_message(embed=embed)

# --- SLASH COMMAND 3: /calculate ---
@bot.tree.command(name="calculate", description="Do items ya values ka direct comparison aur difference nikalein")
@app_commands.describe(item1="Pehla item ya value", item2="Doosra item ya value")
async def slash_calculate(interaction: discord.Interaction, item1: str, item2: str):
    k1 = item1.strip().lower()
    k2 = item2.strip().lower()
    
    val1 = BRAINROTS_DATA[k1]["val_num"] if k1 in BRAINROTS_DATA else (int(item1) if item1.isdigit() else None)
    val2 = BRAINROTS_DATA[k2]["val_num"] if k2 in BRAINROTS_DATA else (int(item2) if item2.isdigit() else None)

    if val1 is None or val2 is None:
        await interaction.response.send_message("❌ Invalid items/numbers! Kripya sahi item ka naam ya number likhein.")
        return

    diff = val2 - val1
    percent = (diff / val1 * 100) if val1 > 0 else 0

    embed = discord.Embed(title="🧮 Value Calculator Result", color=discord.Color.blue())
    embed.add_field(name=f"1. {item1.title()}", value=f"**{val1:,}** Coins", inline=True)
    embed.add_field(name=f"2. {item2.title()}", value=f"**{val2:,}** Coins", inline=True)
    
    if diff > 0:
        res = f"🟢 Item 2 is **+{diff:,}** Coins higher (+{percent:.1f}%)"
    elif diff < 0:
        res = f"🔴 Item 2 is **{diff:,}** Coins lower ({percent:.1f}%)"
    else:
        res = "⚖️ Both values are Equal!"

    embed.add_field(name="Difference", value=res, inline=False)
    await interaction.response.send_message(embed=embed)

# --- SLASH COMMAND 4: /check ---
@bot.tree.command(name="check", description="Kisi specific brainrot ki details check karein")
@app_commands.describe(item_name="Brainrot ka naam likhein")
async def slash_check(interaction: discord.Interaction, item_name: str):
    item_key = item_name.lower()
    if item_key in BRAINROTS_DATA:
        info = BRAINROTS_DATA[item_key]
        embed = discord.Embed(title=f"🔍 Item Info: {item_name.title()}", color=discord.Color.green())
        embed.add_field(name="Value", value=f"{info['value']} Coins", inline=False)
        embed.add_field(name="Exist Count", value=f"{info['count']} in existence", inline=False)
        embed.add_field(name="Rarity", value=info['rarity'], inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"❌ `{item_name}` nahi mila! Check karne ke liye `/brainrots` try karein.")

# --- SLASH COMMAND 5: /additem ---
@bot.tree.command(name="additem", description="Apni inventory me item add karein")
@app_commands.describe(item_name="Brainrot ka naam")
async def slash_additem(interaction: discord.Interaction, item_name: str):
    item_key = item_name.lower()
    if item_key not in BRAINROTS_DATA:
        await interaction.response.send_message(f"❌ `{item_name}` exist nahi karta.")
        return

    user_id = interaction.user.id
    if user_id not in user_inventories:
        user_inventories[user_id] = {}

    user_inv = user_inventories[user_id]
    user_inv[item_key] = user_inv.get(item_key, 0) + 1
    await interaction.response.send_message(f"✅ `{item_name.title()}` aapki inventory me add ho gaya!")

# --- SLASH COMMAND 6: /inv ---
@bot.tree.command(name="inv", description="Apni ya kisi member ki inventory dekhein")
@app_commands.describe(member="Member jiski inventory dekhni hai (Optional)")
async def slash_inv(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    user_id = target.id

    if user_id not in user_inventories or not user_inventories[user_id]:
        await interaction.response.send_message(f"🎒 **{target.display_name}** ki inventory khali hai!")
        return

    user_inv = user_inventories[user_id]
    total_value = 0
    inv_text = ""

    for item_key, count in user_inv.items():
        if count > 0:
            item_info = BRAINROTS_DATA[item_key]
            item_total = item_info["val_num"] * count
            total_value += item_total
            inv_text += f"• **{item_key.title()}** x{count} — Value: `{item_total:,}` Coins\n"

    embed = discord.Embed(title=f"🎒 Inventory - {target.display_name}", description=inv_text, color=discord.Color.gold())
    embed.add_field(name="💰 Net Worth", value=f"**{total_value:,} Coins**", inline=False)
    await interaction.response.send_message(embed=embed)

# --- SLASH COMMAND 7: /tradecalc ---
@bot.tree.command(name="tradecalc", description="Trade calculation karein (items comma ',' se alag karein)")
@app_commands.describe(your_items="Aapke items (e.g. rizzler, skibidi toilet)", for_their_items="Unke items (e.g. fanum tax)")
async def slash_tradecalc(interaction: discord.Interaction, your_items: str, for_their_items: str):
    my_list = [i.strip().lower() for i in your_items.split(",")]
    their_list = [i.strip().lower() for i in for_their_items.split(",")]

    my_total = sum(BRAINROTS_DATA[item]["val_num"] for item in my_list if item in BRAINROTS_DATA)
    their_total = sum(BRAINROTS_DATA[item]["val_num"] for item in their_list if item in BRAINROTS_DATA)

    diff = their_total - my_total
    percent = (diff / my_total * 100) if my_total > 0 else 0

    if abs(diff) <= (my_total * 0.05):
        status = "⚖️ FAIR TRADE"
        color = discord.Color.blue()
    elif diff > 0:
        status = f"🟢 WIN (+{diff:,} Coins / +{percent:.1f}%)"
        color = discord.Color.green()
    else:
        status = f"🔴 LOSE ({diff:,} Coins / {percent:.1f}%)"
        color = discord.Color.red()

    embed = discord.Embed(title="📊 Trade Value Calculator", color=color)
    embed.add_field(name="🫵 Your Offer", value=f"**{my_total:,}** Coins\n({your_items})", inline=True)
    embed.add_field(name="🫱 Their Offer", value=f"**{their_total:,}** Coins\n({for_their_items})", inline=True)
    embed.add_field(name="Trade Verdict", value=f"### {status}", inline=False)
    await interaction.response.send_message(embed=embed)
import os

# Server ke environment variable se token uthayega
token = os.getenv("DISCORD_TOKEN")
bot.run(token)


