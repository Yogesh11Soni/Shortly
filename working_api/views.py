from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from working_api.form import URLForm, URLCredentialsLForm
from working_api.models import URL, URLWithCredentials
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
import random
from django.contrib.auth.views import login_required
from django.db.models import Q


@csrf_exempt
def index(request, hash_url=None):
    if request.session.get('_auth_user_id') is None:
        if hash_url is not None:
            try:
                data = URL.objects.get(url_hash=hash_url).full_url
            except:
                return redirect('/')
            else:
                return redirect(data)

        if request.method == 'POST':
            if not URL.objects.filter(full_url=request.POST['url']).exists():
                form = URLForm(request.POST)
                if form.is_valid():
                    f = form.save(commit=False)
                    f.full_url = request.POST['url']
                    f.save()
                    url = URL.objects.get(full_url=request.POST['url']).url_hash
                    url = 'http://127.0.0.1:8000/{}'.format(url)
                    return render(request, 'index.html', {'data': url})
            else:
                url = URL.objects.get(full_url=request.POST['url']).url_hash
                url = 'http://127.0.0.1:8000/{}'.format(url)
                return render(request, 'index.html', {'data': url})
        return render(request, 'index.html')
    else:
        if hash_url is not None:
            try:
                data = URLWithCredentials.objects.get(Q(url_hash=hash_url) & Q(u_id_id=request.user.pk)).full_url
            except:
                return redirect('/')
            else:
                return redirect(data)
        return redirect('/admin_index/')


@csrf_exempt
def register(request):
    if request.session.get('_auth_user_id') is None:
        if request.method == 'POST':
            if not User.objects.filter(email=request.POST['email']).exists():
                User.objects.create_user(
                    username=request.POST['f_name']+request.POST['l_name']+str(random.randint(1, 1000)),
                    password=request.POST['password'],
                    email=request.POST['email'],
                    first_name=request.POST['f_name'],
                    last_name=request.POST['l_name'],
                    is_superuser=False,
                    is_staff=False,
                    is_active=True
                )
                return redirect('/')
            else:
                return render(request, 'register.html', {'already': True})
        return render(request, 'register.html')
    else:
        return redirect('/admin_index/')


@csrf_exempt
def my_login(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']).exists():
            if check_password(request.POST['password'], User.objects.get(email=request.POST['email']).password):
                user = authenticate(request, username=User.objects.get(email=request.POST['email']).username, password=request.POST['password'])
                if user is not None:
                    login(request, user)
                    request.session['email'] = user.email
                    return redirect('/admin_index/')
            else:
                return render(request, 'login.html', {'invalid_password': True})
        else:
            return render(request, 'login.html', {'invalid_email': True})
    if request.session.get('_auth_user_id') is not None:
        return redirect('/admin_index/')
    else:
        return render(request, 'login.html')


@login_required
def my_logout(request):
    logout(request)
    return redirect('/')


@login_required
@csrf_exempt
def admin_index(request, hash_url=None):
    if hash_url is not None:
        try:
            data = URLWithCredentials.objects.get(Q(url_hash=hash_url) & Q(u_id_id=request.user.pk)).full_url
        except:
           return redirect('/admin_index/')
        else:
            return redirect(data)

    if request.method == 'POST':
        if not URLWithCredentials.objects.filter(Q(full_url=request.POST['url']) & Q(u_id_id=request.user.pk)).exists():
            form = URLCredentialsLForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.full_url = request.POST['url']
                f.u_id_id = request.user.pk
                f.save()
                url = URLWithCredentials.objects.get(Q(full_url=request.POST['url']) & Q(u_id_id=request.user.pk)).url_hash
                url = 'http://127.0.0.1:8000/{}'.format(url)
                return render(request, 'admin_index.html', {'data': url})
        else:
            url = URLWithCredentials.objects.get(Q(full_url=request.POST['url']) & Q(u_id_id=request.user.pk)).url_hash
            url = 'http://127.0.0.1:8000/{}'.format(url)
            return render(request, 'admin_index.html', {'data': url})
    return render(request, 'admin_index.html')


@login_required
def url_list(request):
    data = URLWithCredentials.objects.filter(u_id_id=request.user.pk)
    return render(request, 'url_list.html', {'data': data, 'link': '127.0.0.1:8000/'})
