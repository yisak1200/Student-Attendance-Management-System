from django.db import models
from django.contrib.auth.models import User
from manager.models import Period, Section,Batch,Department

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    devision = models.CharField(choices=(
        ('Regular', 'Regular'),
        ('Extension', 'Extension')
    ), max_length=50)
    programme = models.CharField(choices=(
        ('Degree', 'Degree'),
        ('Masters', 'Masters')
    ), max_length=50)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    batch = models.ForeignKey(Batch,on_delete=models.PROTECT,null=True,blank=True)
    def str(self) -> str:
        return self.user.username.replace('_', '/') + " " + self.user.first_name

class AbsentNote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    note = models.TextField()

    def str(self) -> str:
        return self.student.user.username