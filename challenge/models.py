from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class Challenge(models.Model):
    TYPE_IMAGE = 'img'
    TYPE_FILE = 'file'
    TYPE_AUDIO = 'mp3'
    TYPE_VIDEO = 'mp4'
    TYPES = (
        (TYPE_IMAGE, 'Image'),
        (TYPE_FILE, 'File'),
        (TYPE_AUDIO, 'Audio'),
        (TYPE_VIDEO, 'Video'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, blank=True)
    order = models.IntegerField(primary_key=True)
    type = models.CharField(choices=TYPES, max_length=10)
    solution = models.CharField(max_length=1000)
    file = models.FileField()

    def __str__(self):
        return '%s - %s' % (self.order, self.name)

    # solution will be hard encrypted for security reasons
    def set_solution(self, solution):
        self.solution = make_password(solution)

    def check_solution(self, solution):
        return check_password(solution, self.solution)


class ChallengeUser(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)
    challenge = models.ForeignKey('challenge.Challenge', on_delete=models.DO_NOTHING)
    first_try = models.DateTimeField(default=datetime.now)
    last_try = models.DateTimeField(auto_now_add=True)
    attempt_date = models.DateTimeField(default=datetime.now)
    success = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
