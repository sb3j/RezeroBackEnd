from django.db import models
from django.conf import settings
from orders_b.models import Company

class OrderUser(models.Model):
    CATEGORY_CHOICES = (
        ('shirt', '셔츠/티셔츠'),
        ('sweater', '스웨터')
    )
    SLEEVE_CHOICES = (
        ('short', '짧은 소매'),
        ('long', '긴 소매'),
        ('sleeveless', '민소매')
    )
    NECKLINE_CHOICES_SHIRT = (
        ('round', '라운드넥'),
        ('v_neck', '브이넥'),
        ('square', '스퀘어넥'),
        ('collar', '카라넥')
    )
    NECKLINE_CHOICES_SWEATER = (
        ('round', '라운드넥'),
        ('v_neck', '브이넥'),
        ('square', '스퀘어넥'),
        ('collar', '카라넥'),
        ('turtle', '터틀/모크넥')
    )
    POCKET_CHOICES = (
        ('remove', '제거'),
        ('right', '오른쪽'),
        ('left', '왼쪽')
    )
    ETC_CHOICES = (
        ('crop', '크롭'),
        ('reduce', '폼 줄이기')
    )
    MATERIAL_CHOICES = (
        ('cotton', 'Cotton'),
        ('polyester', 'Polyester'),
        ('wool', 'Wool')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    sleeve_length = models.CharField(max_length=15, choices=SLEEVE_CHOICES)
    neckline = models.CharField(max_length=20)
    pocket = models.CharField(max_length=10, choices=POCKET_CHOICES, blank=True, null=True)
    etc = models.CharField(max_length=10, choices=ETC_CHOICES)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES)  # 새 필드 추가
    color = models.CharField(max_length=20)  # 새 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # 기업 정보 추가
