import csv

from reviews.models import Category, Comment, Genre, Genre_title, Review, Title


def run():
    with open('static/data/category.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Category.objects.all().delete()

        for row in reader:
            print(row)

            category = Category(name=row[1],
                                slug=row[2],)
            category.save()
