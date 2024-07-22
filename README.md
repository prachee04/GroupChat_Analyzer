# WhatsApp Chat Analyzer

WhatsApp Chat Analyzer is a tool designed to visualize and analyze your WhatsApp chat data. It provides various insights such as message activity over time, most common words, emoji analysis, and user activity heatmaps.

## Live Demo

Check out the live demo of the web application here: [Group Chat Analyzer](https://groupchatanalyzer-python.streamlit.app/)

## Features

- **Message Activity Over Time**: Visualize the number of messages sent over different time periods.
- **Most Common Words**: Identify and display the most frequently used words in the chat.
- **Emoji Analysis**: Analyze and display the usage of emojis.
- **User Activity Heatmaps**: Generate heatmaps to show user activity patterns over time.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- WordCloud

## How It Works

1. **Data Loading**: The app loads WhatsApp chat data from the `.txt` file.
2. **Preprocessing**: The data is cleaned and preprocessed to extract useful information such as timestamps, users, messages, and emojis.
3. **Analysis**: Various analyses are performed on the data to generate insights such as message activity, word frequency, emoji usage, and activity heatmaps.
4. **Visualization**: The results are visualized using charts and graphs for easy interpretation.
