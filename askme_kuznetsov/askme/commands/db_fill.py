from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

import askme_kuznetsov.askme.views
from askme_kuznetsov.askme.models import Question, Answer, Tag, Rating, Profile, RatingAnswers
from random import randint, getrandbits
from datetime import datetime
import requests
settings.configure()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='?', default=1, type=int)

    def handle(self, *args, **options):
        ratio = options.get('ratio', 1)
        num_users = ratio
        #num_questions = 10 * ratio
        num_questions = ratio
        #num_answers = 100 * ratio
        num_answers = ratio
        num_tags = ratio
        #num_ratings = 200 * ratio
        num_ratings = ratio

        # create users
        for i in range(num_users):
            username = f'user{i}'
            password = 'passwd'
            email = f'user{i}@examplemail.ru'
            User.objects.create_user(username, email, password)
            #avatar = f'/static/Uploads/avatar/{randint(1,4)}.png'
            register_date = datetime.today().strftime('%Y-%m-%d');
           # Profile.objects.create(user = User.objects.get(username=username),avatar = avatar, nickname = nickname)
            Profile.objects.create(user=User.objects.get(username=username), register_date=register_date)

        # create tags
        for i in range(num_tags):
            name = f'tag{i}'
            Tag.objects.create(name=name)

        # create questions
        for i in range(num_questions):
            title = f'Title {i}'
            author_id = randint(0, num_users-1)
            text = f'question {i}'
            author = User.objects.get(username=f'user{author_id}')
            question = Question.objects.create(author=author, text=text, title=title)

            # add tags to question
            for j in range(randint(1, 5)):
                tag_id = randint(0, num_tags-1)
                tag = Tag.objects.get(name=f'tag{tag_id}')
                question.tags.add(tag)

            question.save()


        # create answers
        for i in range(num_answers):
            author_id = randint(0, num_users-1)
            question_id = randint(0, num_questions-1)
            question = Question.objects.get(id=question_id)
            text = f'Answer {i}'
            user = User.objects.get(username=f'user{author_id}')
            Answer.objects.create(user=user, question=question, text=text)

        # create likes
        for i in range(num_ratings):
            answer_id = randint(0, num_answers-1)
            question_id = randint(0, num_questions-1)
            user = User.objects.get(username=f'user{author_id}')
            value = bool(getrandbits(1))
            Rating.objects.create(user=user, question=Question.objects.get(pk=question_id), value=value)
            RatingAnswers.objects.create(user=user, answer=Answer.objects.get(pk=answer_id), value=value)

        for i in range(num_questions):
            ratingsum = Rating.objects.filter(question=Question.objects.get(id=i)).count()
            question = Question.objects.get(id=i)
            question.ratingsum = ratingsum
            question.save()

        for i in range(num_answers):
            ratingsum = RatingAnswers.objects.filter(answer=Answer.objects.get(id=i)).count()
            answer = Answer.objects.get(id=i)
            answer.ratingsum = ratingsum
            answer.save()

        self.stdout.write(self.style.SUCCESS('dbfill done'))