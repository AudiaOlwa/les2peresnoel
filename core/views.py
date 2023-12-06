from django.shortcuts import render
from .models import Product
from .forms import SignUpForm
import random

# Create your views here.
def signup(request):
   form = SignUpForm()
   return render(request, 'signup.html', {'form': form})

def index(request):
 product_book_all = Product.objects.filter(type='L')
 random_books = random.sample(list(product_book_all), 3)

 product_video_all = Product.objects.filter(type='V')
 random_video = random.sample(list(product_video_all), 1)

 product_musik_all = Product.objects.filter(type='M')
 random_musik = random.sample(list(product_musik_all), 1)

 return render(request, 'index.html', {'random_books': random_books, 'random_video': random_video, 'random_musik': random_musik})




def about(request):
	return render(request, 'about.html')

def boutique(request):
	product_book_all = Product.objects.filter(type='L')
	random_books = random.sample(list(product_book_all), 3)
	product_video_all = Product.objects.filter(type='V')
	random_video = random.sample(list(product_video_all), 3)
	product_musik_all = Product.objects.filter(type='M')
	random_musik = random.sample(list(product_musik_all), 3)
	return render(request, 'boutique.html', {'random_books': random_books, 'random_video': random_video, 'random_musik': random_musik})


def livre(request):
	product_book_all = Product.objects.filter(type='L')
	random_books = random.sample(list(product_book_all), len(product_book_all))
	return render(request, 'livre.html',{'random_books': random_books})
def musique(request):
	product_musik_all = Product.objects.filter(type='M')
	random_musik = random.sample(list(product_musik_all), len(product_musik_all))
	return render(request, 'musique.html',{'random_musik': random_musik})
def video(request):
	product_video_all = Product.objects.filter(type='V')
	random_video = random.sample(list(product_video_all), len(product_video_all))
	return render(request, 'video.html',{'random_video': random_video})


