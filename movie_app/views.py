from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_app.serializers import (
    DirectorSerializers,
    MovieSerializers,
    ReviewSerializers,
    DirectorValidateSerializer,
    MovieValidateSerializer,
    ReviewValidateSerializer,
)
from movie_app.models import Director, Movie, Review
from rest_framework import status
from django.contrib.auth.models import User
from movie_app.serializers import UserValidateSerializer, UserAuthorizationSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(["GET", "POST"])
def director_list_view(request):
    if request.method == "GET":
        directors = Director.objects.all()
        serializer = DirectorSerializers(directors, many=True)
        return Response(data=serializer.data)
    elif request.method == "POST":
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"errors": serializer.errors},
            )
        director = Director.objects.create(**serializer.director_data_movie)
        return Response(data=DirectorSerializers(director).data)


@api_view(["GET", "PUT", "DELETE"])
def director_detail_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(
            data={"error": "Director not Found!!!"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        serializer = DirectorSerializers(director)
        return Response(data=serializer.data)
    elif request.method == "DELETE":
        director.delete()
        return Response(data={"massage": "Director removed!"})
    else:
        director.name = request.data.get("name")
        director.save()
        return Response(data=DirectorSerializers(director).data)


@api_view(["GET", "POST"])
def movie_list_view(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializers(movies, many=True)
        return Response(data=serializer.data)
    elif request.method == "POST":
        serializers = MovieValidateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"errors": serializers.errors},
            )

        movie = Movie.objects.create(**serializers.movie_data_director)
        return Response(data=MovieSerializers(movie).data)


@api_view(["GET", "PUT", "DELETE"])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(
            data={"error": "Movie not Found!!!"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        serializer = MovieSerializers(movie)
        return Response(data=serializer.data)
    elif request.method == "DELETE":
        movie.delete()
        return Response(data={"massage": "Movie removed!"})
    else:
        movie.title = request.data.get("title")
        movie.description = request.data.get("description")
        movie.duration = request.data.get("duration")
        movie.director_id = request.data.get("director_id")
        movie.save()
        return Response(data=MovieSerializers(movie).data)


@api_view(["GET", "POST"])
def review_list_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        serializer = ReviewSerializers(reviews, many=True)
        return Response(data=serializer.data)
    elif request.method == "POST":
        serializers = ReviewValidateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"errors": serializers.errors},
            )
        # movie = serializers.validate_movie_id(movie_id=id)
        review = Review.objects.create(**serializers.review_data_without)
        # review.movie.set(movie)
        # review.save()
        return Response(data=ReviewSerializers(review).data)


@api_view(["GET", "PUT", "DELETE"])
def review_detail_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(
            data={"error": "Review not Found!!!"}, status=status.HTTP_404_NOT_FOUND
        )
    if request == "GET":
        serializer = ReviewSerializers(review)
        return Response(data=serializer.data)
    elif request == "DELETE":
        review.delete()
        return Response(data={"massage": "Review removed!"})
    else:
        review.text = request.data.get("text")
        review.movie = request.data.get("movie")
        review.stars = request.data.get("stars")
        review.save()
        return Response(data=ReviewSerializers(review).data)


@api_view(["GET"])
def movies_reviews_view(request):
    movie_reviews = Movie.objects.all()
    data = MovieSerializers(movie_reviews, many=True).data
    return Response(data=data)



@api_view(['POST'])
def registration(request):
    serializer = UserValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    User.objects.create_user(**serializer.validated_data)
    return Response(data={'message': 'User created'})


@api_view(['POST'])
def authorization(request):
    serializer = UserAuthorizationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
    return Response(data={'message': 'User not found'},
                    status=404)
