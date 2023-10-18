#Selenium imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

#Other imports here
import os
import wget
from time import sleep
driver = webdriver.Chrome()
driver.get("https://twitter.com/login")

with open('twitter.txt', 'r') as tfile:
    username_text = tfile.readline().strip('\n')
    password_text = tfile.readline().strip('\n')
    
sleep(5)
username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys(username_text)
next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Avançar')]")
next_button.click()

sleep(5)
password = driver.find_element(By.XPATH,"//input[@name='password']")
password.send_keys(password_text)
next_button = driver.find_element(By.XPATH, "//div[@data-testid='LoginForm_Login_Button']")
next_button.click()

subject = '"subject"'

# Search item and fetch it
sleep(3)
search_box = driver.find_element(By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(subject)
search_box.send_keys(Keys.ENTER)

sleep(3)
most_rec = driver.find_element(By.XPATH,"//span[contains(text(),'Mais recentes')]")
most_rec.click()

UserTags=[]
TimeStamps=[]
Tweets=[]
Replys=[]
reTweets=[]
Likes=[]

max_tweets = 100  # Defina o número máximo de tweets desejado

while len(Tweets) < max_tweets:  # Continue até que o número desejado de tweets seja atingido
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    
    for article in articles:
        UserTag = article.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
        UserTags.append(UserTag)
        
        Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
        Tweets.append(Tweet)
        
        Reply = article.find_element(By.XPATH, ".//div[@data-testid='reply']").text
        Replys.append(Reply)
        
        reTweet = article.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
        reTweets.append(reTweet)
        
        Like = article.find_element(By.XPATH, ".//div[@data-testid='like']").text
        Likes.append(Like)
    
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(3)
    
    # Atualize os elementos articles após a rolagem
    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    
    # Use um conjunto (set) para garantir tweets únicos
    Tweets2 = list(set(Tweets))
    
    if len(Tweets2) >= max_tweets:
        break


"""print(len(UserTags),
len(Tweets),
len(Replys),
len(reTweets),
len(Likes))"""
import pandas as pd

df = pd.DataFrame(zip(UserTags,Tweets,Replys,reTweets,Likes),columns=['UserTags','Tweets','Replys','reTweets','Likes'])

df.head()
df.to_excel(r"tweets.xlsx",index=False)