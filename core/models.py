from django.db import models
from django.urls import reverse
import random
import string


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    customer_code = models.CharField(max_length=4, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='customer_qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_customer_code(self):
        """Genera un código único de 4 dígitos."""
        while True:
            code = ''.join(random.choices(string.digits, k=4))
            if not Customer.objects.filter(customer_code=code).exists():
                return code

    def generate_qr_code(self):
        """Genera un QR que apunta a la vista pública del cliente."""
        import qrcode
        from django.core.files import File
        from io import BytesIO

        qr_url = reverse('customer_status', args=[self.customer_code])
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(f"http://localhost:8000{qr_url}")
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"qr_customer_{self.customer_code}.png", File(buffer), save=True)

    def save(self, *args, **kwargs):
        """Genera el código y el QR al guardar el cliente."""
        if not self.customer_code:
            self.customer_code = self.generate_customer_code()
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (ID: {self.customer_code})"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('PROCESSING', 'En proceso'),
        ('READY', 'Listo para recoger'),
        # --- LÍNEA AÑADIDA ---
        ('DELIVERED', 'Entregado'), 
        ('CANCELLED', 'Anulado'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Efectivo'),
        ('YAPE', 'Yape'),
        ('PLIN', 'Plin'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Falta Pagar'),
        ('PAID', 'Pagado'),
        ('PARTIAL', 'Parcialmente Pagado'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Peso en kg
    weight_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=5.00)  # Precio por kg
    categories = models.ManyToManyField(Category, through='OrderCategory')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROCESSING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    partial_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Monto pagado parcialmente
    notes = models.TextField(blank=True, null=True)  # Campo de notas
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = self.generate_order_code()
        super().save(*args, **kwargs)

    def generate_order_code(self):
        """Genera un código único de 6 caracteres para el pedido."""
        length = 6
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
            if not Order.objects.filter(order_code=code).exists():
                return code

    def total_price(self):
        weight_price = (self.weight or 0) * self.weight_price_per_kg
        category_price = sum(item.quantity * item.category.price for item in self.ordercategory_set.all())
        return weight_price + category_price

    def remaining_amount(self):
        """Calcula el monto faltante para pagar."""
        if self.payment_status == 'PARTIAL':
            return self.total_price() - self.partial_amount
        return self.total_price() if self.payment_status == 'PENDING' else 0

    def generate_qr_code(self):
        import qrcode
        from django.core.files import File
        from io import BytesIO

        qr_url = reverse('order_status', args=[self.id])
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(f"http://localhost:8000{qr_url}")
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        self.qr_code.save(f"qr_{self.id}.png", File(buffer), save=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.customer.name}"

class OrderCategory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.category.name} x{self.quantity} (Pedido {self.order.id})"
    
class AppConfiguration(models.Model):
    key = models.CharField(max_length=50, primary_key=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.key

    # Para asegurar que solo haya una instancia de cada ajuste
    class Meta:
        verbose_name_plural = "Configuraciones de la Aplicación"

# === INICIO DE CÓDIGO AÑADIDO ===

class Product(models.Model):
    """Representa un producto que se puede vender en la tienda."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Producto")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Stock")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name="Imagen del Producto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Sale(models.Model):
    """Representa una transacción de venta de productos."""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monto Total")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        customer_name = self.customer.name if self.customer else "Venta de Mostrador"
        return f"Venta #{self.id} - {customer_name}"

    def calculate_total(self):
        """Calcula el total de la venta a partir de sus artículos."""
        total = sum(item.quantity * item.unit_price for item in self.saleitem_set.all())
        self.total_amount = total
        self.save()

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"


class SaleItem(models.Model):
    """Representa un artículo dentro de una venta."""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Venta")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en Venta #{self.sale.id}"

    def save(self, *args, **kwargs):
        # Guarda el precio del producto al momento de la venta
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Artículo de Venta"
        verbose_name_plural = "Artículos de Venta"
# === FIN DE CÓDIGO AÑADIDO ===