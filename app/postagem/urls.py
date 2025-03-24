'''
URLs for postagem
'''

from django.urls import(path,include)

from rest_framework.routers import DefaultRouter

from postagem import views

router = DefaultRouter()
router.register('postagem', views.PostagemViewSets)

app_name = 'postagem'

urlpatterns = [
    path('', include(router.urls))
]