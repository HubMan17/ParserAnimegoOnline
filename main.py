import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url = r"https://animego.online/"

maxCountTitles = 5744

count = 0

with open("data.json", "w", encoding="utf-8") as file:
    file.write("[\n")

while True:

    if count == maxCountTitles + 1:
        break

    print(f"Anime id: {count}/{maxCountTitles}")


    page = requests.get(url + str(count), headers={"User-Agent": UserAgent().chrome})
    soup = BeautifulSoup(page.text, "html.parser")

    # title name
    try:
        titlePage = soup.find("h1").text
    
    except:
        count += 1
        continue

    if titlePage == "Популярные новинки аниме онлайн на AnimeGO":
        count += 1
        continue

    # main info
    statusAnime = soup.find("div", class_="poster-item__label")

    try:
        seriesCount = statusAnime.find("span").text
        statusAnime = statusAnime.find("span").next_sibling.text
    except:
        seriesCount = ""
        statusAnime = statusAnime.text

    typeAnime = soup.find("div", class_="speedbar__full").findAll('a')[1].text
    imageAnime = soup.find("div", class_="img-fit-cover").find("img").get("src")
    try:
        releaseDate = soup.find("ul", class_="page__details-list").find('a').text
    except:
        releaseDate = "-"

    directorAnimeTitle = soup.find("ul", class_="page__details-list").findAll("li")[3].find('span').text
    directorAnime = soup.find("ul", class_="page__details-list").findAll("li")[3].findAll('span')[1].text

    studioAnimeTitle = soup.find("ul", class_="page__details-list").findAll("li")[4].find('span').text
    studioAnime = soup.find("ul", class_="page__details-list").findAll("li")[4].findAll('span')[1].text


    # second info
    allSecondInfo = soup.find("ul", class_="line-clamp").findAll("li")

    otherNamesTitles = allSecondInfo[0].find("span").text
    otherNames = allSecondInfo[0].findAll("span")[1].text

    if otherNamesTitles == "Другие названия:":
        
        subtitlesTitle = allSecondInfo[1].find("span").text
        subtitles = []
        for subtitle in allSecondInfo[1].findAll("span")[1:]:
            subtitles.append(subtitle.text)

        genresTitle = allSecondInfo[2].find("span").text
        ganres = []
        for genre in allSecondInfo[2].findAll("span")[1:]:
            ganres.append(genre.text)
        
    else:
        otherNamesTitles = ""
        otherNames = ""
        
        subtitlesTitle = allSecondInfo[0].find("span").text
        subtitles = allSecondInfo[0].findAll("span")[1].text

        genresTitle = allSecondInfo[1].find("span").text
        ganres = allSecondInfo[1].findAll("span")[1].text

    # anime description
    descriptions = soup.find("div", class_="page__text")

    descriptionAnime = ""
    for description in descriptions:
        descriptionAnime += description.text + "\n"

    jsonData = {
        "id": count,
        "title": titlePage,
        "seriesCount": seriesCount,
        "status": statusAnime,
        "type": typeAnime,
        "releaseDate": releaseDate,
        "director": directorAnime,
        "studio": studioAnime,
        "otherNames": otherNames,
        "subtitles": subtitles,
        "genres": ganres,
        "description": descriptionAnime,
        "image": imageAnime
    }

    with open("data.json", "a", encoding="utf-8") as file:
        json.dump(jsonData, file, indent=4, ensure_ascii=False)
        
        if count != maxCountTitles:
            file.write(",")
        
    count += 1
    
    
with open("data.json", "a", encoding="utf-8") as file:
    file.write("\n]")