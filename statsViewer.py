import os
from pytube import YouTube
import pytube
from stqdm import stqdm
import pandas as pd
from youtubesearchpython import Video, ResultMode
import streamlit as st
import scrapetube
from categoryPredictor import predictCategoryFor
import pandas as pd

@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def generate_channel_video_data(of_channel, with_number_of_videos):
    video_urls = []
    c_id = Video.get(of_channel, mode=ResultMode.json, get_upload_date=True)["channel"]["id"]
    videos = scrapetube.get_channel(c_id)
    i = 0
    for video in videos:
        video_urls.append("https://www.youtube.com/watch?v="+str(video['videoId']))
        i += 1
        if i == with_number_of_videos:
            break

    data = {
        "Title": [],
        "Description": [],
        "Category": [],
        "Is Educational?": [],
        "Beyond Exams Category": [],
    }

    timer = stqdm(video_urls)

    for video in timer:
        timer.set_description("☕️ Have a coffee, while we are generating your dataset.  ")
        try:
            v = Video.get(video, mode = ResultMode.json, get_upload_date=True)
            t = v["title"]
            d = v["description"]
            c = v["category"]
            isEdu, isCat, cat_array, sub_array = predictCategoryFor(video)
            data["Description"].append(d)
            data["Category"].append(c)
            data["Title"].append(t)
            data["Is Educational?"].append(isEdu)
            data["Beyond Exams Category"].append(isCat)
        except Exception as e:
            print(e)
            continue

    df = pd.DataFrame(data)
    st.dataframe(df)
    csv = convert_df(df)

    st.download_button(
        "Download this dataframe",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )

# generate_channel_video_data(of_channel="https://www.youtube.com/channel/UCgHn1lIrwR5AqmqDN-m8wXA", with_number_of_videos=10)