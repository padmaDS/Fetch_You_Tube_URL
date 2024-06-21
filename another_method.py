import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your internet speed
internet_speed = 1

# Define the URL of the YouTube channels' video page
channels = [
    'https://www.youtube.com/@krishnaik06/videos'
]

# Create a list to store video information
video_info = []

# Iterate through the YouTube Channel lists to go over them one by one:
for channel in channels:
    logging.info(f"Processing channel: {channel}")
    
    # Initialize Selenium WebDriver with WebDriver Manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    # Open the channel URL
    driver.get(channel)

    # Scroll the page until no new videos are loaded
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    scroll_pause_time = internet_speed  # seconds

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        # Wait to load the page
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the updated page source
    updated_page_source = driver.page_source

    # Close the web driver
    driver.quit()

    # Parse the updated HTML content with BeautifulSoup
    soup = BeautifulSoup(updated_page_source, 'html.parser')

    # Try multiple selectors to find video elements
    selectors = [
        {'name': 'Using yt-simple-endpoint class', 'selector': 'a.yt-simple-endpoint.style-scope.ytd-rich-grid-media'},
        {'name': 'Using id attribute', 'selector': 'a#video-title'},
        {'name': 'Using CSS selector', 'selector': 'a#video-title-link'}
    ]
    
    video_tags = []
    for method in selectors:
        video_tags = soup.select(method['selector'])
        if video_tags:
            logging.info(f"Videos found using selector: {method['name']}")
            break

    if not video_tags:
        logging.warning("No video tags found. The HTML structure may have changed.")

    # Iterate through the video elements and extract information
    for video_tag in video_tags:
        video_title = video_tag.get('title')
        video_url = video_tag.get('href')

        if video_title and video_url:
            video_url = 'https://www.youtube.com' + video_url
            logging.info(f"Found video: {video_title} - {video_url}")
            video_info.append(f"{video_title}\t{video_url}")
        else:
            logging.warning("Missing title or URL attribute in video tag.")

# Write the video information to a text file
with open('video_info.txt', 'w', encoding='utf-8') as output_file:
    for entry in video_info:
        output_file.write(entry + '\n')

logging.info("Video information has been saved to video_info.txt")
logging.info(f"Total videos found: {len(video_info)}")
