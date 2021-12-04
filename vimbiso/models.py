from django.db import models
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey

class User(AbstractUser):
    address = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=25, null=True, blank=True)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    image = models.ImageField(upload_to="media",default=None)
    description = models.TextField(null=True, blank=True)
    verified =  models.BooleanField(default=False)
    category = models.ManyToManyField("vimbiso.Category", related_name="company")
    tags = models.ManyToManyField("vimbiso.Tags", related_name="tag_company")
    
    def __str__(self):
        return self.user.username

class BusinessSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="subscription")
    plan_type = models.CharField(max_length=100)
    subscription_id = models.TextField(null=True, blank=True)
    paid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class BusinessImages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="images")
    img = models.ImageField(upload_to="media")

class Tags(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE,related_name="tags")
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag

class Category(MPTTModel):
    name = models.CharField(max_length=200,unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='child',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "categories"   

    def __str__(self):                           
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

class Reviews(models.Model):
    contact = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    purchased_item = models.CharField(max_length=100)
    item_counter = models.IntegerField(default=0)
    date_of_purchase = models.DateField()
    branch_location = models.CharField(max_length=100)
    review = models.TextField()
    ratings = models.DecimalField(max_digits=3,decimal_places=2)
    resolved = models.BooleanField(default=False)
    response = models.TextField()
    is_resolved =  models.BooleanField(default=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact

    def get_ratings(self):
        return range(int(self.ratings))

