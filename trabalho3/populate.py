from decimal import Decimal
import os
import random
from faker import Faker
from django.core.files import File
from django.contrib.auth.models import User
from beerview.models import BeerStyle, Brewery, Beer, Review, Address
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trabalho3.settings')
django.setup()

fake = Faker()

def create_address():
    return Address.objects.create(
        line1=fake.street_address(),
        city=fake.city(),
        region=fake.state(),
        postal_code=fake.postcode(),
        country=fake.country_code()
    )

def create_brewery(user, image_dir):
    address = create_address()
    brewery = Brewery.objects.create(
        name=fake.company(),
        address=address,
        user=user
    )
    image_path = get_random_image_path(image_dir)
    if image_path:
        with open(image_path, 'rb') as image_file:
            brewery.picture.save(os.path.basename(image_path), File(image_file), save=True)
    return brewery

def get_random_image_path(image_dir, extensions=['.jpg', '.png']):
    images = [f for f in os.listdir(image_dir) if os.path.splitext(f)[1].lower() in extensions]
    return os.path.join(image_dir, random.choice(images))

def create_beer(brewery, beer_style, user, default_image_path):
    min_abv = Decimal(beer_style.min_abv if beer_style.min_abv else 2.0)
    max_abv = Decimal(beer_style.max_abv if beer_style.max_abv else 10.0)
    abv = Decimal(str(round(random.uniform(float(beer_style.min_abv or 2.0), float(beer_style.max_abv or 10.0)), 1)))

    beer_name_parts = [fake.color_name(), fake.word(), "Ale", "Lager", "Stout", "Porter", "IPA"]
    beer_name = ' '.join([random.choice(beer_name_parts) for _ in range(3)]).title()

    beer_description = fake.paragraph(nb_sentences=3)

    beer = Beer.objects.create(
        name=beer_name,
        brewery=brewery,
        style=beer_style,
        abv=abv,
        ibu=random.randint(10, 100),
        srm=random.randint(5, 40),
        description=beer_description,
        user=user
    )
    if default_image_path:
        with open(default_image_path, 'rb') as image_file:
            beer.picture.save(os.path.basename(default_image_path), File(image_file), save=True)
    return beer

def create_review(beer, user):
    return Review.objects.create(
        beer=beer,
        user=user,
        rating=Decimal(str(round(random.uniform(1.0, 5.0), 1))),
        comment=fake.text()
    )

def populate_all():
    brewery_image_dir = 'default_media/brewery_pictures'
    beer_image_dir = 'default_media/beer_pictures/red-ale.jpeg'

    faker_user = User.objects.get(username='faker')
    beer_styles = BeerStyle.objects.all()

    for _ in range(10):
        brewery = create_brewery(faker_user, brewery_image_dir)
        for _ in range(5):
            beer_style = random.choice(beer_styles)
            beer = create_beer(brewery, beer_style, faker_user, beer_image_dir)
            for _ in range(3):
                create_review(beer, faker_user)

    print("Fake data generation complete.")