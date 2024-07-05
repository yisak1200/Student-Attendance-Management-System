from django.contrib import admin
from .models import (
    Department,
    Batch,
    Instructor,
    Course,
    Period,
    PeriodTime,
    TimeTable,
    Section,
    Room,
    Semester
)

admin.site.register(Department)
admin.site.register(Batch)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Period)
admin.site.register(TimeTable)
admin.site.register(Section)
admin.site.register(PeriodTime)
admin.site.register(Room)
admin.site.register(Semester)