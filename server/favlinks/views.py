from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import requests

from .models import Category, Tag, FavoriteURL
from .serializers import CatSerializer, TagSerializer, FavoriteSerializer


################### Category ###################

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_cat(request):
    data = request.data.copy()
    data['user'] = request.user.id
    print(request.user.username) # Test
    print(request.user.email) # Test
    serializer = CatSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_cats(request):
    categories = Category.objects.filter(user=request.user)
    serializer = CatSerializer(categories, many=True)
    return Response(serializer.data)

###############################################

################### Tag ###################

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_tag(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = TagSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_tags(request):
    tags = Tag.objects.filter(user=request.user)
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)

###############################################

################### FavLinks ###################
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_favorite_url(request):
    data = request.data.copy()
    data['user'] = request.user.id
    try:
        response = requests.head(data['url'], timeout=5)
        data['is_valid'] = response.status_code == 200
    except requests.RequestException:
        data['is_valid'] = False
    serializer = FavoriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_favorite_urls(request):
    user = request.user
    favorite_urls = FavoriteURL.objects.filter(user=user)

    category_id = request.query_params.get('category_id')
    tag_ids = request.query_params.getlist('tag_ids')

    if category_id:
        favorite_urls = favorite_urls.filter(category_id=category_id)
    
    if tag_ids:
        favorite_urls = favorite_urls.filter(tags__id__in=tag_ids).distinct()

    for favorite_url in favorite_urls:
        try:
            response = requests.head(favorite_url.url, timeout=5)
            favorite_url.is_valid = response.status_code == 200
        except requests.RequestException:
            favorite_url.is_valid = False
        favorite_url.save()

    serializer = FavoriteSerializer(favorite_urls, many=True)
    return Response(serializer.data)

################################################


# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_res(request):
    return Response({'Hi', 'Hello'})
