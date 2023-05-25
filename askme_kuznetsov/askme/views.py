from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from . import models
from django.contrib import auth
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from askme.forms import LoginForm, RegistrationForm, SettingsForm, AskForm
from django.http import HttpResponse

def index(request):
    question_items = models.Question.manager.new_questions()
    p = Paginator(question_items, 3)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'questions': page}
    return render(request, 'index.html', context)


def question(request, question_id):
    answer_items = models.Answer.manager.get_answer(models.Question.manager.get_question(question_id))
    p = Paginator(answer_items, 3)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'question': models.Question.manager.get_question(question_id),
               'answers': page}
    return render(request, 'question.html', context)


@login_required()
def ask(request):
    if request.method == 'GET':
        ask_form = AskForm()
    else:
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            ask_question = models.Question(title=ask_form.cleaned_data['title'], text=ask_form.cleaned_data['text'], author_id=request.user.id)
            ask_question.save()
            for i in ask_form.cleaned_data['tags'].split(', '):
                tag = models.Tag.objects.filter(name=i)
                if not tag:
                    tag = models.Tag(name=i)
                    tag.save()
                else:
                    tag = tag[0]
                ask_question.tags.add(tag.id)
            ask_question.save()
            return redirect('question', question_id = ask_question.id)
    return render(request, 'ask.html', {'form': AskForm})


def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()

    elif request.method == 'POST':
        login_form = LoginForm(request.POST)

    if login_form.is_valid():
        user = auth.authenticate(request=request, **login_form.cleaned_data)
        if user:
            login(request, user)
            return redirect(reverse('index'))
        login_form.add_error(None, "Invalid username or password")
    return render(request, 'login.html', context={'form': login_form})


def register(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            if User.objects.filter(username=user_form.cleaned_data['username']):
                user_form.add_error(field=None, error="Username taken")
            else:
                user = User.objects.create_user(user_form.cleaned_data['username'], user_form.cleaned_data['email'], user_form.cleaned_data['password1'])
                profile = models.Profile(user=user)
                profile.save()
                user = auth.authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password1'])
                auth.login(request, user)
                return redirect(reverse('index'))
    return render(request, 'register.html', context={'form': user_form})


#@login_required(login_url='login/, redirect_field_name='continue')
@login_required()
def settings(request):
    if request.method == 'GET':
        settings_form = SettingsForm()
    else:
        settings_form = SettingsForm(request.POST)
    if settings_form.is_valid():
        user = request.user
        user.username = settings_form.cleaned_data['username']
        user.email = settings_form.cleaned_data['email']
        user.save()

    return render(request,'settings.html', context={'form': settings_form})


def tag(request):
    question_items = models.Question.manager.get_tag('black_jack')
    p = Paginator(question_items, 3)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'questions': page}
    return render(request, 'tag.html', context)


def hot(request):
    question_items = models.Question.manager.hot_questions()
    p = Paginator(question_items, 3)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'questions': page}
    return render(request, 'hot.html', context)


def pagination(request, index, count):
    paginator = Paginator(index, count)
    page = request.Get.get('page')
    content = paginator.get_page(page)
    return content


@login_required()
def log_out(request):
    logout(request)
    return redirect('index')