import scrapetube
import pandas as pd

# Prompt for channel_id
channel_id = input("Enter the Channel_id: ")

# Initialize list for URLs
url_list = []

# Base URL for YouTube videos
base_url = "https://www.youtube.com/watch?v="

# Fetch videos from the channel
videos = scrapetube.get_channel(channel_id)

# Loop through videos and collect URLs
for video in videos:
    video_url = base_url + video['videoId']
    print(video_url)
    url_list.append(video_url)

# Create a DataFrame with collected URLs
dataframe = pd.DataFrame(url_list, columns=["URL"])

# Save DataFrame to an Excel file
dataframe.to_excel("tv9urls.xlsx", index=False)

print("Task is completed")

### Reference:

https://www.youtube.com/watch?v=LUOm0QqL3q8
