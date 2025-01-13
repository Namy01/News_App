from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group, User

from rest_framework import permissions, viewsets, exceptions
from rest_framework.response import Response 
from rest_framework.views import APIView

from api.serializers import CategorySerializer, CommentSerializer, ContactSerializer, GroupSerializer, NewsletterSerializer, PostPublishSerializer, PostSerializer, UserSerializer, TagSerializer
from newspaper.models import Category, Comment, Contact, Newsletter, Post, Tag


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

class PostViewSet(viewsets.ModelViewSet):

    """    
    API endpoint that allows Posts to be viewed or edited.
    """
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostSerializer
    permission_classes = [permissions. IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["list", "retrieve"]:
            queryset = queryset.filter(status="active", published_at__isnull=False)

            from django.db.models import Q

            search_term = self.request.query_params.get("query", None)
            if search_term:
                queryset = queryset.filter(
                    Q(title__icontains= search_term)|Q(content__icontains= search_term)
                )


        return queryset

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1 #Increment the views_count
        instance.save(update_fields=["views_count"]) # Save only the updated field
        serializer = self.get_serializer (instance)
        return Response(serializer.data)
        

from rest_framework.generics import ListAPIView

class PostListBycategoryViewSet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status="active", published_at__isnull=False,
            category = self.kwargs["category_id"],
        )
        return queryset
    
class PostListBytagViewSet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status="active", published_at__isnull=False,
            tag = self.kwargs["tag_id"],
        )
        return queryset

class DraftListViewSet(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions. IsAuthenticated]


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter( published_at__isnull=True)
        return queryset

from django.utils import timezone
from rest_framework import status

class  PostPublishViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostPublishSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid(raise_exception = True):
            data = serializer.data

            post = Post.objects.get(pk=data["id"])
            post.published_at = timezone.now()
            post.save()

            serializer_data = PostSerializer(post).data
            return Response(serializer_data, status=status.HTTP_200_OK)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ["list","retrieve","destroy"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def update(self,request,*args,**kwargs):
        raise exceptions.MethodNotAllowed(request.method)

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ["list", "retrieve","destroy"]:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)
    

class CommentViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request,post_id, *args,**kwargs):
        comments = Comment.objects.filter(post = post_id).order_by("-created_at")
        serialized_data = CommentSerializer(comments, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    def post(self,request,post_id, *args,**kwargs):
        request.data.update({"post":post_id})
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)