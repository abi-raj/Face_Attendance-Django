from django.urls import path

from .mlfunctions import detect_cont, capture_face
from .views import index, add_class, add_student, dirss, filess, csv_data, login_request, logout_request, stu_list

urlpatterns = [
    path('', index, name='home'),
    # path('cap', capture_face, name='capture'),
    path('stlist',stu_list,name='stu-list'),
    path('add', add_class, name='add_class'),
    path('adds', add_student, name='add-student'),
    path('detect', detect_cont, name='detect'),
    path('files/<date_input>', filess, name='files'),
    path('data/<file_name>/<path>', csv_data, name='data'),
    path('dirs', dirss, name='dirss'),
    path('login/', login_request, name='login'),
    path("logout", logout_request, name="logout"),
    # path('logout', django.contrib.auth.views.LogoutView, {'next_page': '/'}, name='logout'),
]
