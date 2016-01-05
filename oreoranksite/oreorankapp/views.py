from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Max

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

from .models import CookieScore, Cookie

WEIGHT_CONSTANT = 10.0


def index(request):
    # HILARIOUSLY INEFFICIENT
    weighting_dict = dict()
    user_list = User.objects.all()
    for user in user_list:
        if len(CookieScore.objects.filter(user_id=user.id)) > 0:
            weighting_dict[user.id] = WEIGHT_CONSTANT / CookieScore.objects.filter(user_id=user.id).aggregate(Max('score'))['score__max']
    cookie_score_list = []
    cookie_list = Cookie.objects.all()
    for cookie in cookie_list:
        class WeightedCookieScore():
            name = ""
            score = 0

            def __init__(self):
                pass
        weighted_cookie_score = WeightedCookieScore()
        weighted_cookie_score.name = cookie.name

        total_score = 0
        len_score = 0
        i_cookie_score_list = CookieScore.objects.filter(cookie_id=cookie.id)
        for cookie_score in i_cookie_score_list:
            len_score += 1
            total_score += cookie_score.score * weighting_dict[cookie_score.user.id]
        weighted_cookie_score.score = total_score / len_score

        cookie_score_list.append(weighted_cookie_score)
    cookie_score_list.sort(key=lambda x: x.score, reverse=True)
    context = {'cookie_score_list': cookie_score_list}
    return render(request, 'oreorankapp/index.html', context)

@login_required()
def score(request):
    if request.method == 'POST':
        if 'cookie_score_id' in request.POST:
            cookie_score = CookieScore.objects.get(pk=request.POST['cookie_score_id'])
            if request.POST['submit'] == 'Update':
                cookie_score.score = request.POST['score']
                cookie_score.save()
            elif request.POST['submit'] == 'Delete':
                cookie_score.delete()
        else:
            user = User.objects.get(pk=request.user.id)
            cookie = Cookie.objects.get(pk=request.POST['cookie_id'])
            cookie_score = CookieScore(user=user, cookie=cookie, score=request.POST['score'])
            cookie_score.save()
    cookie_score_list = CookieScore.objects.filter(user_id=request.user.id).order_by('-score')
    unscored_cookie_list = Cookie.objects.exclude(cookiescore__user__id=request.user.id)
    context = {'cookie_score_list': cookie_score_list,
               'unscored_cookie_list': unscored_cookie_list}
    return render(request, 'oreorankapp/score.html', context)

def logout_view(request):
    logout(request)

    return HttpResponse("You're all logged out now.")