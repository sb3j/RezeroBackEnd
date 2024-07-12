from django.db import models

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('corporate', 'Corporate'),
    ]
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='general')


    def __str__(self):
        return self.question

