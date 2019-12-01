from django.contrib import auth
from django.shortcuts import render, redirect
from django.urls import reverse  # 反解析
from .forms import LoginFrom


def login(request):

    if request.method == 'POST':
        login_form = LoginFrom(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('home'))
    else:
        login_form = LoginFrom()

    context = {'login_form': login_form}
    return render(request, "login.html", context)


"""
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return credits(referer)
    else:
        return render(request, 'error.html', {'message', '用户名或密码不正确'})

    """
