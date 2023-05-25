from django.db import models
from django.contrib.auth.models import User

class AnswerManager(models.Manager):
    def get_answer(self, questions):
        return self.filter(question=questions).order_by('-date')



class QuestionManager(models.Manager):

    def new_questions(self):
        return self.order_by('-date')

    def hot_questions(self):
        return self.order_by()

    def get_tag(self, tag_name):
        return self.filter(tags__name__iexact=tag_name).order_by('-date')

    def get_question(self, number):
        return self.filter(pk=number)[0]


class Profile(models.Model):
    #avatar = models.ImageField(null=True, blank=True, upload_to='static/img/', default='static/img/avatar1a.jpg')
    register_date = models.DateField(null=False, blank=True, auto_now_add=True)
    user = models.OneToOneField(User, related_name='userprofile', primary_key=True, null=False,
                                on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=1024)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField('Tag')
    date = models.DateTimeField(blank=True, auto_now_add=True)
    ratingsum = models.IntegerField(default=0)

    manager = QuestionManager()

    def __str__(self):
        return self.title


class Rating(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    value = models.BinaryField(default=1)

    def __str__(self):
        return self.id_user


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Answer(models.Model):
    text = models.TextField(max_length=1024)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, auto_now_add=True)
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE)
    ratingsum = models.IntegerField(default=0)

    manager = AnswerManager()

    def __str__(self):
        return self.text


class RatingAnswers(models.Model):
    id_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    value = models.BinaryField(default=1)

    def __str__(self):
        return self.id_answer
