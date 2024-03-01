import pandas as pd
import matplotlib.pyplot as plt

# Read data from teams.csv file
df = pd.read_csv('teams.csv')

# Sort the DataFrame based on the 'Points' column in descending order
df = df.sort_values(by='Points', ascending=True)

# Reset the index and add 1 to get ranks
df = df.reset_index(drop=True)
df.insert(0, 'Rank', range(len(df), 0, -1))

# Remove the 'Manager' column from the DataFrame
df = df.drop(columns=['Manager'])

fig = plt.figure(figsize=(10, 7), facecolor='#1A0531')  # Set figure background color
ax = plt.subplot()

ncols = len(df.columns)
nrows = len(df)

ax.set_xlim(0, ncols)
ax.set_ylim(0, nrows + 0.7)

columns = df.columns

# Add table's main text
for i in range(nrows):
    for j, column in enumerate(columns):
        if column == 'Points' or column == 'Team':
            text_label = f'{df[column].iloc[i]}'
            weight = 'bold'
        else:
            text_label = f'{df[column].iloc[i]}'
            weight = 'normal'
        ax.annotate(
            xy=(j + 0.5, i + 0.5),
            text=text_label,
            ha='center',
            va='center',
            weight=weight,
            color='#FF1493',  # Neon pink text color
            fontsize=14
        )

# Add column names
for index, c in enumerate(columns):
    ax.annotate(
        xy=(index + 0.5, nrows + 0.25),
        text=c,
        ha='center',
        va='bottom',
        weight='bold',
        color='#FF1493',  # Neon pink text color
        fontsize=14
    )

# Add dividing lines
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [nrows, nrows], lw=1.5, color='#FF1493', marker='', zorder=4)
ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [0, 0], lw=1.5, color='#FF1493', marker='', zorder=4)
for x in range(1, nrows):
    ax.plot([ax.get_xlim()[0], ax.get_xlim()[1]], [x, x], lw=1.15, color='#FF1493', ls=':', zorder=3, marker='')

# Set background color
ax.set_facecolor('#1A0531')  # Dark purple background color

ax.set_axis_off()
plt.savefig('league_table.png', dpi=300, transparent=False, bbox_inches='tight')
#plt.show()
