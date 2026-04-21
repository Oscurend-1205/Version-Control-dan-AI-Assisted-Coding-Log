from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.province.name}"

class Petition(models.Model):
    CATEGORY_CHOICES = [
        ('sosial', 'Sosial'),
        ('pendidikan', 'Pendidikan'),
        ('lingkungan', 'Lingkungan'),
        ('kesehatan', 'Kesehatan'),
        ('politik', 'Politik'),
        ('ekonomi', 'Ekonomi'),
        ('lainnya', 'Lainnya'),
    ]

    STATUS_CHOICES = [
        ('aktif', 'Aktif'),
        ('selesai', 'Selesai'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='petitions')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='petitions/', blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='petitions')
    target_support = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def support_count(self):
        return self.supports.count()

    @property
    def progress_percentage(self):
        if self.target_support == 0:
            return 0
        percentage = (self.support_count / self.target_support) * 100
        return min(round(percentage, 1), 100)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('petition_detail', kwargs={'pk': self.pk})

class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supports')
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='supports')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'petition')

    def __str__(self):
        return f"{self.user.username} supported {self.petition.title}"
