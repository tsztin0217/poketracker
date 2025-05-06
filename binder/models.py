from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


GRADED = (
    ('', 'Select an option'),
    ('Y', 'Yes'),
    ('N', "No")
)

METHODS = (
    ('', 'Select a method'),
    ('E', 'Ebay'),
    ('S', 'Store'),
    ('P', 'Pokemon Center'),
    ('O', 'Other'),
)

class Binder(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("binder-detail", kwargs={"pk": self.pk})
    
    
class UserCardInfo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    binder = models.ForeignKey('Binder', on_delete=models.CASCADE, related_name='cards')
    card_id = models.CharField(max_length=100) 
    name = models.CharField(max_length=100, blank=True, null=True)
    img_url_large = models.URLField(blank=True, null=True)
    img_url_small = models.URLField(blank=True, null=True)

    date_obtained = models.DateField(blank=True, null=True)
    method_obtained = models.CharField(max_length=1, choices=METHODS, blank=True, null=True)
    graded = models.CharField(
        max_length=1, 
        choices=GRADED, 
        blank=True, 
        null=True
        )
    grade = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    price_paid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    comments = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Card ID {self.card_id} from {self.binder.name} "
    
    def get_absolute_url(self):
        return reverse("user-card-detail", kwargs={"pk": self.pk})
    
