from random import randint
from time import sleep
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get


pages = np.arange(0, 199,
                  1)
#initialize empty lists to store the variables scraped
titles = []
years = []
ratings = []
platforms = []
user_scores = []

userAgent = {'User-agent': 'Mozilla/5.0'}

for page in pages:

    # get request for games
    response = get("https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?"
                   + "page="
                   + str(page),
                   headers=userAgent)

    sleep(randint(5, 10))
    # parse the content of current iteration of response
    page_html = BeautifulSoup(response.text, 'html.parser')
    movie_containers = page_html.find_all('td', class_="clamp-summary-wrap")
    # extract the 100 games for that page
    for container in movie_containers:
        # conditional for all with metascore
        if container.find('a', class_="title") is not None:

            # title
            title = container.h3.text
            titles.append(title)
            print(title)
        else:
            years.append(
                None)

        if container.find('div', class_="clamp-details") is not None:
            # year released
            year = container.find('div', class_="clamp-details").find_all('span')
            years.append(list(year)[2])
            print(list(year)[2])

        else:
            years.append(
                None)

        if container.find('div', class_="clamp-score-wrap") is not None:
            try:
                # rating positive
                rating = container.find('div', class_="metascore_w large game positive").text
                ratings.append(rating)
                print(rating)

            except AttributeError:
                #rating mixed
                if container.find('div', class_="metascore_w large game mixed") is not None:
                    rating = container.find('div', class_="metascore_w large game mixed").text
                    ratings.append(rating)
                    print(rating)
                #rating negative
                else:
                    rating = container.find('div', class_="metascore_w large game negative").text
                    ratings.append(rating)
                    print(rating)

        else:
            ratings.append("")

        if container.find('div', class_="clamp-details") is not None:

            # platform
            platform = container.find('span', class_="data").text
            platforms.append(platform.strip().strip("\n"))
            print(platform)
        else:
            platforms.append(None)
        if container.find('div', class_="clamp-userscore") is not None:
            try:
                # user score
                user_score = container.find('div', class_="metascore_w user large game positive").text
                user_scores.append(user_score)
                print(user_score)

            except AttributeError:
                #user score mixed
                if container.find('div', class_="metascore_w user large game mixed") is not None:
                    user_score = container.find('div', class_="metascore_w user large game mixed").text
                    user_scores.append(user_score)
                    print(user_score)
                    #if user score is tbd
                elif container.find('div', class_="metascore_w user large game tbd") is not None:
                    user_scores.append(str('5.0'))
                #user score negative
                else:
                    user_score = container.find('div', class_="metascore_w user large game negative").text
                    user_scores.append(user_score)
                    print(user_score)

#cleaning up results
x = 0
while x < len(years):
    years[x] = years[x].text.strip('<span></')
    years[x].split(',')
    a = years[x].split(',')
    years[x] = a[1]
    platforms[x] = platforms[x].strip(' ')
    b = user_scores[x].split('.')
    user_scores[x] = b[0] + b[1]
    x = x + 1

#creating DF
games_df = pd.DataFrame({'title': titles,
                         'year': years,
                         'rating': ratings,
                         'user_score': user_scores,
                         'platform': platforms}
                        )


games_df2 = games_df.drop_duplicates(subset=["title"])#keep it if you dont need versions of the same game for all platform
games_df2.to_csv("games_df.csv", sep='\t', encoding='utf-8', index=False)# writing Df into CSV
