from django.db import models
from django.db.models import Sum


class Director(models.Model):
    name = models.CharField(max_length=100)

    @property
    def count_movies(self):
        return self.movies.all().count()

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, related_name="movies", null=True, blank=True
    )

    def __str__(self):
        return self.title

    @property
    def reviews(self):
        review = Review.objects.filter(movie=self)
        return [{"text"} for i in review]

    @property
    def rating(self):
        s = Review.objects.all().aggregate(Sum("stars"))["stars__sum"]
        c = Review.objects.all().count()
        try:
            return s / c
        except:
            return 0


CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
)


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True
    )
    stars = models.IntegerField(default=1, choices=CHOICES, null=True, blank=True)

    def __str__(self):
        return self.text
