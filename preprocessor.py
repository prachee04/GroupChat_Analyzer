import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'

    messages = re.split(pattern, data)

    # Find all dates in the data
    dates = re.findall(pattern, data)

    # Handle possible leading empty message if the first match was at the start
    if messages[0].strip() == '':
        messages = messages[1:]

    # Re-check lengths after handling leading empty message
    # print(f"Number of messages after adjustment: {len(messages)}")
    # print(f"Number of dates after adjustment: {len(dates)}")

    # Check if the lengths still mismatch
    if len(messages) > len(dates):
        print("There are more messages than dates. Extra messages will be removed.")
        messages = messages[:len(dates)]  # Trim the extra messages
    elif len(dates) > len(messages):
        print("There are more dates than messages. Extra dates will be removed.")
        dates = dates[:len(messages)]  # Trim the extra dates


    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)


    # Split user and message
    users = []
    msgs = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 1:  # user name
            users.append(entry[1])
            msgs.append(entry[2] if len(entry) > 2 else '')
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['user_message'], inplace=True)


    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df