# Twitter Bot

This project is a Python-based Twitter bot that uses the Selenium library to automate various Twitter interactions. The bot can log in to a Twitter account, post tweets, follow users who follow the account, and like and reply to its own previously posted tweets.

## Features

*   **Login**: Securely logs into a specified Twitter account.
*   **Tweet**: Posts a predefined tweet. It ensures that only one tweet is posted per day.
*   **Follow Back**: Navigates to the account's followers list and follows back users.
*   **Like and Reply**: Likes and replies to tweets previously posted by the bot. It keeps track of replies to avoid excessive interaction.
*   **Data Persistence**: Uses a `twitter.json` file to store information about posted tweets (links, reply counts) and the date of the last tweet.

## Project Structure

```
.
├── main.py           # Main script to run the bot and orchestrate operations.
├── twitterBot.py     # Contains the TwitterBot class with Selenium automation logic.
├── twitter.json      # Stores data like tweet links and last tweet date (created automatically).
└── README.md         # This file.
```

## How It Works

### `main.py`

*   **Configuration**: Sets Twitter credentials (email, password, handle) and default text for tweets, comments, and replies.
*   **JSON Helpers**: Includes functions (`save_to_json`, `read_json`) to manage data in `twitter.json`.
*   **File Check**: The `file_check()` function ensures `twitter.json` exists, creating it with a default structure if it's missing.
*   **Bot Orchestration**:
    1.  Initializes the `TwitterBot` from `twitterBot.py`.
    2.  Calls `twitter_bot.login()` to sign in.
    3.  The `tweet()` function:
        *   Checks `twitter.json` to see if a tweet was already made today.
        *   If not, it calls `twitter_bot.tweet()` to post the `Default_Tweet`.
        *   Saves the new tweet's link and reply status to `twitter.json`.
    4.  Calls `twitter_bot.comment()` to post a predefined comment.
    5.  Calls `twitter_bot.follow()` to follow back users.
    6.  The `like_and_reply()` function:
        *   Iterates through tweet links stored in `twitter.json`.
        *   If a tweet hasn't reached its reply limit (currently 2), it calls `twitter_bot.like_and_reply()`.
        *   Updates the reply count in `twitter.json`.
    7.  Calls `twitter_bot.quit()` to close the browser.

### `twitterBot.py`

This file defines the `TwitterBot` class, which handles all direct interactions with the Twitter website using Selenium:

*   **`__init__(self, handle)`**: Initializes the Selenium WebDriver (Chrome) and sets the Twitter handle.
*   **`login(self, email, password)`**: Automates the login process on Twitter.
*   **`scroll(self)`**: Helper method to scroll the current page to load dynamic content.
*   **`tweet(self, tweet)`**: Types and posts a tweet, then navigates to the user's profile to copy the link of the new tweet (using `pyperclip`).
*   **`follow(self)`**: Navigates to the followers page and clicks the "Follow" button for users not already followed. It scrolls to load all followers.
*   **`like_and_reply(self, link, my_reply)`**: Navigates to a given tweet link, likes it, and posts a reply. (Implementation details for this method were partially complete in the provided code).
*   **`comment(self, comment_text)`**: Intended to post a comment. (Implementation details for this method were partially complete in the provided code).
*   **`quit(self)`**: Closes the Selenium WebDriver.

### `twitter.json`

This file is automatically created and managed by `main.py`. It stores:

*   `tweet_links`: A list of objects, where each object contains:
    *   `link`: The URL of a tweet posted by the bot.
    *   `replied`: A counter for how many times the bot has replied to this tweet.
*   `last_tweet_date`: A string representing the date (YYYY-MM-DD) of the last tweet made by the bot.

## Prerequisites

*   Python 3.x
*   Google Chrome browser installed.
*   ChromeDriver: Download the ChromeDriver executable that matches your Chrome version and ensure it's in your system's PATH or specify its location in `twitterBot.py`.
*   Required Python packages:
    *   `selenium`
    *   `pyperclip`

    You can install them using pip:
    ```bash
    pip install selenium pyperclip
    ```

## Setup and Usage

1.  **Clone the repository or download the files.**
2.  **Install Prerequisites**: Make sure Python, Chrome, ChromeDriver, and the required Python packages are installed.
3.  **Configure Credentials**:
    *   Open `main.py`.
    *   Update the following global variables with your actual Twitter account details:
        ```python
        Email = "Your Email"
        Password = "Your Password"
        Handle = "Your Handle" # Your Twitter @username without the @
        ```
    *   Optionally, customize the `Default_Tweet`, `Comment`, and `Reply` string variables in `main.py`.
4.  **Run the Bot**:
    Execute the `main.py` script from your terminal:
    ```bash
    python main.py
    ```

The bot will then launch Chrome, log in, and perform the programmed actions.

## Demo

Check out a video demonstration of this bot in action on LinkedIn:
[Twitter Bot Demo](https://www.linkedin.com/posts/gabzcode_letsconnect-letsconnect-100daysofcode-activity-7178304954661543937-iuzF?utm_source=share&utm_medium=member_desktop&rcm=ACoAADvWKnEBodmd-RwKXHR3tvderBPAbFceE5k)

## Important Notes

*   **Web Scraping and Automation**: Automating social media interactions can be against the terms of service of platforms like Twitter. Use this bot responsibly and at your own risk. Frequent or aggressive automation might lead to account restrictions.
*   **Selectors**: The bot relies on XPATH and CSS selectors to find elements on Twitter's pages. These selectors can change if Twitter updates its website structure, which might break the bot. If the bot stops working, these selectors in `twitterBot.py` would be the first place to check and update.
*   **Error Handling**: The current error handling is basic. For more robust operation, additional error handling and logging could be implemented.
*   **`time.sleep()`**: The script uses `time.sleep()` for delays. While sometimes necessary, relying heavily on fixed sleep times can make the bot slower than needed or unreliable if pages load slower or faster than expected. Selenium's explicit waits (`WebDriverWait`) are used in many places, which is good practice, but some `time.sleep()` calls might be optimizable.
