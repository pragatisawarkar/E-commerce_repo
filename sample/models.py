from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


def is_vendor(value):
    user_role = User.objects.filter(id=value.id)[0].role.title
    if user_role != 'vendor':
        raise ValidationError('Provided id is not a vendor')


def is_customer(value):
    user_role = User.objects.filter(id=value.id)[0].role.title
    if user_role != 'customer':
        raise ValidationError('Provided id is not a customer')


class UserRole(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email'), max_length=100, unique=True)
    role = models.ForeignKey(UserRole, on_delete=models.DO_NOTHING, related_name='user')

    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.FloatField()


class Order(models.Model):
    ORDER_STATUS = (
                ('placed', 'placed',),
                ('accepted', 'accepted',),
                ('canceled', 'canceled',)
            )

    order_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                 related_name='customer_order', validators=[is_customer, ])
    vendor = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                               related_name='vendor_order', validators=[is_vendor, ])
    order_status = models.CharField(max_length=8, choices=ORDER_STATUS, default='placed')


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_item')


