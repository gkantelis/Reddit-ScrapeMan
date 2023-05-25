Reddit ScrapeMan is a simple Python script that automatically scrapes posts from specified Reddit subreddits for specified keywords. When a keyword is detected in a new post's title, the script sends an email with the post's title and link to the specified email address.


Setup
Before using the script, you need to set up a Reddit "app" for API access, a Google App Password for email sending, and customize your script configurations.
If you don't have both of these set up, running the program will open up relevant webpages with instructions on how to do so. After you set them up and add your info
to the config.ini file, you'll be able to run the program properly.

Reddit App

Go to the Reddit Apps page while logged into your Reddit account.
Scroll down to the 'Developed Applications' section and click 'Create App' or 'Create Another App'.
Fill in the application details:
'name' can be anything (it's just for your reference).
'App type' should be 'script'.
'description' can be left blank.
'about url' can be left blank.
'redirect uri' should be http://localhost:8000 (this is a placeholder and won't be used).
'permissions' should be 'read'.
Click 'Create app'. Reddit will then provide a 'client_id' and 'client_secret'.
Google App Password

Navigate to the Google App Passwords page while logged into your Google account.
At the bottom, select 'Mail' and 'This computer', then click 'Generate'.
Copy the 16-character password (without spaces) that's generated.
Configuration File

Open the config.ini file in a text editor.
Under the [Credentials] section:
Replace your-email@gmail.com with your own email address.
Replace your-google-app-password with the Google App Password you just generated.
Under the [Reddit] section:
Replace the empty ClientID and ClientSecret fields with the 'client_id' and 'client_secret' from your Reddit app.
Replace keyword1,keyword2,keyword3 with the keywords you want to scrape for, separated by commas.
Replace subreddit1,subreddit2,subreddit3 with the subreddits you want to scrape from, separated by commas.
Usage
To run the script, open a terminal, navigate to the directory containing the script and configuration file, and enter the command python scrapeman.py.

The script will now start scanning the specified subreddits for the specified keywords. When it detects a keyword in a new post's title, it will send an email with the post's title and link to your email address.

If you want to change the keywords, subreddits, or email address, simply edit the config.ini file and save your changes. You do not need to restart the script for changes to take effect.

Troubleshooting
If you encounter any issues or have any questions about using the script, feel free to raise an issue on this repository.