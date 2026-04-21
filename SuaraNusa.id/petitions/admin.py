from django.contrib import admin
from .models import Province, City, Petition, Support

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ('province',)

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'city', 'status', 'support_count', 'target_support')
    list_filter = ('category', 'status', 'city__province')
    search_fields = ('title', 'description')

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('user', 'petition', 'created_at')
    list_filter = ('petition',)
