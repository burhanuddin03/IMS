from django.urls import path
from . import views


app_name='accounts'
urlpatterns = [
    path('',views.DashboardView,name='index'),
    path('register/',views.UserRegisterView.as_view(),name='user_register'),
    path('user-profiles/',views.GetUserList.as_view(),name="users_list"),
    path('user-profiles/delete/<int:pk>/',views.DeleteUser.as_view(),name="user_delete"),
    path('user-profiles/update/<int:pk>/',views.UserUpdateView.as_view(),name='user_update'),
    path('user-profiles/password_update/<int:pk>/',views.UserPasswordUpdateView.as_view(),name='user_password_update')

]
