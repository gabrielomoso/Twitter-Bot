import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip


class TwitterBot:

    def __init__(self, handle):
        """Initialize TwitterBot with the provided handle"""

        self.handle = handle
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.home = "https://www.twitter.com"
        self.driver.get(self.home)
        self.wait = WebDriverWait(self.driver, 10)  # 10 seconds timeout (adjust as needed)

    def login(self, email: str, password: str):
        """Method to log in to Twitter with the provided email and password"""
        print("Attempting the login...")

        time.sleep(5)
        # Click the sign-in link
        sign_in = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a')))
        sign_in.click()

        time.sleep(10)
        # Enter email
        username = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                     '//*[@id="layers"]/div['
                                                                     '2]/div/div/div/div/div/div[2]/div['
                                                                     '2]/div/div/div[2]/div[2]/div/div/div/div['
                                                                     '5]/label/div/div[2]/div/input')))
        username.send_keys(email)
        # Click next
        next_button = self.driver.find_element(By.XPATH,
                                               '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div['
                                               '2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
        next_button.click()

        # try:
        #     authentication = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')))
        # except selenium.common.exceptions.NoSuchElementException or selenium.common.exceptions.TimeoutException:
        #     print("No authentication... Moving on")
        # else:
        #     authentication.send_keys(self.handle)
        #     auth_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
        #     auth_button.click()

        # Enter password
        password_label = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                           '//*[@id="layers"]/div['
                                                                           '2]/div/div/div/div/div/div[2]/div['
                                                                           '2]/div/div/div[2]/div[2]/div[1]/div/div/div['
                                                                           '3]/div/label/div/div[2]/div[1]/input')))
        password_label.send_keys(password)
        # Click login
        log_in = self.driver.find_element(By.XPATH,
                                          '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div['
                                          '2]/div[2]/div[2]/div/div[1]/div/div/div')
        log_in.click()
        print("Login successful")

        time.sleep(20)

    def scroll(self):
        """Method to Scroll down the page
        Note: Not to be called outside the class"""

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Add a short delay to allow content to load

    def tweet(self, tweet):
        """This Method makes a Tweet and Returns the Tweet's link"""
        print("Starting the Tweet app")

        # Locate and input tweet content
        content = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                    '//*[@id="react-root"]/div/div/div['
                                                                    '2]/main/div/div/div/div/div/div[3]/div/div['
                                                                    '2]/div[1]/div/div/div/div[2]/div['
                                                                    '1]/div/div/div/div/div/div/div/div/div/div'
                                                                    '/label/div[1]/div/div/div/div/div/div['
                                                                    '2]/div/div/div/div')))
        content.send_keys(tweet)
        # Click post tweet button
        post_button = self.driver.find_element(By.XPATH,
                                               '//*[@id="react-root"]/div/div/div['
                                               '2]/main/div/div/div/div/div/div[3]/div/div[2]/div['
                                               '1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div['
                                               '3]/div/span/span')
        time.sleep(1)
        post_button.click()
        print("Tweet has been posted successfully!")

        # Get link to the posted tweet
        self.driver.get(f"{self.home}/{self.handle}")
        time.sleep(5)
        recent_post = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
        like = recent_post.find_element(By.CSS_SELECTOR, 'div[data-testid="like"]')
        like.click()
        time.sleep(1)
        share_button = recent_post.find_element(By.CSS_SELECTOR, 'div[aria-label="Share post"]')
        share_button.click()
        time.sleep(2)
        copy_link_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="Dropdown"] div[role="menuitem"]')))
        copy_link_button.click()
        time.sleep(1)
        print("Copied Tweet Link")
        return pyperclip.paste()

    def follow(self):
        """Method to follow users who follow the specified account"""
        print("Starting the Follow app")

        self.driver.get(f"{self.home}/{self.handle}/followers")
        time.sleep(10)
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            followers = self.wait.until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] div[role="button"] div[role="button"]')))
            for follower in followers:
                if follower.text == "Follow":
                    try:
                        follower.click()
                    except selenium.common.exceptions.ElementClickInterceptedException:
                        print("Could not click follow... Moving on")
                    time.sleep(1)

            self.scroll()
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                print("Reached the end of the page")
                break
            prev_height = new_height

        print("Successfully Followed all Followers")


    def like_and_reply(self, link: str, my_reply: str):
        """Method to like and reply to tweets"""
        print('Starting the "Like and Reply" app')

        self.driver.get(link)
        time.sleep(5)
        visited_article = []
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            replies = self.wait.until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'article')))

            for replied in replies[1::]:
                if replied not in visited_article:
                    visited_article.append(replied)
                    try:
                        time.sleep(2)
                        like = replied.find_element(By.CSS_SELECTOR, 'div[data-testid="like"]')
                    except selenium.common.exceptions.NoSuchElementException:
                        print("Already liked... Moving on")
                    else:
                        like.click()
                        reply = replied.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
                        if reply.text != my_reply:
                            reply_button = replied.find_element(By.CSS_SELECTOR, 'div[data-testid="reply"]')
                            reply_button.click()
                            time.sleep(2)
                            modal = self.wait.until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-labelledby="modal-header"]')))
                            post_text = modal.find_element(By.CSS_SELECTOR, 'div[aria-label="Post text"]')
                            post_text.send_keys(my_reply)
                            post_button = modal.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButton"]')
                            time.sleep(1)
                            post_button.click()
                            time.sleep(2)

            self.scroll()
            time.sleep(2)
            more_replies = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"] div[role="button"]')
            for more in more_replies:
                if more.text == "Show more replies" or more.text == "Show":
                    more.click()
                    time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                print("Reached the end of the page")
                break
            prev_height = new_height

        print("Successfully Replied to all tweets")

    def comment(self, comment_text):
        """Method to comment on tweets"""
        print("Starting the comment app")

        self.driver.get("https://twitter.com/search?q=%23letsconnect&src=typed_query&f=live")
        time.sleep(5)
        visited_articles = []  # Set to keep track of visited articles
        while len(visited_articles) <= 20:  # Assuming you want to interact with 20 unique articles
            articles = self.wait.until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]')))
            for article in articles:
                if article not in visited_articles:
                    visited_articles.append(article)  # Add current article to visited set
                    try:
                        time.sleep(2)
                        like_button = article.find_element(By.CSS_SELECTOR, 'div[data-testid="like"]')
                    except selenium.common.NoSuchElementException:
                        print("Already Liked this post, moving on...")
                    except selenium.common.exceptions.StaleElementReferenceException:
                        pass
                    else:
                        try:
                            like_button.click()
                        except selenium.common.exceptions.ElementClickInterceptedException:
                            print("Could not click like, Moving on...")
                        else:
                            reply_button = article.find_element(By.CSS_SELECTOR, 'div[data-testid="reply"]')
                            reply_button.click()
                            time.sleep(5)
                            try:
                                modal = self.wait.until(
                                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-labelledby="modal-header"]')))
                            except selenium.common.exceptions.TimeoutException:
                                print("Could not comment... Moving on")
                            else:
                                comment_box = modal.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
                                comment_box.send_keys(comment_text)
                                post_button = modal.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButton"]')
                                time.sleep(1)
                                post_button.click()
                                time.sleep(2)

            self.scroll()  # Scroll after interacting with each batch of articles
            time.sleep(3)
        print("Successfully Commented on 20 posts")

    def quit(self):
        self.driver.quit()