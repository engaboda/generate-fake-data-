from django.db import models

# Create your models here.

class UserModel(models.Model):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    addreess = models.CharField(max_length=255)
    class Meta():
        verbose_name = ("المستخدم")
        verbose_name_plural = ("المستخدمين")

    def __str__(self):
          return str(self.username)

class Employee(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name="الموظف"
        verbose_name_plural="الموظفين"
    def __str__(self):
        return self.name

class Lead(models.Model):
    employee = models.ManyToManyField(Employee ,  blank=True)
    picture = models.ImageField(null=True , blank=True,upload_to='image')
    user_model = models.ForeignKey(UserModel , on_delete=models.CASCADE , verbose_name=("المستخدم") ,  null=True , blank=True)
    user_id        = models.IntegerField(blank=True, null=True, verbose_name=('كود المستخدم'))
    user_name = models.CharField(max_length=255 , null=True , blank=True  )
    RPODateAdded   = models.DateField(blank=True, null=True, verbose_name=('تاريخ المكافأة'))
    RPODescription = models.CharField(blank=True, max_length=255,null=True, verbose_name=('الوصف'))
    RPOPoints      = models.IntegerField(blank=True, null= True, verbose_name=('عدد النقاط'))
    RPOSlug        = models.SlugField(blank=True, null=True)
    
    class Meta():
        verbose_name = ("نقطة مكافأة")
        verbose_name_plural = ("نقاط المكافآت")

    def __str__(self):
          return str(self.id)