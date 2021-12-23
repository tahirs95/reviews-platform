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
    category = models.ManyToManyField("vimbiso.Category", related_name="category")
    tags = models.ManyToManyField("vimbiso.Tags", related_name="tag_company")
    status = models.IntegerField(blank=True,null=True)
    #1 for claimed
    #2 for uncliamed
    #3 for AskingReviews
    
    def __str__(self):
        return self.user.username

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
    item_counter = models.IntegerField(default=0,null=True,blank=True)
    date_of_purchase = models.DateField()
    branch_location = models.CharField(max_length=100)
    review = models.TextField()
    ratings = models.DecimalField(max_digits=3,decimal_places=2)
    type_of_purchase = models.CharField(max_length=100,null=True,blank=True)
    resolved = models.BooleanField(default=False)
    response = models.TextField(null=True,blank=True)
    is_resolved =  models.BooleanField(default=False)
    company = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.contact

    def get_ratings(self):
        return range(int(self.ratings))

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="subscription")
    sub_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    period_start = models.DateTimeField(blank=True,null=True)
    period_end = models.DateTimeField(blank=True,null=True)
    amount_paid = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.email},{self.id}"

