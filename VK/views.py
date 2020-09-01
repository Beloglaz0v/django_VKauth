import requests
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from social_django.models import UserSocialAuth




def login(request):
    return render(request, 'login.html')


@login_required
def home(request):
    # user = request.user
    # social = request.user.social_auth.get(provider='vk-oauth2')
    #
    # print(user, social.extra_data['access_token'])
    # token = social.extra_data['access_token']
    #
    # url_friends = 'https://api.vk.com/method/friends.get'
    # friends_params = {
    #         'v': '5.52',
    #         'access_token': token,
    #         'count': '5',
    #         'fields': 'city, online, photo_100',
    #         'order': 'random'
    # }
    # friends_json = requests.get(url=url_friends, params=friends_params)
    # friends = json.loads(friends_json)['response']['items']
    #
    # myself_id = social.extra_data['id']
    # url_myself = f'https://api.vk.com/method/users.get?v=5.52&user_ids={myself_id}&fields=photo_200&access_token={token}'
    # myself_json = requests.get(url=url_myself).text
    # myself = json.loads(myself_json)['response'][0]
    # return render(request, 'home.html', {'friends': friends, 'myself': myself})
    # # return render(request, 'home.html')
    social = request.user.social_auth.get(provider='vk-oauth2')
    log_user = requests.get(
        'https://api.vk.com/method/users.get',
        params={'access_token': social.extra_data['access_token'], 'v': '5.103', 'fields': ['photo_100']}
    )
    friends = requests.get(
        'https://api.vk.com/method/friends.get',
        params={'access_token': social.extra_data['access_token'], 'fields': ['photo_100'], 'v': '5.103', 'order': 'random'}
    )
    friends = friends.json()
    log_user = log_user.json()
    friends = friends['response']['items'][:5]
    log_user = log_user['response']
    logged_user = log_user[0]

    context = {'user': logged_user, 'friend_list': friends}
    return render(request, 'home.html', context)
