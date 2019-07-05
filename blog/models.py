from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from updown.fields import RatingField


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = RatingField(can_change_vote=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_likes(self):
    	return self.rating_likes


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'post_comments')
	text = models.TextField()
	rating = RatingField(can_change_vote=True)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.text[:10]

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.post.id})
