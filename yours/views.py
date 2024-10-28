from urllib import response
from . import models  # because we need to save things in database
from bs4.element import Tag
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
import re
#from requests.compact import quote_plus
from.models import Search

# Create your views here.

# here you also put the name and the the url of the website in which you're scraping
# like this BASE_NAMEOFTHEWEBSITE_URL = the url
# BASE_CRAIGLIST_URL = "https://tampa.craigslist.org/" for craiglist.org in the tampa location
#BASE_IKEA_URL = "https://www.ikea.com/"
#BASE_WEBSITENAME_URL = "https://.org/"
# we put this here because BeautifulSoup doesn't scrap into the images, images <div>
# and images has what is called image id
# and craigslist has many images per post which are swiped over and is possible by <div class="swipe" style="visibility: visible";>
# BASE_IMAGE_URL in order to get the images from the given url
# 300x300 is putted there in order to get the images of the same size
#BASE_IMAGE_URL = 'https://images._300x300.jpg'


def home(request):
    return render(request, template_name="base.html")


def new_search(request):
    search = request.POST.get("search")
    # to create our search in the database
    models.Search.objects.create(search=search)

    #final_url = BASE_WEBSITENAME_URL.format(quote_plus(search))
    # print(search)
    #response = requests.get(final_url)
    data = response.text
    # parsing the html data into this object
    soup = BeautifulSoup(data, features="html.parser")
    # result-row contains the info of the title,the link and the price
    post_listings = soup.find_all('li', {'class': 'result-row'})
    # 'a' is link, it says find all links where the class is 'results-title'
    post_titles = soup.find_all('a', {'class': 'results-title'})
    post_url = post_listings[0].find('a').get("href")
    #post_price = post_listings[0].find(class="result-price").text
    # the get part is for getting the link it means that after that we get the title and the link
    # if we wanted to have only the first result, we would have written this print(post_titles[0].get('href'))
    # print(data)
    print(post_titles.get('href'))

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []
    # all those codes under final_postings[] are stored into final_postings[]

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        # the images ids mentioned on the 16th line
        if post.find(class_='result-image').get('data-ids'):
            # the [0] is because we want to get one image id
            # , is putted there after split because the list of ids is separated by ,
            # because we're gonna split that string in a list separated by ,
            post_image_id = post.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            # the image we give when the searched item has no picture
            # we have to give a default image here where come the else
            post_image_url = 'https:///images/peace.jpg'

        final_postings.append(
            (post_title, post_url, post_price, post_image_url))

    frontend = {
        "search": search,
        "final_postings": final_postings,

    }
    return render(request, "yours/new_search.html", frontend)
