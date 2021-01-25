from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^books/$', views.BookListView.as_view(), name='books'),
  url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
  
  url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
  url(r'^authors/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
  path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
  path('borrowed/', views.LoanedBooksByLibrarianListView.as_view(), name='all-borrowed'),
  path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
  path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
  path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
  path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
  path('book/create/', views.BookCreate.as_view(), name='book-create'),
  path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
  path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]