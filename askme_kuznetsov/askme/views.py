from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from . import models
from django.http import HttpResponse

def index(request):
    question_items = models.QUESTIONS
    p = Paginator(question_items, 3)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'questions': page}
    return render(request, 'index.html', context)

def question(request, question_id):
    answer_items = models.ANSWERS
    p = Paginator(answer_items, 3)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'question': models.QUESTIONS[question_id],
               'answers': page}
    return render(request, 'question.html', context)

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def settings(request):
    return render(request,'settings.html')

def tag(request):
    question_items = models.QUESTIONS
    p = Paginator(question_items, 3)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'questions': page}
    return render(request, 'tag.html', context)

def hot(request):
    question_items = models.QUESTIONS
    p = Paginator(question_items, 3)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)
    context = {'questions': page}
    return render(request, 'hot.html', context)