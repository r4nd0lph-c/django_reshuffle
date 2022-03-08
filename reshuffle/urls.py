from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('auth/', Auth.as_view(redirect_authenticated_user=True), name='auth'),
    path('logout/', logout_user, name='logout'),
    path('creation/', Creation.as_view(), name='creation'),
    path('download/', Download.as_view(), name='download'),
    path('download_archive/', download_archive, name='download_archive'),
    path('get_subj_info/', get_subj_info, name='get_subj_info')
]
