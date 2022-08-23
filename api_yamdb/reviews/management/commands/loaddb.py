import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Genre_title, Review, Title
from users.models import User


class Command(BaseCommand):
    help = "Load test DB from dir (../static/data/)"

    def handle(self, *args, **kwargs):
        with open('static/data/category.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            Category.objects.all().delete()

            for row in reader:
                print(row)

                table = Category(id=row[0],
                                 name=row[1],
                                 slug=row[2],)
                table.save()
            file.close

        with open('static/data/users.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            User.objects.all().delete()

            for row in reader:
                print(row)

                table = User(id=row[0],
                             username=row[1],
                             email=row[2],
                             role=row[3],
                             bio=row[4],
                             first_name=row[5],
                             last_name=row[6],)
                table.save()
            file.close

        with open('static/data/genre.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            Genre.objects.all().delete()

            for row in reader:
                print(row)

                table = Genre(id=row[0],
                              name=row[1],
                              slug=row[2],)
                table.save()
            file.close

        with open('static/data/titles.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            Title.objects.all().delete()

            for row in reader:
                print(row)

                cat, _ = Category.objects.get_or_create(id=row[3])

                table = Title(id=row[0],
                              name=row[1],
                              year=row[2],
                              category=cat,
                              )
                table.save()
            file.close

        with open('static/data/genre_title.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            Genre_title.objects.all().delete()

            for row in reader:
                print(row)

                title, _ = Title.objects.get_or_create(id=row[1])
                genre, _ = Genre.objects.get_or_create(id=row[2])

                table = Genre_title(id=row[0],
                                    title_id=title,
                                    genre_id=genre,
                                    )
                table.save()
            file.close

        with open('static/data/review.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            Review.objects.all().delete()

            for row in reader:
                print(row)
                title, _ = Title.objects.get_or_create(id=row[1])
                author_id, _ = User.objects.get_or_create(id=row[3])

                table = Review(id=row[0],
                               title_id=title,
                               text=row[2],
                               author=author_id,
                               score=row[4],
                               pub_date=row[5],)
                table.save()
            file.close

        with open('static/data/comments.csv', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            Comment.objects.all().delete()

            for row in reader:
                print(row)
                review, _ = Review.objects.get_or_create(id=row[1])
                author_id, _ = User.objects.get_or_create(id=row[3])

                table = Comment(id=row[0],
                                review_id=review,
                                text=row[2],
                                author=author_id,
                                pub_date=row[4],)
                table.save()
            file.close
