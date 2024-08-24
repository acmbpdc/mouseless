from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from quiz import views as quiz_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', quiz_views.home, name='home'),
    path('markdownx/', include('markdownx.urls')),
    path('admin/', admin.site.urls),
    # path('register/', quiz_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='quiz/logout.html'), name='logout'),
    path('player/', include('player.urls')),
    path('task/', include('quiz.urls')),

    path('leaderboard/', quiz_views.leaderboard, name='leaderboard'),
    path("accounts/",include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    path('leaderboard/', quiz_views.leaderboard, name='leaderboard')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

