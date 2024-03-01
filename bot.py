import discord
from discord.ext import commands
from discord.ext.commands import MissingAnyRole
import os
import pandas as pd
import subprocess

BOT_TOKEN = "MTIwODk2NjUxMzcyNjU4Njk0MA.GQ_tip.C8Mg9KidiH7_abZLU2hoYIWQa4-M9sHIITunC4"
CHANNEL_ID = 1209379948519882842
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
allowed_role = "tester"
#---------------------------------------------------------------------------------------------------------------------------------
csv_file = 'teams.csv'
df = pd.DataFrame() #declare df

if not os.path.exists(csv_file): #if teams.csv doesn't exist
    # Create a DataFrame with initial values
    df = pd.DataFrame(columns=['Team', 'Wins', 'Draws', 'Losses', 'Points', 'Manager'])
    df.to_csv(csv_file, index=False)
    print("Created teams.csv")
else:
    df = pd.read_csv(csv_file)

@bot.event
async def on_ready():
    print("Hello! League bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! League bot is ready! Type !cmds to see commands")

@bot.command() #COMMANDS LIST
async def cmds(ctx):
    desc = "__***User Commands:***__\n**!table** - Displays league table\n**!info** *team* - displays team information\n__***LMT Commands:***__\n**!add_team** *team* - Adds a team to the league\n" \
    "**!remove_team** *team* - Removes a team from the league\n**!add_m** *team* *manager* - Adds a new manager to a team\n**!add_w** *team* - Adds a win to a team\n" \
    "**!add_d** *team* - Adds a draw to a team\n**!add_l** *team* - Adds a loss to a team\n**!set_score** *team* *w d l* - Sets the win, draw and loss score for a team\n"
    embed = discord.Embed(title="Commands:", description=desc, color=discord.Color.dark_blue())
    await ctx.send(embed=embed)

@bot.command() #ADD TEAM
@commands.has_any_role(allowed_role)
async def add_team(ctx, team_name):
    global df
    if team_name in df['Team'].values:
        print("Team already exists.")
        message = "Team already added!"
        color = discord.Color.red()
    else:
        new_row = {'Team': team_name, 'Wins': 0, 'Draws': 0, 'Losses':0, 'Points': 0, 'Manager': "No manager assigned"}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(csv_file, index=False)
        print(f"Added team: {team_name}")
        message = f"Added: {team_name}"
        color = discord.Color.dark_purple()
    embed = discord.Embed(description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() # REMOVE TEAM
@commands.has_any_role(allowed_role)
async def remove_team(ctx, team_name):
    global df
    if team_name not in df['Team'].values:
        message = "Team not found."
        color = discord.Color.red()
    else:
        df = df[df['Team'] != team_name]
        df.to_csv(csv_file, index=False)
        print(f"Removed team: {team_name}")
        message = f"Removed team: {team_name}"
        color = discord.Color.dark_red()
    embed = discord.Embed(description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() #SET SCORE
@commands.has_any_role(allowed_role)
async def set_score(ctx, team_name, w, d, l):
    global df
    if team_name not in df['Team'].values:
        message = "Team not found."
        color = discord.Color.red()
    else:
        idx = df.index[df['Team'] == team_name].tolist()[0]
        df.loc[idx, 'Wins'] = int(w)
        df.loc[idx, 'Draws'] = int(d)
        df.loc[idx, 'Losses'] = int(l)
        df.loc[idx, 'Points'] = int(w) * 3 + int(d)
        df.to_csv(csv_file, index=False)
        message=f"Set score for {team_name}"
        color=discord.Color.blue()
    embed = discord.Embed(description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() #ADD MANAGER
@commands.has_any_role(allowed_role)
async def add_m(ctx, team_name, m_name):
    global df
    if team_name not in df['Team'].values:
        message = "Team not found."
        color = discord.Color.red()
    else:
        idx = df.index[df['Team'] == team_name].tolist()[0]
        df.loc[idx, 'Manager'] = m_name
        df.to_csv(csv_file, index=False)
        message=f"Changed manager for {team_name} to {m_name}"
        color=discord.Color.dark_purple()
    embed = discord.Embed(description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() #ADD WIN
@commands.has_any_role(allowed_role)
async def add_w(ctx, team_name):
    global df
    if team_name not in df['Team'].values:
        message = "Team not found."
        color = discord.Color.red()
    else:
        idx = df.index[df['Team'] == team_name].tolist()[0]
        df.loc[idx, 'Wins'] += 1
        df.loc[idx, 'Points'] += 3
        df.to_csv(csv_file, index=False)
        message=f"Win added for {team_name}"
        color=discord.Color.green()
    embed = discord.Embed(description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() #ADD DRAW
@commands.has_any_role(allowed_role)
async def add_d(ctx, team_name):
    global df
    if team_name not in df['Team'].values:
        message = "Team not found."
        color = discord.Color.red()
    else:
        idx = df.index[df['Team'] == team_name].tolist()[0]
        df.loc[idx, 'Draws'] += 1
        df.loc[idx, 'Points'] += 1
        df.to_csv(csv_file, index=False)
        message=f"Draw added for {team_name}"
        color=discord.Color.light_grey()
    embed = discord.Embed(description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() #ADD LOSS
@commands.has_any_role(allowed_role)
async def add_l(ctx, team_name):
    global df
    if team_name not in df['Team'].values:
        message = "Team not found."
        color = discord.Color.red()
    else:
        idx = df.index[df['Team'] == team_name].tolist()[0]
        df.loc[idx, 'Losses'] += 1
        df.to_csv(csv_file, index=False)
        message=f"Loss added for {team_name}"
        color=discord.Color.dark_red()
    embed = discord.Embed(description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() #TEAM INFO
async def info(ctx, team_name):
    global df
    if team_name not in df['Team'].values:
        message = "Team not found."
        color = discord.Color.red()
    else:
        idx = df.index[df['Team'] == team_name].tolist()[0]
        message = f"Team: {team_name}\nManager: {df.loc[idx, 'Manager']}\nPoints: {df.loc[idx, 'Points']}\nWins: {df.loc[idx, 'Wins']}\nDraws: {df.loc[idx, 'Draws']}\nLosses: {df.loc[idx, 'Losses']}"
        color=discord.Color.dark_purple()
    embed = discord.Embed(title="Team information:", description=message, color=color)
    await ctx.send(embed=embed)

@bot.command() #SHOW LEAGUE TABLE
async def table(ctx):
    subprocess.run(["python", "league_table.py"])
    embed = discord.Embed(title="League Table :cold_face:", color=discord.Color.dark_purple())
    file = discord.File("league_table.png", filename="league_table.png")
    embed.set_image(url="attachment://league_table.png")
    await ctx.send(embed=embed, file=file)

bot.run(BOT_TOKEN)
