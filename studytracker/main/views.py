from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import StudentRegistrationForm, StudentLoginForm, AssignmentCreateForm, AssignmentEditForm, SubmissionEditForm
from django.contrib.auth.decorators import login_required
from .models import Course, Assignment, Submission
from django.db.models import Avg, Max, Min, Count

def index(request):
    courses = Course.objects.all()
    return render(request, 'main/index.html', {'courses': courses})


def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])
            student.save()
            login(request, student)
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            student = form.get_user()
            login(request, student)
            return redirect('tracker')
    else:
        form = StudentLoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def tracker_view(request):
    student = request.user

    active_assignments = Submission.objects.filter(student=student, submitted_at__isnull=True)
    completed_assignments = Submission.objects.filter(student=student, submitted_at__isnull=False)

    return render(request, 'tracker/tracker.html', {
        'student': student,
        'active_assignments': active_assignments,
        'completed_assignments': completed_assignments,
    })


@login_required
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save()
            Submission.objects.create(student=request.user, assignment=assignment)
            return redirect('tracker')
    else:
        form = AssignmentCreateForm()
    return render(request, 'tracker/create_assignment.html', {'form': form})

@login_required
def edit_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, student=request.user)
    assignment = submission.assignment

    if request.method == 'POST':
        assignment_form = AssignmentEditForm(request.POST, request.FILES, instance=assignment)
        submission_form = SubmissionEditForm(request.POST, instance=submission)
        if assignment_form.is_valid() and submission_form.is_valid():
            assignment_form.save()
            sub = submission_form.save(commit=False)
            if sub.grade and sub.submitted_at:
                sub.submitted_at = sub.submitted_at  # если дата вручную указана
            sub.save()
            return redirect('tracker')
    else:
        assignment_form = AssignmentEditForm(instance=assignment)
        submission_form = SubmissionEditForm(instance=submission)

    return render(request, 'tracker/edit_submission.html', {
        'assignment_form': assignment_form,
        'submission_form': submission_form
    })


@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
    return redirect('tracker')


@login_required
def statistics_view(request):
    student = request.user

    # Завершённые задания (есть оценка)
    completed_submissions = Submission.objects.filter(student=student, grade__isnull=False)

    total_completed = completed_submissions.count()
    max_grade = completed_submissions.aggregate(Max('grade'))['grade__max']
    min_grade = completed_submissions.aggregate(Min('grade'))['grade__min']

    # Средняя оценка по каждому курсу
    course_stats = completed_submissions.values(
        'assignment__course__title'
    ).annotate(
        avg_grade=Avg('grade'),
        count=Count('id')
    )

    return render(request, 'tracker/statistics.html', {
        'total_completed': total_completed,
        'max_grade': max_grade,
        'min_grade': min_grade,
        'course_stats': course_stats,
    })