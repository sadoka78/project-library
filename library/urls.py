from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-library/', views.my_library, name='my_library'),


    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='library/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='library/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='library/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='library/password_reset_complete.html'), name='password_reset_complete'),



    path('', views.index, name='index'),
    path('my-library/', views.my_library, name='my_library'),
    path('my-library/add-new/', views.add_new_media_to_library, name='add_new_media_to_library'),
    path('add-category/', views.create_category, name='create_category'),
    path('my-library/edit/<int:pk>/', views.edit_library_item, name='edit_library_item'),
    path('my-library/delete/<int:pk>/', views.delete_library_item, name='delete_library_item'),
    path('add-to-library/<int:media_id>/', views.add_existing_media_to_library, name='add_to_library'),
    path('media/<int:media_id>/reviews/', views.media_reviews, name='media_reviews'),




]
