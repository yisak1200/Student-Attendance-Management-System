from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from .models import Department,Batch,Course,Instructor,PeriodTime,Section,Room,Semester
from django.contrib.auth.models import User,Group
from student.models import Student
import re
class ManagerIndexView(View):
    def get(self,request):
        number_of_department = Department.objects.count()
        number_of_instructors = Instructor.objects.count()
        number_of_courses = Course.objects.count()
        context ={'number_of_department':number_of_department,'number_of_instructors':number_of_instructors,'number_of_courses':number_of_courses}
        return render(request,'manager_templates/manager_index.html',context)
class AddDepartmentView(View):
    def get(self,request):
        return render(request,'manager_templates/add_department.html')
    def post(self,request):
        department_name = request.POST.get('department_name')
        description = request.POST.get('description')
        department_name_filter = Department.objects.filter(department_name=department_name).count()
        if not department_name:
            messages.error(request,'Department name can not be null')
            request.session['form_data'] = {'department_name': department_name, 'description': description} 
            return redirect('add_department')
        if not description:
            messages.error(request,'Description name can not be null') 
            return redirect('add_department')
        if department_name_filter >=1:
            messages.error(request,'this department already registered') 
            return redirect('add_department')
        else:
            department = Department(department_name=department_name,description=description)
            department.save()
            messages.success(request,'Department Registerd successfully')
            return redirect('list_of_department')
class ListOfDepartmentView(View):
    def get(self,request):
        list_of_department = Department.objects.filter(is_visible=True)
        context = {'list_of_department':list_of_department}
        return render(request,'manager_templates/list_of_department.html',context)
class BatchView(View):
    def get(self,request):
        batches = Batch.objects.filter(is_visible=True)
        context = {'batches':batches}
        return render(request,'manager_templates/batch.html',context) 
    def post(self,request):
        year = request.POST.get('year')
        year_filter = Batch.objects.filter(year=year)
        if not year:
            messages.error(request,'Year is Required') 
            return redirect('batch')
        if year_filter.exists():
            messages.error(request,'This Year is alrread Registered') 
            return redirect('batch')
        else:
            batch = Batch.objects.create(year=year)
            messages.success(request,'Year saved successfully')
            return redirect('batch')
            
            
class AddInstructorView(View):
    def get(self, request):
        departments = Department.objects.all().order_by('department_name')
        context = {'departments': departments}
        return render(request, 'manager_templates/add_instructor.html', context)

    def post(self, request):
        form_data = {
            'username': request.POST.get('username', ''),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'email': request.POST.get('email', ''),
            'phone_number': request.POST.get('phone_number', ''),
            'password': request.POST.get('password'),
            'confirm_password': request.POST.get('confirm_password'),
            'department': request.POST.getlist('department', []),
        }

        name_regex = r"^[A-Za-z\-'/\\]+$"
        username_regex = r"^\w+$"
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        print("=============================",len(form_data['phone_number']))
        # if len(form_data['phone_number'] >10):
        #     messages.error(request,'Phone number length should be 10 numbers')
        #     return redirect('add_instructor')
        if not form_data['department']:
            messages.error(request, 'Department is Required')
            return redirect('add_instructor')
        if not re.match(name_regex, form_data['first_name']):
            messages.error(request, "Please enter a valid first name using only letters.")
        if not re.match(name_regex, form_data['last_name']):
            messages.error(request, "Please enter a valid last name with only letters.")
        if not re.match(email_regex, form_data['email']):
            messages.error(request, "Invalid email format. Please enter a valid email address.")
        if User.objects.filter(email=form_data['email']).exists():
            messages.error(request, "This email is already associated with an existing account.")
        if form_data['password'] != form_data['confirm_password']:
            messages.error(request, "Password and Confirm Password should be the same.")
        if len(form_data['password']) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        if not re.match(username_regex, form_data['username']):
            messages.error(request, "Please enter a valid username.")
        if User.objects.filter(username=form_data['username']).exists():
            messages.error(request, "Username is already taken.")
        if any(messages.get_messages(request)):
            departments = Department.objects.all()
            context = {'departments': departments, 'form_data': form_data}
            return render(request, 'manager_templates/add_instructor.html', context)
        else:
            user = User.objects.create(username=form_data['username'], first_name=form_data['first_name'], last_name=form_data['last_name'], email=form_data['email'])
            user.set_password(form_data['password'])
            group = Group.objects.get(name='Instructor')
            user.groups.add(group)
            user.save() 
            instructor = Instructor.objects.create(user=user, phone_no=form_data['phone_number'])
            instructor.department.set(form_data['department'])  # Use set() for many-to-many field
            messages.success(request, "Instructor Saved Successfully")
            return redirect('add_instructor')
            
class ListOfInstructors(View):
    def get(self,request):
        instructors = Instructor.objects.all()
        context = {'instructors':instructors}   
        return render(request,'manager_templates/list_of_instructors.html',context)    
class AddCourseView(View):
    def get(self, request):
        instructors = Instructor.objects.all()  
        courses = Course.objects.all()
        semsters = Semester.objects.filter(is_visible=True)
        context = {'instructors': instructors, 'courses': courses,'semsters':semsters}
        return render(request, 'manager_templates/course.html', context)

    def post(self, request):
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')
        instructor_id = request.POST.get('Instructor')
        semster_id = request.POST.get('semster')
        if not course_code:
            messages.error(request, 'Course code is required')
            return redirect('add_course')
        if not course_name:
            messages.error(request, 'Course name is required')
            return redirect('add_course')
        if not instructor_id:
            messages.error(request, 'Instructor is required')
            return redirect('add_course')
        if not semster_id:
            messages.error(request,"Semster is Required")
            return redirect('add_course')
        try:
            instructor_get = Instructor.objects.get(pk=instructor_id)  # Fetch instructor by primary key
            semster_get = Semester.objects.get(id = semster_id)
        except Instructor.DoesNotExist:
            messages.error(request, 'Instructor does not exist')
            return redirect('add_course')
        if Course.objects.filter(code=course_code).exists():
            messages.error(request, 'This course code is already taken by another course')
            return redirect('add_course')

        course = Course.objects.create(name=course_name, code=course_code, instructor=instructor_get,semester=semster_get)
        messages.success(request, 'Course added successfully')
        return redirect('add_course')
class BatchYearUpdate(View):
    def get(self,request,pk):
        select_batch = Batch.objects.get(id = pk)
        context = {'select_batch':select_batch}
        return render(request,'manager_templates/update_batch.html',context)
    def post(self,request,pk):
        year = request.POST.get('year')
        select_batch = Batch.objects.get(id=pk)
        if not year:
            messages.error(request,'Year is required')
            return redirect('update_batch')
        select_batch.year = year    
        select_batch.save()
        messages.success(request,'Batch updated successfully')
        return redirect('batch')    
class RemoveBatchView(View):
    def get(self,request,pk):
       select_batch = Batch.objects.get(id=pk) 
       context = {'select_batch':select_batch}
       return render(request,'manager_templates/remove_batch.html',context)
class RemovePost(View):
    def post(self,request):
        batch_id = request.POST.get('batch_id')
        select_batch = Batch.objects.get(id = batch_id) 
        select_batch.is_visible = False
        select_batch.save()
        messages.success(request,'Batch Removed successfully')
        return redirect('batch')        
class UpdateDepartmentView(View):
    def get(self,request,pk):
        select_department = Department.objects.get(id=pk)
        context = {'select_department':select_department}
        return render(request,'manager_templates/update_department.html',context)
    def post(self,request,pk):
        department_name = request.POST.get('department_name')
        description = request.POST.get('description')    
        select_department = Department.objects.get(id=pk)
        if not department_name:
            messages.error(request,'Department name is required')
            return redirect('update_department')
        if not description:
            messages.error(request,'Description is required')
            return redirect('update_department')
        select_department.department_name = department_name
        select_department.description = description
        select_department.save()
        messages.success(request,"Departemnt Updated Successfully")
        return redirect('list_of_department')
class RemoveDepartmentConfirmationView(View):
    def get(seld,request,pk):
        select_department = Department.objects.get(id=pk)
        context = {'select_department':select_department}
        return render(request,'manager_templates/remove_department.html',context)
class RemoveDepartmentView(View):
    def post(self,request):
        department_id = request.POST.get('department_id')
        departmnet = Department.objects.get(id = department_id)  
        departmnet.is_visible = False
        departmnet.save()
        messages.success(request,'Departmemnt removed successfully')
        return redirect('list_of_department')
class PeriodTimeView(View):
    def get(self,request):
        period_time = PeriodTime.objects.all()
        context = {'period_time':period_time}
        return render(request,'manager_templates/period_time.html',context)    
    def post(self,request):
        form_data = {
            'starting_time':request.POST.get('starting_time'),
            'end_time':request.POST.get('end_time')
        }
        
        if not form_data['starting_time']:
            messages.error(request,"Starting Time is Required")
            return redirect('period_time')
        if not form_data['end_time']:
            messages.error(request,"End Time is Required")
            return redirect('period_time')
        if any(messages.get_messages(request)):
            context = {'form_data': form_data}
            return render(request, 'manager_templates/period_time.html', context)
        period_time = PeriodTime.objects.create(start_time=form_data['starting_time'],end_time=form_data['end_time'])
        messages.success(request,'Period Time Saved successfully')
        return redirect('period_time')
        
# class AddStudentView(View):
#     def get(self,request):
#         sections = Section.objects.all()
#         context = {'sections':sections}
#         return render(request,'manager_templates/add_student.html',context)                
class RoomView(View):
    def get(self,request):
        rooms = Room.objects.all()
        context = {'rooms':rooms}
        return render(request,'manager_templates/room.html',context)   
    def post(self,request):
        room_num = request.POST.get('room_num')
        building = request.POST.get('Building') 
        room_filter = Room.objects.filter(room_no=room_num,Building=building)
        if room_filter.exists():
            messages.error(request,'This Room is Saved before')   
            return redirect('room')   
        if not room_num:
            messages.error(request,'Room Number is Required')   
            return redirect('room')     
        if not building:
            messages.error(request,'Building is Required')
            return redirect('room')
        room = Room.objects.create(room_no=room_num,Building=building)
        messages.success(request,'Room Saved Successfully')
        return redirect('room')
class UpdateRoomView(View):
    def get(self,request,pk):
        room = Room.objects.get(id = pk)
        context = {'room':room}
        return render(request,'manager_templates/update_room.html',context)  
    def post (self,request,pk):
        room_num = request.POST.get('room_num')
        building = request.POST.get('Building') 
        room = Room.objects.get(id = pk)
        room_filter = Room.objects.filter(room_no=room_num,Building=building)
        if room_filter.exists():
            messages.error(request,'This Room is Saved before')   
            return redirect('room')   
        if not room_num:
            messages.error(request,'Room Number is Required')   
            return redirect('room')     
        if not building:
            messages.error(request,'Building is Required')
            return redirect('room')
        room.Building = building
        room.room_no = room_num
        room.save()
        messages.success(request,'Room Updated Successfully')
        return redirect('room')
class AddSemesterView(View):
    def get(self, request):
        batches = Batch.objects.filter(is_visible=True)
        context = {'batches': batches}
        return render(request, 'manager_templates/add_semester.html', context)
    def post(self, request):
        semster_number = request.POST.get('semster_number')
        batch_id = request.POST.get('batch')
        starting_date = request.POST.get('starting_date')
        end_date = request.POST.get('end_date')
        semster_number_filter = Semester.objects.filter(semster_number=semster_number)
        batch_filter = Semester.objects.filter(batch=batch_id)
        if semster_number_filter.exists() and batch_filter.exists():
            messages.error(request, 'This Semster With is batch is already Saved')
            return redirect('add_semster')
        if not semster_number:
            messages.error(request, 'Semster Number is Required')
            return redirect('add_semster')
        if not batch_id:
            messages.error(request, 'Batch is Required')
            return redirect('add_semster')
        if not starting_date:
            messages.error(request, 'Starting Date is Required')
            return redirect('add_semester')
        if not end_date:
            messages.error(request, 'End Date is Required')
            return redirect('add_semster')

        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            messages.error(request, 'Invalid Batch selected')
            return redirect('add_semester')

        # Creating the Semester object
        try:
            semester = Semester.objects.create(
                semster_number=semster_number,
                batch=batch,
                starting_date=starting_date,
                end_date=end_date
            )
            messages.success(request, 'Semster Added Successfully')
        except Exception as e:
            messages.error(request, f'Error saving semester: {e}')
            return redirect('list_of_semster')

        return redirect('add_semster')
class ListOfSemsterView(View):
    def get(self,request):
        semsters = Semester.objects.filter(is_visible=True)
        context = {'semsters':semsters}
        return render(request,'manager_templates/list_of_Semstre.html',context)    
class AddStudentView(View):
    def get(self, request):
        sections = Section.objects.all().order_by('name')
        batches = Batch.objects.all()
        context = {'sections': sections, 'batches': batches}
        return render(request, 'manager_templates/add_student.html', context)
    def post(self, request):
        form_data = {
            'username': request.POST.get('username', '').strip(),
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'phone_number': request.POST.get('phone_number', '').strip(),
            'password': request.POST.get('password', ''),
            'confirm_password': request.POST.get('confirm_password', ''),
            'devision': request.POST.get('devision', ''),
            'batch': request.POST.get('batch', ''),
            'section': request.POST.get('section', ''),
            'programme': request.POST.get('programme', '')
        }

        name_regex = r"^[A-Za-z\-'/\\]+$"
        username_regex = r"^\w+$"
        email_regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        
        # Validation checks
        if not re.match(name_regex, form_data['first_name']):
            messages.error(request, "Please enter a valid first name using only letters.")
        if not re.match(name_regex, form_data['last_name']):
            messages.error(request, "Please enter a valid last name using only letters.")
        if not re.match(email_regex, form_data['email']):
            messages.error(request, "Invalid email format. Please enter a valid email address.")
        if User.objects.filter(email=form_data['email']).exists():
            messages.error(request, "This email is already associated with an existing account.")
        if form_data['password'] != form_data['confirm_password']:
            messages.error(request, "Password and Confirm Password should be the same.")
        if len(form_data['password']) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        if not re.match(username_regex, form_data['username']):
            messages.error(request, "Please enter a valid username.")
        if User.objects.filter(username=form_data['username']).exists():
            messages.error(request, "Username is already taken.")
        if len(form_data['phone_number']) != 10 or not form_data['phone_number'].isdigit():
            messages.error(request, 'Phone number length should be exactly 10 digits.')

        if any(messages.get_messages(request)):
            sections = Section.objects.all().order_by('name')
            batches = Batch.objects.all()
            context = {'sections': sections, 'batches': batches, 'form_data': form_data}
            return render(request, 'manager_templates/add_student.html', context)
        
        # Saving the user and student
        try:
            section = Section.objects.get(id=form_data['section'])
            batch = Batch.objects.get(id=form_data['batch'])
        except (Section.DoesNotExist, Batch.DoesNotExist):
            messages.error(request, "Invalid section or batch selected.")
            sections = Section.objects.all().order_by('name')
            batches = Batch.objects.all()
            context = {'sections': sections, 'batches': batches, 'form_data': form_data}
            return render(request, 'manager_templates/add_student.html', context)

        user = User.objects.create(
            username=form_data['username'], 
            first_name=form_data['first_name'], 
            last_name=form_data['last_name'], 
            email=form_data['email']
        )
        user.set_password(form_data['password'])
        user.save()

        group = Group.objects.get(name='Student')
        user.groups.add(group)

        student = Student.objects.create(
            user=user,
            phone_no=form_data['phone_number'],
            section=section,
            devision=form_data['devision'],
            programme=form_data['programme'],
            batch=batch
        )

        messages.success(request, "Student Saved Successfully")
        return redirect('add_student')
class ListOfStudentView(View):
    def get(self,request):
        students = Student.objects.all() 
        context = {'students':students}  
        return render(request,'manager_templates/list_of_student.html',context)
class UpdateSemsterView(View):
    def get(self,request,pk):
        semster = Semester.objects.get(id = pk)
        batches = Batch.objects.all()
        context = {'semster':semster,'batches':batches}
        return render(request,'manager_templates/update_semster.html',context)
    def post(self,request,pk):
        semster_number = request.POST.get('semster_number')
        batch_id = request.POST.get('batch')
        starting_date = request.POST.get('starting_date')
        end_date = request.POST.get('end_date')
        if not semster_number:
            messages.error(request,'Semster Number is Required')
            return redirect('update_semster')
        if not batch_id:
            messages.error(request,'Batch is Required')
            return redirect('update_semster')
        if not starting_date:
            messages.error(request,"Starting Date is Required")
            return redirect('update_semster')
        if not end_date:
            messages.error(request,'End Date is Required')
            return redirect('update_semster')
        batch = Batch.objects.get(id = batch_id)
        semster = Semester.objects.get(id = pk)
        semster.semster_number = semster_number
        semster.batch = batch
        semster.starting_date = starting_date
        semster.end_date = end_date
        semster.save()
        messages.success(request,"Semster Updated Successfully")
        return redirect('list_of_semster')