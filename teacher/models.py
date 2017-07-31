from django.db import models


class TeacherInfo(models.Model):
    name = models.CharField(max_length=64)
