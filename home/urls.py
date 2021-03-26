from django.urls import path
from . import views
from .views import PostCreateView , PostUpdateView,PostDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('Contact/',views.Contact,name='Contact'),
    path('search/',views.search,name='search'),
    path('logout/',views.logouthandel,name='logouthandel'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password-reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password-reset-done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'),name='password_reset_complete'),
    path('documentations/',views.document,name='documentations'),
    path('license/',views.license,name='license'),
    path('privacy/',views.privacy,name='privacy'),
    path('questions/',PostCreateView.as_view(),name='questions'),
    path('profile/<str:username>',views.profile,name="profile"),
    path('blogComment',views.blogComment,name="blogComment"),
    path('category/<str:cate>',views.category,name="category"),
    path('<str:slug>',views.posts, name='posts'),
    path('<str:slug>/update/',PostUpdateView.as_view(), name='posts-update'),
    path('<str:slug>/delete/',PostDeleteView.as_view(), name='posts-delete'),
    path('<str:slug>/',views.notAvailable,name='notAvailable'),
]
