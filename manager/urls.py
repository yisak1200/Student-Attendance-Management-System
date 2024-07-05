from django.urls import path
from .views import (ManagerIndexView,AddDepartmentView,
                    ListOfDepartmentView,BatchView,AddInstructorView,
                    ListOfInstructors,AddCourseView,BatchYearUpdate,
                    RemoveBatchView,RemovePost,UpdateDepartmentView,
                    RemoveDepartmentConfirmationView,RemoveDepartmentView,
                    PeriodTimeView,AddStudentView,
                    RoomView,UpdateRoomView,AddSemesterView,
                    ListOfSemsterView,AddStudentView,ListOfStudentView,
                    UpdateSemsterView
                    )
urlpatterns = [
    path('manager-index/',ManagerIndexView.as_view(),name = 'manager_index'),
    path('add-department/',AddDepartmentView.as_view(),name = 'add_department'),
    path('list-of-department/',ListOfDepartmentView.as_view(),name = 'list_of_department'),
    path('batch/',BatchView.as_view(),name = 'batch'),
    path('add-instructor/',AddInstructorView.as_view(),name = 'add_instructor'),
    path('instructor-list/',ListOfInstructors.as_view(),name = 'instructor_list'),
    path('add-course/',AddCourseView.as_view(),name='add_course'),
    path('update-batch/<str:pk>/',BatchYearUpdate.as_view(),name='update_batch'),
    path('remove-batch/<str:pk>/',RemoveBatchView.as_view(),name ='remove_batch'),
    path('remove-batch-post/',RemovePost.as_view(),name='remove_post'),
    path('update-department/<str:pk>/',UpdateDepartmentView.as_view(),name = 'update_departemnt'),
    path('remove-confirmation-department/<str:pk>/',RemoveDepartmentConfirmationView.as_view(),name = 'remove_confirmation_department'),
    path('remove-department/',RemoveDepartmentView.as_view(),name = 'remove_department'),
    path('period-time/',PeriodTimeView.as_view(),name ='period_time'),
    path('add-student/',AddStudentView.as_view(),name = 'add_student'),
    path('room/',RoomView.as_view(),name='room'),
    path('update-room/<str:pk>',UpdateRoomView.as_view(),name = 'update_room'),
    path('add-semster/',AddSemesterView.as_view(),name = 'add_semster'),
    path('list-of-semster/',ListOfSemsterView.as_view(),name = 'list_of_semster'),
    path('list-of-student/',ListOfStudentView.as_view(),name = 'list_of_student'),
    path('update-semster/<str:pk>/',UpdateSemsterView.as_view(),name = 'update_semster')
]