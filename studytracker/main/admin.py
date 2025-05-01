from django.contrib import admin
from .models import Student, Course, Assignment, Submission

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadlain')
    list_filter = ('course',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'grade', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('student__email', 'assignment__title')
