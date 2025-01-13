from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'Newsletter', views.NewsletterViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("post-by-category/<int:category_id>/", views.PostListBycategoryViewSet.as_view(), name="post-list-by-category-api"),
    path("post-by-tag/<int:tag_id>/", views.PostListBytagViewSet.as_view(), name="post-list-by-tag-api"),
    path("draft-list/", views.DraftListViewSet.as_view(), name="draft-list"),
    path("post-publish/", views.PostPublishViewSet.as_view(), name="Post-Publish-api"),
    path("post/<int:post_id>/comments/", views.CommentViewSet.as_view(), name="comment-api"),
]