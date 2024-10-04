from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=255)  # Название товара
    description = models.TextField()  # Описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара
    stock = models.PositiveIntegerField()  # Количество на складе
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)  # Категория товара
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # Изображение товара
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)  # Название категории
    slug = models.SlugField(unique=True)  # Для создания ЧПУ ссылок (URL)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)  # Покупатель
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания заказа
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Ожидает'), ('Shipped', 'Отправлено'), ('Delivered', 'Доставлено')],
        default='Pending'
    )  # Статус заказа
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая сумма заказа


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Заказ
    product = models.ForeignKey(Item, on_delete=models.CASCADE)  # Товар
    quantity = models.PositiveIntegerField()  # Количество товаров
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент заказа

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Заказ
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма оплаты
    method = models.CharField(
        max_length=20,
        choices=[('Credit Card', 'Кредитная карта'), ('PayPal', 'PayPal'), ('Bank Transfer', 'Банковский перевод')]
    )  # Способ оплаты
    payment_date = models.DateTimeField(auto_now_add=True)  # Дата оплаты

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"


class DeliveryAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Покупатель
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Заказ
    address = models.TextField()  # Адрес доставки
    city = models.CharField(max_length=255)  # Город
    postal_code = models.CharField(max_length=10)  # Почтовый индекс
    country = models.CharField(max_length=255)  # Страна

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"


