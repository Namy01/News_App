import requests
from newspaper.models import Category, Post, Tag
from django.db.models import Count
from django.shortcuts import render

def navigation(request):
    tags = Tag.objects.all()[:12]
    categories = Category.objects.all()[:3]
    trending_posts = Post.objects.filter(
            published_at__isnull = False , status = "active"
            ).order_by("-views_count")[:3]
    side_categories = Category.objects.all()[:6]
    
    recent_posts = Post.objects.filter(
            published_at__isnull = False , status = "active"
            ).order_by("-published_at")[:6]
    
    popular_posts = Post.objects.filter(
            published_at__isnull = False , status = "active"
            ).order_by("-published_at","-views_count")[:6]

    url = 'http://api.openweathermap.org/data/2.5/weather?q=kathmandu&units=metric&appid=fb954e1db45d1487d236413fe0369f4c'
    
    response = requests.get(url)
    weather_data = response.json()
    
    return {
        "tags": tags,
        "categories": categories,
        "trending_posts" : trending_posts,
        "side_categories" : side_categories,
        "recent_posts" : recent_posts,
        "popular_posts" : popular_posts,
        'weather_data': weather_data,
    }