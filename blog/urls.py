from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from blog import views

app_name = 'blog'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('new_post/', views.new_user_post, name='new_post'),
    path('draft_view/', views.view_user_draft, name='view_draft'),
    path('post_list/', views.post_list, name='post_list'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_detail/<int:pk>/edit_post/', views.edit_post, name='edit_post'),
    path('profile/<user>/', views.profile_page, name="profile_page"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)