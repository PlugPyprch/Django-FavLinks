from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

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

    serializer = FavoriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_favorite_urls(request):
    favorite_urls = FavoriteURL.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorite_urls, many=True)
    return Response(serializer.data)

################################################


# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_res(request):
    return Response({'Hi', 'Hello'})
