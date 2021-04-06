from django.db import models
from django_countries.fields import CountryField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from tongghor.utils import random_username_generator
# Create your models here.
class GenderChoices(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'others'


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=12,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    photo = models.FileField(upload_to='users', blank=True, null=True)
    country = CountryField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GenderChoices.choices)
    deleted_by = models.ForeignKey('self', related_name='user_deleted_by', on_delete=models.DO_NOTHING ,null=True)
    blocked_users = models.ManyToManyField('self', related_name='blocked_users')
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_reason = models.TextField(blank=True, null=True)
    term_and_condition_accepted = models.BooleanField(default=False)
    privacy_policy_accepted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = "tongghor_users"
        verbose_name = "tongghor_user"
        verbose_name_plural = "tongghor_users"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self._new = False
        if self.pk is None:
            self._new = True
            self.username = random_username_generator(self)
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
        


class UnitOfHistory(models.Model):
    title = models.CharField(
        max_length=30,
        blank=True, null=True,
        verbose_name="Name of Content",
        help_text="The name of the content from which this unit of history is generated"
    )
    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name="Description of Content",
        help_text="From where this unit of history is generated"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="history"
    )
    created = models.DateTimeField(auto_now_add=True)
    # Generic Foreignkey Configuration. DO NOT CHANGE
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()