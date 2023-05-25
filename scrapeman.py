import configparser
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox
import threading
import praw
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Check if the configuration file exists
if not os.path.exists('config.ini'):
    # If it doesn't exist, create it
    config = configparser.ConfigParser()

    config['Credentials'] = {
        'Email': 'your-email@gmail.com',
        'Google App Password': 'your-google-app-password'
    }

    config['Reddit'] = {
        'ClientID': '',
        'ClientSecret': '',
        'Keywords': 'keyword1,keyword2,keyword3',
        'Subreddits': 'subreddit1,subreddit2,subreddit3'
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Read configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

# Check Google App Password
if config['Credentials']['Google App Password'] == 'your-google-app-password':
    # Open Google App Password page and instructions
    webbrowser.open('https://myaccount.google.com/apppasswords')
    with open('google_app_instructions.txt', 'w') as f:
        f.write("To create a Google App Password:\n"
                "1. Make sure you have 2-Step Verification turned on for your Google Account.\n"
                "2. Navigate to https://myaccount.google.com/apppasswords\n"
                "3. At the bottom, select 'Mail' and 'This computer', then click 'Generate'.\n"
                "4. Copy the 16-character password (without spaces) that's generated.\n"
                "5. Enter this in the 'Google App Password' field in 'config.ini'.")
    webbrowser.open('google_app_instructions.txt')

# Check Reddit App credentials
if config['Reddit']['ClientID'] == '' or config['Reddit']['ClientSecret'] == '':
    # Open Reddit app page and instructions
    webbrowser.open('https://www.reddit.com/prefs/apps')
    with open('reddit_app_instructions.txt', 'w') as f:
        f.write("To create a Reddit app:\n"
                "1. Log in to your Reddit account.\n"
                "2. Navigate to https://www.reddit.com/prefs/apps\n"
                "3. Scroll down to the 'Developed Applications' section and click 'Create App' or 'Create Another App'.\n"
                "4. Fill in the application details:\n"
                "    - 'name' can be anything (it's just for your reference).\n"
                "    - 'App type' should be 'script'.\n"
                "    - 'description' can be left blank.\n"
                "    - 'about url' can be left blank.\n"
                "    - 'redirect uri' should be http://localhost:8000 (this is a placeholder and won't be used).\n"
                "    - 'permissions' should be 'read'.\n"
                "5. Click 'Create app'.\n"
                "After creating the application, Reddit will provide the 'client_id' and 'client_secret'.\n"
                "Enter these in the 'ClientID' and 'ClientSecret' fields in 'config.ini'.")
    webbrowser.open('reddit_app_instructions.txt')

reddit = praw.Reddit(client_id=config['Reddit']['ClientID'], 
                     client_secret=config['Reddit']['ClientSecret'], 
                     user_agent='ScrapeMan')

keywords = config['Reddit']['Keywords'].split(',')
email = config['Credentials']['Email']
google_app_password = config['Credentials']['Google App Password']

def send_email(subject, body, to):
    print('Preparing to send an email...')
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = 'ScrapeBot New Report'
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], google_app_password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print('Email sent!')

# Create a list of relevant subreddit names
relevant_subreddits = config['Reddit']['Subreddits'].split(',')

def search_keywords():
    for subreddit_name in relevant_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.stream.submissions():
            print(f"Checking post titled '{submission.title}'")
            for keyword in keywords:
                if keyword in submission.title:
                    print('Keyword found in new submission. Preparing to send an email...')
                    send_email("New Reddit Post about Alpha Chi", 
                               f"Title: {submission.title}\nLink: https://reddit.com{submission.permalink}", 
                               email)
            time.sleep(1)

# Send a test email when the script starts
send_email("Test Email", "This is a test email from your Reddit scraping script.", email)

while True:
    try:
        search_keywords()
    except Exception as e:
        print(e)
        time.sleep(180)
