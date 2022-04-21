from django.db import models

# Create your models here.


class Customer(models.Model):
    user_id = models.BigIntegerField(verbose_name="user_id", primary_key=True)
    username = models.CharField(verbose_name="username", max_length=200)

    def __str__(self):
        if self.username:
            return f"{self.username}  [{self.user_id}]"

        return f"{str(self.user_id)}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Category(models.Model):
    category = models.CharField(verbose_name="Категория", max_length=64, unique=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    sub_category = models.CharField(verbose_name="Подкатегория", max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.sub_category} - {self.category}"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, verbose_name="Подкатегория", on_delete=models.CASCADE,
                                     null=True, blank=True)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Состав и описание", max_length=870)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Apply(models.Model):
    customer = models.ForeignKey(Customer, verbose_name="Клиент", on_delete=models.CASCADE)  # related_name="customer_id"
    customer_name = models.CharField(verbose_name="Имя", max_length=64, null=True)
    customer_phone = models.CharField(verbose_name="Номер телефона", max_length=13, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, null=True)
    date_ordered = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class About_Us(models.Model):
    about_us = models.TextField(verbose_name="О нас", null=True, blank=True)

    def __str__(self):
        return self.about_us

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class Contact(models.Model):
    addresses = models.TextField(verbose_name="Адреса", null=True, blank=True)
    phone_numbers = models.TextField(verbose_name="Номера телефонов", null=True, blank=True)
    locations = models.TextField(verbose_name="Ссылки локаций", null=True, blank=True)

    def __str__(self):
        return self.addresses

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


