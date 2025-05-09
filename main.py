Email = "Your Email"
Password = "Your Password"
Handle = "Your Handle"
Default_Tweet = """Hey there! I'm an Aspiring Backend Developer
looking to #Connect with folks interested in: 

- Web Development
- Front-end
- Back-end
- Full stack development 
- DevOps
- AI
- Building online
- UI/UX
- Open Source   

Let's connect and grow together #LetsConnect #100DaysOfCode."""

Comment = """Hi, I am an Aspiring Backend Developer
Currently on #100DaysOfCode Python Journey
Let's connect and grow together."""

Reply = """Excellent, Let's Connect."""

import json
from datetime import date


def save_to_json(data, filename):
    """Saving data to a JSON file"""
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file, indent=4)


def read_json(filename):
    """Reading data from a JSON file"""
    with open(f"{filename}.json", "r") as file:
        return json.load(file)


def file_check():
    """Checks if the file exists else create new one"""
    try:
        read_json(filename="twitter")
    except FileNotFoundError:
        twitter_file = {
            "tweet_links": [],
            "last_tweet_date": ""
        }
        save_to_json(data=twitter_file, filename="twitter")


def tweet():
    """Makes a tweet by calling the tweet method, saves the link and progress to the JSON file"""
    twitter_file = read_json(filename="twitter")
    today = f"{date.today()}"
    if twitter_file["last_tweet_date"] < today:
        link = twitter_bot.tweet(tweet=Default_Tweet)
        link_data = {
            "link": link,
            "replied": 0
        }
        twitter_file["tweet_links"].append(link_data)
        twitter_file["last_tweet_date"] = today
        save_to_json(data=twitter_file, filename="twitter")
        print("Link saved")


def like_and_reply():
    """Likes and replies to all links in the JSON file and update its progess"""
    twitter_file = read_json(filename="twitter")
    updated_tweet_links = []  # To store updated list of dictionaries
    for data in twitter_file["tweet_links"]:
        if data["replied"] < 2:
            twitter_bot.like_and_reply(link=data["link"], my_reply=Reply)
            data["replied"] += 1
            updated_tweet_links.append(data)  # Append the updated dictionary to the list

    print("Successfully Replied to all tweets")
    # Update the file with the updated list of dictionaries
    twitter_file["tweet_links"] = updated_tweet_links
    save_to_json(data=twitter_file, filename="twitter")
    print("Updated tweet progress")


file_check()  # Checking if the file exist

# Running the Twitter bot operations
from twitterBot import TwitterBot

twitter_bot = TwitterBot(handle=Handle)  # Initializing the Twitter bot

twitter_bot.login(email=Email, password=Password)
tweet()
twitter_bot.comment(comment_text=Comment)
twitter_bot.follow()
like_and_reply()

twitter_bot.quit()
print("The Twitter bot has been successful")
print("You can run it again in a few hours to grow more follows")
print("See you soon!")
