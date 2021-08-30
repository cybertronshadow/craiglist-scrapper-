from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
import requests
from . import models
# add space to the url when you type separate words
from requests.compat import quote_plus
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

BaseUrl = 'https://www.craigslist.org/d/services/search/bbb?query={}'
BaseImageUrl = 'https://images.craigslist.org/{}_600x450.jpg'


def loginpage(request):
    page = 'login'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'craig/loginpage.html', {'page': page})


def logoutuser(request):
    logout(request)
    return redirect('loginpage')


def registeruser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request, username=user.username,
                                password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('home')

    context = {'form': form, 'page': page}
    return render(request, 'craig/loginpage.html', context)


@login_required(login_url=('loginpage'))
def home(request):
    return render(request, 'base.html')


@login_required(login_url=('loginpage'))
def new_search(request):
    search = request.POST.get('search')
    # to feed what we search in the database we use the below command

    models.Search.objects.create(search=search)

    finalUrl = BaseUrl.format(quote_plus(search))
    response = requests.get(finalUrl)
    data = response.text

    soup = BeautifulSoup(data, features="html.parser")
    postlistings = soup.find_all('li', {'class': 'result-row'})

    finalPostings = []

    for post in postlistings:
        postTitles = post.find(class_='result-title').text
        postUrl = post.find('a').get('href')

        if post.find(class_='result-price'):
            postPrice = post.find(class_='result-price').text
        else:
            postPrice = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            postImageID = post.find(
                class_='result-image').get('data-ids').split(',')[0]
            idofimage = postImageID[2:]
            postImageUrl = BaseImageUrl.format(idofimage)
            print(postImageUrl)
        else:
            postImageUrl = 'https://media.wired.com/photos/5ab55b4934b40d53cae8682e/16:9/w_5000,c_limit/craigslist-01.png'

        finalPostings.append((postTitles, postUrl, postPrice, postImageUrl))

    thingstosee = {
        'search': search,
        'finalPostings': finalPostings,
    }
    return render(request, 'craig/new_search.html', thingstosee)
