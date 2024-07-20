import extract
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd 
from collections import Counter

def find_urls(text):
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.findall(text)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++ Statistics for a single user ++++++++++++++++++++++++++++++++++++++++++
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #messages
    num_messages = df.shape[0]

    #words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #links
    links = []
    for message in df['message']:
        links.extend(find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head() #top most busy users
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'}) #percentage of business
    return x,df


def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=400,height=400,min_font_size=10,background_color='pink')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    f=open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification'] #to remove group notification messages
    temp = temp[temp['message'] != '<Media omitted>\n'] #to remove media messages

    words = []

    for message in temp['message']: #to remove hinglish words
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df =  pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

