from django import views
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import DocumentCreateView
from .views import DocumentCreateView
from . import views
from .views import login_redirect

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name = 'home'),
    path('logout', LogoutView.as_view()),
    path('upload/', DocumentCreateView.as_view(template_name = "home_page.html"), name = 'upload'),
    path('upload/success/', views.uploadSuccessView, name='upload_success'),
    path('all_documents/', views.admin_document_list, name='admin_document_list'),
    path('my_documents/', views.user_document_list, name='user_document_list'),
    path('documents/<int:form_id>/update_status/', views.update_document_status, name='update_document_status'),
    path('documents/<int:form_id>/view_document/', views.view_document, name='view_document'),
    path('documents/<int:form_id>/comment/', views.comment_form, name='comment_form'),
    path('documents/<int:form_id>/resolve/', views.mark_as_resolved, name='mark_as_resolved'),
    path('documents/<int:form_id>/submit_comment/', views.submit_comment, name='submit_comment'),
    path('report-form/', views.report_form, name='report_form'),
    path('documents/<int:form_id>/delete/', views.delete_document, name='delete_document'),
    path('login-redirect/', login_redirect, name='login_redirect'),
]