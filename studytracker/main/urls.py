from django.urls import path
from .views import index, register_view, login_view, \
    logout_view, tracker_view, statistics_view, \
    create_assignment, edit_submission, \
    delete_assignment, AssignmentDetailView

urlpatterns = [
    path('', index, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tracker/', tracker_view, name='tracker'),
    path('stat/', statistics_view, name='statistics'),
    path('create/', create_assignment,
         name='create_assignment'),
    path('edit/<int:submission_id>/', edit_submission,
         name='edit_submission'),
    path('delete/<int:assignment_id>/', delete_assignment,
         name='delete_assignment'),
    path('assignment/<int:pk>/', AssignmentDetailView.as_view(),
         name='assignment_detail'),
]
