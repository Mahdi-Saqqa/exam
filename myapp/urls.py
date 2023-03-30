from django.urls import path
from . import views
urlpatterns = [
    path('',views.root),
    path('loginpage',views.loginpage),
    path('signup',views.signup),
    path('signin',views.signin),
    path('success',views.success),
    path('logout',views.logout),
    path('addpainting',views.addpainting),
    path('addpaintsubmit',views.addpaintsubmit),
    path('paint/<int:id>/edit',views.edit),
    path('paint/<int:id>/editsubmit',views.editsubmit),
    path('paint/<int:id>/delete',views.delete),
    path('paint/<int:id>',views.paintdetails),
    path('paint/<int:id>/buy',views.buy),

]