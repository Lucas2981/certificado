from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # path('signup/',views.signup, name='signup' ),
    path('logout/',login_required(views.logout_), name='logout'),
    path('signin/',views.signin, name='signin'),
]