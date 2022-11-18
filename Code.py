import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.simplefilter(action='ignore', category = FutureWarning)

# Loading the DataSet
df = pd.read_csv("Statics/data.csv")
print(df.head())
print('\n')

# Data Pre-Processing
df.drop('Unnamed: 0', axis = 1, inplace=True)
print(df.head())
print('\n')

print(df.info())
print('\n')

# Checking the number of unique values in each column
dict = {}
for i in list(df.columns):
    dict[i]=df[i].value_counts().shape[0]
print(pd.DataFrame(dict, index=['Unique count']).T)
print('\n')

# Summary Statistics
print(df.describe())
print('\n')

# Classifying data into numerical and categorical variables.
cat_cols = df.select_dtypes(exclude="number").columns.to_list()
print("Categorical Variables:",cat_cols,'\n')

num_cols = df.select_dtypes(include="number").columns.to_list()
print("Numerical Variables:",num_cols,'\n')


data_numerical = df[num_cols]
data_categorical = df[cat_cols]
print(data_categorical.head())
print('\n')
print(data_numerical.head())
print('\n')

# Correlation Matrix And Plot
correlation = data_numerical.corr()
print(correlation)
print('\n')
sns.heatmap(correlation,cmap="Greens_r",annot=True)
plt.show()

# Liked vs. DisLiked Songs
labels = ["Liked Songs"," DisLiked Songs"]
values = df['target'].value_counts().tolist()
plt.pie(values, labels = labels, autopct= '%.1f%%', shadow=True,startangle = 60)
plt.title("Liked/DisLiked Songs Distribution Pie Chart")
plt.show()

# Skewness and kurtosis
s_k = []
for i in data_numerical.columns:
    s_k.append([i,data_numerical[i].skew(),data_numerical[i].kurt()])
skew_kurt=pd.DataFrame(s_k,columns=['Columns','Skewness','Kurtosis'])
print(skew_kurt)
print('\n')

# Numerical Variable Analysis
cols = ['acousticness','danceability','energy','instrumentalness','liveness','speechiness','tempo','loudness','valence']
fig, axes = plt.subplots(3,3)
ax_no = 1
for col in cols:
    plt.subplot(3, 3, ax_no).patch.set_facecolor('#f6f5f7')
    sns.kdeplot(df.loc[(df['target'] == 1), col], color='r',
                fill=True, label='Liked')

    sns.kdeplot(df.loc[(df['target'] == 0), col], color='b',
                fill=True, label='Not Liked')
    plt.legend(['Liked', 'Not Liked'])
    ax_no += 1
fig.suptitle('Kde Plots')
plt.show()

# Subplots of Top Artists, Loudest Songs,Energetic Songs
fig,ax = plt.subplots(3,1)
top_artist_count = df.artist.value_counts()
sns.barplot(x = top_artist_count.values[:6], y= top_artist_count.index[:6], ax = ax[0])
ax[0].set_title('Artists with Most Songs')

top_five_loudest=df[["loudness","song_title"]].sort_values(by="loudness",ascending=True)[:5]
sns.barplot(x="loudness",y="song_title",data=top_five_loudest, ax = ax[1])
ax[1].set_title("Top Five Loudest")

top_ten_energetic=df[["energy","song_title","artist"]].sort_values(ascending=False,by="energy")[:10]
sns.barplot(x="energy",y="song_title",data=top_ten_energetic, ax = ax[2])
ax[2].set_title("Top 10 Energetic Songs")
plt.show()

# More Subplots
fig,ax = plt.subplots(3,1)
top_five_artist_dancebility=df[["danceability","song_title","artist"]].sort_values(by="danceability",ascending=False)[:5]
sns.barplot(x="danceability",y="artist",data=top_five_artist_dancebility,ax=ax[0])
ax[0].set_title("Artist with most danceability song")

duration=df["duration_ms"].value_counts()[:10]
sns.barplot(x=duration.index,y=duration.values,ax=ax[1])
ax[1].set_xlabel("Time_ms")
ax[1].set_title("Most Common Duration")

top_10=df[["song_title","valence"]].sort_values(ascending=False,by="valence")[:10]
sns.barplot(y="song_title",x="valence",data=top_10,ax=ax[2])
ax[2].set_title("Songs with Most Valence")
plt.show()

# EDA
sns.set_palette("viridis_r")
ax_no = 1
for col in num_cols:
    plt.subplot(5, 3, ax_no)
    sns.boxplot(data = df, x=col)
    ax_no += 1
plt.show()

# Exploring Data
sns.set_palette("Blues_r")
ax_no = 1
for col in num_cols:
    plt.subplot(5, 3, ax_no)
    sns.histplot(data = df, x=col, bins=25, kde=True)
    ax_no += 1
plt.show()

continuous_cols = ['acousticness', 'danceability', 'duration_ms', 'energy',
    'liveness', 'loudness',  'tempo',  'valence', 'speechiness', 'instrumentalness']
discrete_cols = ['key','mode','time_signature','target']

# Distributions of Continuous Features
fig, axes = plt.subplots(5,2)
palettes = ['viridis','Set1', 'prism', 'rocket']
axes = axes.flatten()
ax_no = 0
for col in continuous_cols:
    sns.set_palette(palettes[ax_no % 4])
    sns.histplot(data=df, x=col, hue='target', bins=25, kde=True, ax=axes[ax_no])
    ax_no += 1
fig.suptitle('Distributions of Continuous Features')
plt.show()

# Distributions of Discrete Features
sns.set_palette("Set1")
fig, axes = plt.subplots(2,2)
palettes = ['tab10', 'Paired', 'rocket', 'Set1']
axes = axes.flatten()
ax_no = 0
for col in discrete_cols:
    sns.set_palette(palettes[ax_no%4])
    sns.countplot(data = df, x= col, ax = axes[ax_no], hue='target')
    ax_no += 1
fig.suptitle('Distributions of Discrete Features')
plt.show()

# Correlation Analysis
plt.figure()
plt.subplot(3,2,1)
sns.scatterplot(data=df,x=df['acousticness'],y=df['danceability'],hue=df['target'],palette="OrRd",style=df['target'])
plt.title('Scatterplot for acousticness vs danceability')
plt.subplot(3,2,2)
sns.scatterplot(data=df,x=df['duration_ms'],y=df['energy'],hue=df['target'],palette="OrRd",style=df['target'])
plt.title('Scatterplot for duration_ms vs enery')
plt.subplot(3,2,3)
sns.scatterplot(data=df,x=df['instrumentalness'],y=df['liveness'],hue=df['target'],palette="OrRd",style=df['target'])
plt.title('Scatterplot for instrumentalness vs liveness')
plt.subplot(3,2,4)
sns.scatterplot(data=df,x=df['loudness'],y=df['speechiness'],hue=df['target'],palette="OrRd",style=df['target'])
plt.title('Scatterplot for loudness vs speechiness')
plt.subplot(3,2,5)
sns.scatterplot(data=df,x=df['tempo'],y=df['valence'],hue=df['target'],palette="OrRd",style=df['target'])
plt.title('Scatterplot for tempo vs valence')
plt.show()

modified_df = df[['acousticness', 'danceability', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'target']]
sns.pairplot(modified_df.iloc[:,1:], hue="target", palette="plasma", markers=["o", "s"])
plt.show()

