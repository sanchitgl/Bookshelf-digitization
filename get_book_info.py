from bs4 import BeautifulSoup
import requests
import re
from googlesearch import search
import json
import cloudscraper
from urllib.request import urlopen
from isbntools.app import *

def get_book_info(book_title):
    #print(book_title)
    '''
    Searches the internet for book_title
    and returns a BookInfo object containing
    the scrapped information
    '''
    title = 'NA'
    author = 'NA'
    image_url = 'NA'
    description = 'NA'
    publish_date = 'NA'

    book_title = book_title.lower()
    isbn = isbn_from_words(book_title)
    #print(isbn)
    try:
        json_obj = registry.bibformatters['json'](meta(isbn))
        json_object = json.loads(json_obj)
        #print(json_object)
        if json_object['title']:
            title = json_object['title']
        if json_object['author'][0]['name']:
            author = json_object['author'][0]['name']
        #print(title)
        #print(author)
        #print()
    except:
        print()

    # search_txt = book_title + " amazon book"

    # book_amazon_link = ""
    # for link in search(search_txt,num_results=10):
    #     #print(link)
    #     if "amazon" in link and "dp/" in link:
    #         book_amazon_link = link
    #         break

    #scraper = cloudscraper.create_scraper( browser='chrome')
    # page = scraper.get(book_amazon_link)
    # soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.body)
    
    #print(title_az)

    #print(book_title.replace(" ","+"))
    #processeddate=soup.find('span', attrs={'id':'LargeHeader_dateText'}).text
    #isbn10 = book_amazon_link[book_amazon_link.find("dp/") + 3:]
    #print(isbn10)
    # gr_response = scraper.get("https://www.goodreads.com/book/isbn/" + isbn10)
    # gr_soup = BeautifulSoup(gr_response.content, "html.parser")
    #print(gr_soup.body)
    # ISBN = re.search(r'isbn(.*?)<',str(gr_soup.body)).group(1)
    # print(ISBN)
    #print(gr_soup.body)
    # with open('readme.txt', 'w') as f:
    #     f.write(str(gr_soup.body))
    # try:
    #     title = gr_soup.find("div", attrs={"class": 'BookPageTitleSection__title'}).text
    #     #print(title)
    #     author = gr_soup.find("span", attrs={"class": "ContributorLink__name"}).text
    # except:
    #     title = gr_soup.find("h1", attrs={"class": 'bookTitle gr-h1 gr-h1--serif'}).text
    #     #print(title)
    #     author = gr_soup.find("a", attrs={"class": "authorName"}).text
    try:
        if title != 'NA':
            #print('hi')
            response = urlopen("https://www.googleapis.com/books/v1/volumes?q="+title.replace(" ","+")+"+inauthor:"+author.replace(" ","+")+"&orderBy=relevance",headers={'User-Agent' : "Magic Browser"})
            book_data = json.load(response)
            #print(book_data)
            volume_info = book_data["items"][0]["volumeInfo"]
            #print(volume_info)
        else:
            try:
                if not isbn:
                    raise ValueError('invalid ISBN')
                #print('hey')
                response = urlopen("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn+"&orderBy=relevance&printType=books",headers={'User-Agent' : "Magic Browser"})
                book_data = json.load(response)
                volume_info = book_data["items"][0]["volumeInfo"]
            except:
                # try:
                #     print('duh')
                #     response = urlopen("https://www.googleapis.com/books/v1/volumes?q="+isbn+"&orderBy=relevance&printType=books")
                #     book_data = json.load(response)
                #     volume_info = book_data["items"][0]["volumeInfo"]
                # except:
                #print('hello')
                response = urlopen("https://www.googleapis.com/books/v1/volumes?q="+book_title.replace(" ","+")+"&orderBy=relevance&printType=books",headers={'User-Agent' : "Magic Browser"})
                book_data = json.load(response)
                volume_info = book_data["items"][0]["volumeInfo"]
                #print(volume_info)
        #print(volume_info)
        title = volume_info['title']
        author = volume_info["authors"]
        author = ', '.join(author)
        if volume_info["imageLinks"]['thumbnail']:
            image_url = volume_info["imageLinks"]['thumbnail']
        elif volume_info["imageLinks"]['smallThumbnaill']:
            image_url = volume_info["imageLinks"]['smallThumbnail']
        publish_date = volume_info["publishedDate"]
        description = volume_info["description"]
    except:
        pass


    #print(book_data)
    

    #print(soup)


    # image_url = soup.find("div", {"class": "editionCover"}).img.get("src")
    # title = soup.find("div", {"class": "infoBoxRowItem"}).text
    # author = soup.find("span", {"itemprop": "name"}).text
    # publisher = soup.find_all("div", {"class": "row"})[1].text
    # publisher = format_publisher(publisher)
    # isbn13 = soup.find("span", {"itemprop": "isbn"}).text
    # rating = ".".join(re.findall('\d+', soup.find("span", {"itemprop": "ratingValue"}).text))
    # description = soup.find(id="description").find_all("span")[1].text
    # total_pages = soup.find("span", {"itemprop": "numberOfPages"}).text
    # total_pages = total_pages[0:total_pages.find("pages")]
    # genre = soup.find("a", {"class": "actionLinkLite bookPageGenreLink"}).text + \
    #     ", " + soup.find_all("a", {"class": "actionLinkLite bookPageGenreLink"})[1].text

    return title, author, image_url, publish_date, description
        #image_url,
        #publisher,
        #isbn10,
        #isbn13,
        #rating,
        #description,
        #total_pages,
        #genre
