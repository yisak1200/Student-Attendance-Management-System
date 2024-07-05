from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=225)
    description = models.TextField()
    department_register_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_visible = models.BooleanField(default=True)
    def __str__(self):
        return self.department_name
class Batch(models.Model):
    year = models.IntegerField()
    is_visible = models.BooleanField(default=True)
    def str(self) -> str:
        return str(self.year)
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department, blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    def str(self) -> str:
        return self.user.first_name
class Semester(models.Model):
    semster_number = models.IntegerField(null=True,blank=True)
    batch = models.ForeignKey(Batch,on_delete=models.PROTECT,null=True,blank=True)
    starting_date = models.DateField(null=True,blank=True)
    is_visible = models.BooleanField(default=True)
    end_date = models.DateField(null=True,blank=True)    
class Course(models.Model):
    name = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester,on_delete=models.PROTECT,null=True,blank=True)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    def str(self) -> str:
        return "{0} ({1})".format(self.name, self.code)
class PeriodTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
class Room(models.Model):
    room_no = models.CharField(max_length=50)
    Building  = models.CharField(max_length=50,null=True,blank=True)
    def str(self) -> str:
        return self.room_no
class Period(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_exam = models.BooleanField(default=False)
    time = models.ForeignKey(PeriodTime, on_delete=models.CASCADE)
    day = models.IntegerField(blank=True, null=True)
    campus = models.CharField(max_length=100)
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.CASCADE)
    def str(self) -> str:
        return self.room.room_no
    def isCurrentClass(self):
        print('dd ', self.day, datetime.date.today().isoweekday())
        check_time = timezone.localtime(timezone.now()).time()
        st = self.time.start_time
        et = self.time.end_time
        if not self.day == datetime.date.today().isoweekday(): return False
        if st < et:
            return check_time >= st and check_time <= et
        else: # crosses midnight
            return check_time >= st or check_time <= et
    def isUpComingClass(self):
        time = timezone.localtime(timezone.now())
        return (not self.isCurrentClass()) and (self.day ==  datetime.date.today().isoweekday()) and (self.time.start_time > time.time())
class TimeTable(models.Model):
    periods = models.ManyToManyField(Period)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    version = models.IntegerField(default=1)
    semster = models.ForeignKey(Semester,models.PROTECT,null=True,blank=True)
    def str(self) -> str:
        return "Semester {0} (v{1})".format(self.semester.semster_number, self.version)
class Section(models.Model):
    batch = models.ForeignKey(Batch,on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    devision = models.CharField(choices=(
        ('Regular', 'Regular'),
        ('Extension', 'Extension')
    ), max_length=50,null=True,blank=True)
    time_table = models.OneToOneField(TimeTable, on_delete=models.CASCADE, blank=True, null=True)
    def str(self) -> str:
        return "{0} - {1} - {2}".format(
            self.department.name,
            self.batch,
            self.name
        )