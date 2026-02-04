from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:product_id>/add/', views.add_review, name='add_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('<int:review_id>/helpful/', views.vote_helpful, name='vote_helpful'),
    path('<int:review_id>/unhelpful/', views.vote_unhelpful, name='vote_unhelpful'),
]
