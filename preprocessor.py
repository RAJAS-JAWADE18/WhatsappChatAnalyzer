import re
import pandas as pd


def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s"
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    date = []
    time = []
    for i in dates:
        dt = i.split(", ")
        date.append(dt[0])
        time.append(dt[1].split("\u202f")[0])  # handles narrow no-break space

    df = pd.DataFrame({
        'user_msg': message,
        'date': date,
        'time': time
    })

    user = []
    msg = []
    for i in df['user_msg']:
        entry = re.split(r"([\w\W]+?):\s", i)
        if len(entry) > 2:
            user.append(entry[1])
            msg.append(entry[2])
        else:
            user.append('Group Notification')
            msg.append(entry[0])

    df['user'] = user
    df['msg'] = msg
    df.rename(columns={'msg': 'message'}, inplace=True)

    df.drop(columns=['user_msg'], inplace=True)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = pd.to_datetime(df['time'], errors='coerce').dt.hour
    df['period'] = df['hour'].apply(lambda x: f"{x}-{(x + 1) % 24}")

    return df
