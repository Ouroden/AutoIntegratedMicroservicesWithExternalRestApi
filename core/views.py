from django.shortcuts import render
from django.conf import settings
import requests
from github import Github, GithubException

def home(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '74.91.20.42')
        response = requests.get('http://api.ipstack.com/%s?access_key=eef8ds7ds8dsd7fgs8gsdg9sdd9dgss8' % ip_address)
        request.session['geodata'] = response.json()

    geodata = request.session['geodata']

    return render(request, 'core/home.html', {
        'country': geodata.get('country_name',''),
        'latitude': geodata.get('latitude',''),
        'longitude': geodata.get('longitude',''),
        'ip': geodata.get('ip',''),
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'is_cached': is_cached
    })

def github(request):
    user = {}
    if 'username' in request.GET:
        username = request.GET['username']
        try:
            response = requests.get('https://api.github.com/users/%s' % username)
            response.raise_for_status()
        except requests.HTTPError as http_err:
            r = response.json()
            user = {
                'name': username,
                'public_repos': http_err
            }
            print(f'HTTP error occurred: {http_err}')
        else:
            r = response.json()
            user = {
                'name': r.get('login'),
                'public_repos': r.get('public_repos')
            }
    return render(request, 'core/github.html', {'user': user})