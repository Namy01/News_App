from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('published-post/', views.PublishedPostView.as_view(), name='published-post'),
    path('draft-post/', views.DraftPostView.as_view(), name='draft-post'),
    path('admin-post-detail/<int:pk>/', views.PostDetailView.as_view(), name='admin-post-detail'),
    path('hidden-post/', views.HiddenPostView.as_view(), name='hidden-post'),
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('tags/', views.TagView.as_view(), name='tags'),
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("admin-update/<int:pk>/", views.PostUpdateView.as_view(), name="admin-update"),
    path("delete/<int:pk>/", views.PostdeleteView.as_view(), name="delete"),
    path("publish/<int:pk>/", views.PostpublishView.as_view(), name="publish"),
    path("create-tag/", views.TagCreateView.as_view(), name="create-tag"),
    path("delete-tag/<int:pk>", views.TagdeleteView.as_view(), name="delete-tag"),
    path("update-tag/<int:pk>", views.TagUpdateView.as_view(), name="update-tag"),
    path("create-category/", views.CategoryCreateView.as_view(), name="create-category"),
    path("delete-category/<int:pk>", views.CategorydeleteView.as_view(), name="delete-category"),
    path("update-category/<int:pk>", views.CategoryUpdateView.as_view(), name="update-category"),
    path("post-active/<int:pk>", views.PostActiveView.as_view(), name="post-active"),
    path("post-in-active/<int:pk>", views.PostInActiveView.as_view(), name="post-in-active"),
]
