import requests
from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    if "/ru/" in request.path:
        template = 'mainapp/index_ru.html'
    else:
        template = 'mainapp/index_uz.html'
    return render(request, template)


def message(request):
    if request.method == "POST":
        name = ''
        department = ''
        phone = ''

        if 'name' in request.POST.keys():
            name = request.POST['name']

        if 'department' in request.POST.keys():
            department = request.POST['department']

        if 'phone' in request.POST.keys():
            phone = request.POST['phone']

        text = request.POST['message']

        BOT_TOKEN = "5715491299:AAFVSh2z8Qqjmcxn0olha-aXkAO2BzdAt4E"
        # chat_id = "1115944718"
        chat_id = "-841650719"

        message_to_bot = 'Сообщение от портала SAG!'
        message_to_bot += '\n\nИмя: ' + name
        message_to_bot += '\nОтдел: ' + department
        message_to_bot += '\nТелефон: ' + phone
        message_to_bot += '\nЖалоба или предложение: ' + text
        requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message_to_bot}')

        new_message = Message(name=name, department=department, phone=phone, msg_text=text)
        new_message.save()

    if request.POST['lang'] == 'uz':
        return redirect('thank_you_uz')
    else:
        return redirect('thank_you_ru')


def thank_you(request):
    if "/ru/" in request.path:
        template = 'mainapp/thank_you_ru.html'
    else:
        template = 'mainapp/thank_you_uz.html'
    return render(request, template)


def admin(request):
    if request.user.is_authenticated:
        template = 'mainapp/admin.html'
        messages = Message.objects.all().order_by('-pk')

        context = {'messages': messages}
        return render(request, template, context)
    else:
        return redirect('admin_auth')


# Не авторизованный пользователь anonymous
def admin_auth(request):
    if request.method == 'GET':
        template = 'mainapp/admin_auth.html'
        return render(request, template)
    elif request.method == "POST":
        user = authenticate(request, username=request.POST['login'], password=request.POST['password'])
        if user is None:
            return redirect('admin_auth')
        else:
            login(request, user)
            return redirect('admin')
