from django.db import models

# Create your models here.

class Bubble(models.Model):
    title = models.CharField(max_length = 200)
    source = models.CharField(max_length = 200)
    source_url = models.CharField(max_length = 100, blank=True)
    commit_stamp = models.DateTimeField()
    likes = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default = 0)
    content = models.TextField()
    abstract = models.CharField(max_length = 200)

    publisher = models.ForeignKey('Account',on_delete=models.SET_NULL,blank=True,null=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return "<Bubble>{" + self.title + "}"


class Account(models.Model):
    account_num = models.CharField(max_length = 30)
    password_plain = models.CharField(max_length = 30)
    alias = models.CharField(max_length = 30)
    avatar = models.TextField()
    student_validation = models.BooleanField(default=False)
    student_id = models.CharField(max_length = 20,blank=True)
    validated_name = models.CharField(max_length = 20,blank=True)

    def __str__(self):
        return "<Account>{" + self.account_num + "}"

class Tag(models.Model):
    name = models.CharField(max_length=10)
    access_restriction = models.BooleanField(default=False)
    publish_restriction = models.BooleanField(default=False)

    def __str__(self):
        return "<Tag>{" + self.name + "}"

class Comment(models.Model):
    commit_stamp = models.DateTimeField()
    content = models.TextField()

    master_bubble = models.ForeignKey('Bubble',on_delete=models.CASCADE)
    publisher = models.ForeignKey('Account',on_delete=models.CASCADE)

    def __str__(self):
        return "<Comment>{" + self.content + "}"

