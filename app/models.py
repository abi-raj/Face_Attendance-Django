from django.db import models


class StudentClass(models.Model):
    title = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    regno = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=30)
    stclass = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.regno)
