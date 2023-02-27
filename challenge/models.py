import hashlib
import re
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.template import Template, Context


class ChallengeTopic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    TYPE_IMAGE = 'img'
    TYPE_FILE = 'file'
    TYPE_AUDIO = 'mp3'
    TYPE_VIDEO = 'mp4'
    TYPE_HTML = 'html'
    TYPE_NONE = 'none'
    TYPES = (
        (TYPE_IMAGE, 'Image'),
        (TYPE_FILE, 'File'),
        (TYPE_AUDIO, 'Audio'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_HTML, 'HTML Template'),
        (TYPE_NONE, 'None'),
    )
    HASH_DERIVATION = 'Hash'
    LIST_DERIVATION = 'List'
    NO_DERIVATION = None
    KEY_DERIVATIONS = (
        (HASH_DERIVATION, 'Hash derivation: sha256(code + user.id)'),
        (NO_DERIVATION, 'No derivation'),
        (LIST_DERIVATION, 'Coma-separated list code derivation: code[id % len]')
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(help_text='Starts by 0', default=0)
    type = models.CharField(choices=TYPES, max_length=10)
    key_derivation = models.CharField(choices=KEY_DERIVATIONS, null=True, max_length=5)
    solution = models.TextField()
    file = models.FileField()
    activation_date = models.DateTimeField(default=datetime.now)
    topic = models.ForeignKey(ChallengeTopic, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s - %s - %s' % (self.order, self.topic, self.name)

    def active(self):
        return self.activation_date <= pytz.utc.localize(datetime.now())

    def get_template_html(self):
        with self.file.open('r') as file:
            text = file.read()
        template = Template(text)
        context = Context({'self': self})
        return template.render(context=context)

    def set_solution(self, solution):
        if self.key_derivation == self.NO_DERIVATION:
            self.solution = make_password(solution)
        else:
            self.solution = solution

    def check_solution(self, solution, user_id):
        try:
            solution = re.match(getattr(settings, 'CODE_FORMAT'), solution, re.IGNORECASE).group(1)
        except AttributeError:
            return False
        if self.key_derivation == self.NO_DERIVATION:
            return check_password(solution, self.solution)
        elif self.key_derivation == self.HASH_DERIVATION:
            hasher = hashlib.sha256()
            hasher.update(('%s%s' % (self.solution, user_id)).encode('utf-8'))
            return solution == hasher.hexdigest()
        elif self.key_derivation == self.LIST_DERIVATION:
            solution_list = self.solution.replace(' ', '').split(',')
            return solution == solution_list[user_id % len(solution_list)]
        return False

    def check_troll(self, code):
        try:
            return self.challengetroll_set.get(code=code).url
        except ChallengeTroll.DoesNotExist:
            return None


class ChallengeUser(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING)
    challenge = models.ForeignKey('challenge.Challenge', on_delete=models.DO_NOTHING)
    first_try = models.DateTimeField(default=datetime.now)
    last_try = models.DateTimeField(null=True)
    attempt_date = models.DateTimeField(default=datetime.now)
    success = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    vote = models.IntegerField(null=True)
    comment = models.TextField(null=True, blank=True)


class ChallengeTroll(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000)
    url = models.URLField()

    def __str__(self):
        return '%s (%s)' % (self.challenge, self.pk)

    class Meta:
        unique_together = ('challenge', 'code')


class VoteReaction(models.Model):
    TYPE_HAPPY = 'happy'
    TYPE_SAD = 'sad'
    TYPES = [
        (TYPE_HAPPY, 'Happy'),
        (TYPE_SAD, 'Sad'),
    ]

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    image = models.FileField()
    type = models.CharField(max_length=10, choices=TYPES)

    def __str__(self):
        return '%s - %s' % (self.challenge, self.get_type_display())

    class Meta:
        unique_together = ('challenge', 'type')
