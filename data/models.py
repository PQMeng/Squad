from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    account_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    profile_photo = models.FileField(default=None, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email + "; " + self.first_name + "; " + self.last_name + "; " + self.password + "; " + \
               str(self.is_admin) + "; " + str(self.is_active) + "; " + str(self.is_staff) + "; " + \
               str(self.is_superuser) + "; " + str(self.is_instructor)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Class(models.Model):
    class_id = models.BigAutoField(primary_key=True)
    class_name = models.CharField(max_length=200, unique=True, default=None)
    description = models.TextField()
    instructor = models.ForeignKey('Account', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Classes"


class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE)
    sender_instance = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='send_Account')
    receiver_instance = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='receiver_Account')
    status = models.IntegerField()
    read = models.BooleanField()


class Group(models.Model):
    group_id = models.BigIntegerField(primary_key=True)  # It's a sql type ForeignKey referred to notification_id
    group_name = models.CharField(max_length=50, default='')


class Relationship(models.Model):
    student_instance = models.ForeignKey('Account', on_delete=models.CASCADE)
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE)
    group_id = models.BigIntegerField(default=-1)  # It's a sql type ForeignKey referred to notification_id

    def __str__(self):
        return 'account ' + str(self.student_instance.account_id) + ' in class ' + \
               str(self.class_instance.class_id) + ' ' + self.class_instance.class_name + ' group ' + \
               str(self.group_id)


class Skill_label(models.Model):
    student_instance = models.ForeignKey('Account', on_delete=models.CASCADE)
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE)
    label = models.CharField(max_length=20)

    def __str__(self):
        return self.label + ' ' + \
               self.student_instance.first_name + ' ' + \
               self.student_instance.last_name


# a student's self description in a class
class Description(models.Model):
    student_instance = models.ForeignKey('Account', on_delete=models.CASCADE)
    class_instance = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='+')
    description = models.TextField()


