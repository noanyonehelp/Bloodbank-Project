from django.urls import path
from . import views

urlpatterns=[
    path('', views.bloodbanks, name='bloodbanks'),
    path('profile/<int:id>/', views.bloodbank_profile, name='profilebloodbank'),
    path('add-new-bloodbank', views.addnewbloodbank, name='addnewbloodbank'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='editbloodbank'),
    path('favourite/<int:id>/', views.favourite_bloodbank, name='favourite_bloodbank'),
    path('favourites-list/<str:username>/<int:id>/', views.bloodbank_favourite_list, name='bloodbank_favourite_list'),

    path('likeBloodbank/<int:id>/', views.like_bloodbank, name='like_bloodbank'),
    path('likes-list/<str:username>/<int:id>/', views.bloodbank_like_list, name='bloodbank_like_list'),
    
    path('comment/<int:profileID>/userID/<int:userID>/deleteComment/<int:commentID>', views.deleteCommentBloodbank, name='deleteCommentBloodbank'),

    path('comment/<int:bloodbankID>/userID/<int:userID>/editComment/<int:commentID>', views.editCommentBloodbank, name='editCommentBloodbank')
]