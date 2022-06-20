from django.db import models
from django.conf import settings
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL

class UserLike(models.Model):
    '''Промежуточная модель для юзеров и их лайков.'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserRetweet(models.Model):
    '''Промежуточная модель для юзеров и их ретвитов.'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(MPTTModel):
    
    text = models.CharField(max_length=140, db_index=True, verbose_name='Текст твита')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    likes = models.ManyToManyField(User, blank=True, related_name='liked', through='UserLike')
    retweets = models.ManyToManyField(User, blank=True, related_name='retweeted', through='UserRetweet')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets', verbose_name='Пользователь')
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='Является ответом на твит')

    class Meta:
        verbose_name = 'tweet'
        verbose_name_plural = 'Tweets'
        ordering = ('id',)

    def __str__(self):
        if len(self.text) > 50:
            return self.text[:51] + '...'
        return self.text