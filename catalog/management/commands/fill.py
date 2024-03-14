import json

from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('data.json', 'r') as file:
            category_list = []
            list = json.load(file)
            for line in list:
                for key, item in line.items():
                    if item == 'catalog.category':
                        category_list.append(line)
            print(category_list)
            return category_list


    @staticmethod
    def json_read_products():
        with open('data.json', 'r') as file:
            products_list = []
            list = json.load(file)
            for line in list:
                for key, item in line.items():
                    if item == 'catalog.product':
                        products_list.append(line)
            return products_list

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(id=category['pk'], title=category["fields"]["title"], description=category["fields"]["description"])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(
                Product(id=product['pk'], title=product["fields"]['title'],
                        description=product["fields"]['description'],
                        avatar=product["fields"]['avatar'],
                        category=Category.objects.get(pk=product["fields"]['category']),
                        price=product["fields"]['price'],
                        created_at=product["fields"]['created_at'],
                        updated_at=product["fields"]['updated_at'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)