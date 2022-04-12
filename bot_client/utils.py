from django.template.context_processors import media

from bot_admin.models import *
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from django.db.models import F
from config import settings


# ------------------------------ ACTIONS WITH USERS -------------------------------------

@sync_to_async
def create_or_update_user(user_id, defaults):
    try:
        # obj, _ = Client.objects.update_or_create(tg_id=tg_id, defaults=default)
        obj = Customer.objects.update_or_create(user_id=user_id, defaults=defaults)
        # obj.save()
        return obj
    except ObjectDoesNotExist:
        return None


@sync_to_async
def check_user(user_id):
    try:
        obj = Customer.objects.get(user_id=user_id)
        # obj.save()
        return obj
    except ObjectDoesNotExist:
        return None


# ------------------------------------ PRODUCT ACTIONS -------------------------------------------

@sync_to_async
def get_all_categories():
    try:
        categories_list = []
        obj = Category.objects.all()
        for category in obj:
            categories_list.append(category.category)
        return categories_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_all_subcategories():
    try:
        subcategories_list = []
        obj = SubCategory.objects.all()
        for subcategory in obj:
            subcategories_list.append(subcategory.sub_category)
        return subcategories_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_all_products():
    try:
        product_list = []
        obj = Product.objects.all()
        for product in obj:
            product_list.append(product.name)
        return product_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_category_products_names(category_name):
    try:
        category_product_names = []
        obj = Product.objects.filter(category__category=category_name)
        for product in obj:
            # if product.sub_category is None:
            #     category_product_names.append(product.name)
            category_product_names.append(product.name)
        print(category_product_names)
        return category_product_names
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_category_products_detail(product_name):
    try:
        category_product_detail = []
        obj = Product.objects.get(name=product_name)
        category_product_detail.append(f"{settings.MEDIA_ROOT}/{obj.image}")
        category_product_detail.append(obj.name)
        category_product_detail.append(obj.description)
        category_product_detail.append(obj.price)

        return category_product_detail
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_need_subcategories(callback):
    try:
        subcategories_list = []
        obj = SubCategory.objects.filter(category__category=callback)
        for subcategory in obj:
            subcategories_list.append(subcategory.sub_category)
        return subcategories_list
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_category_products(callback):
    try:
        category_product_names = []
        obj = Product.objects.filter(category__category=callback)
        for product in obj:
            print(product.sub_category, product.name)
            if product.sub_category is None:
                print(product.sub_category, product.name)
                category_product_names.append(product.name)
        print(category_product_names)
        return category_product_names
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_subcategory_products(callback):
    try:
        subcategory_product_names = []
        obj = Product.objects.filter(sub_category__sub_category=callback)
        for product in obj:
            subcategory_product_names.append(product.name)
        return subcategory_product_names
    except ObjectDoesNotExist:
        return None


@sync_to_async
def apply_to_product(user_id, product_name):
    try:
        customer = Customer.objects.get(user_id=user_id)
        # customer_id = customer.user_id
        customer_name = customer.name
        customer_number = customer.number
        product = Product.objects.get(name=product_name)

        apply_object = Apply.objects.create(customer=customer, customer_name=customer_name,
                                            customer_phone=customer_number, product=product)
        apply_object.save()

        # customer_data = CustomerData.objects.create(apply=apply_object, customer_id=customer, customer_name=customer,
        #                                             customer_number=customer)
        # customer_data.save()

        # apply_object.customer.set(customer_data.customer_id, customer_data.customer_name, customer_data.customer_number)
        # apply_object.save()

        return apply_object
    except ObjectDoesNotExist:
        return None


@sync_to_async
def create_apply(user_id, customer_name, customer_phone, product_name):
    try:
        customer = Customer.objects.get(user_id=user_id)
        product = Product.objects.get(name=product_name)
        obj = Apply.objects.create(customer=customer, customer_name=customer_name,
                                   customer_phone=customer_phone, product=product)
        obj.save()
        apply_id = obj.pk
        return apply_id
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_apply(user_id, product_name):
    try:
        customer = Customer.objects.get(user_id=user_id)
        product = Product.objects.get(name=product_name)
        obj = Apply.objects.filter(customer=customer).filter(product=product)

        return obj
    except ObjectDoesNotExist:
        return None


@sync_to_async
# def change_apply_customer_name(user_id, product_name, customer_name):
def change_apply_customer_name(apply_id, customer_name):
    try:
        # customer = Customer.objects.get(user_id=user_id)
        # product = Product.objects.get(name=product_name)
        # obj = Apply.objects.filter(customer=customer).filter(product=product)
        # for name in obj:
        #     name.customer_name = customer_name
        #     name.save()

        obj = Apply.objects.get(pk=apply_id)
        obj.customer_name = customer_name
        obj.save()

        return obj
    except ObjectDoesNotExist:
        return None


@sync_to_async
# def change_apply_customer_phone(user_id, product_name, customer_phone):
def change_apply_customer_phone(apply_id, customer_phone):
    try:
        # customer = Customer.objects.get(user_id=user_id)
        # product = Product.objects.get(name=product_name)
        # obj = Apply.objects.filter(customer=customer).filter(product=product)
        # for phone in obj:
        #     phone.customer_phone = customer_phone
        #     phone.save()
        apply_details = []
        obj = Apply.objects.get(pk=apply_id)
        obj.customer_phone = customer_phone
        obj.save()

        apply_details.append(obj.customer_name)
        apply_details.append(obj.customer_phone)
        apply_details.append(obj.product)

        return apply_details
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_about_us():
    try:
        text_about = []
        obj = About_Us.objects.all()
        for text in obj:
            text_about.append(text.about_us)
        return text_about
    except ObjectDoesNotExist:
        return None


@sync_to_async
def get_contacts():
    try:
        text_contacts = []
        obj = Contact.objects.all()
        for text in obj:
            text_contacts.append(text.addresses)
            text_contacts.append(text.phone_numbers)
            text_contacts.append(text.locations)

        return text_contacts
    except ObjectDoesNotExist:
        return None
