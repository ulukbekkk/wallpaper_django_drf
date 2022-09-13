from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

from decouple import config


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # if extra_fields.get('is_staff') == False and extra_fields.get('is_superuser') == False:
        user.generate_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    password = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='images', upload_to='user_img', default='default.png')
    is_active = models.BooleanField('active', default=False)
    activation_code = models.CharField('activation code', max_length=36, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def generate_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=8, allowed_chars='qwertyuiopasdfghjklzxcvbnm1234567890')
        self.activation_code = code
        self.save()

    def send_activation_code(self):
        from django.core.mail import send_mail
        self.generate_activation_code()
        activation_url = f'{config("DOMAIN")}api/v1/account/activate/{self.activation_code}/'
        message = f'Activate your account, follow this link {activation_url}'
        send_mail("Activate account", message, 'wallpaper@gmail.com', [self.email])