from petitions.models import Province, City

def seed():
    provinces_data = {
        'DKI Jakarta': ['Jakarta Pusat', 'Jakarta Selatan', 'Jakarta Timur', 'Jakarta Barat', 'Jakarta Utara'],
        'Jawa Barat': ['Bandung', 'Bogor', 'Bekasi', 'Depok', 'Sukabumi'],
        'Jawa Tengah': ['Semarang', 'Surakarta', 'Magelang', 'Tegal', 'Salatiga'],
        'Jawa Timur': ['Surabaya', 'Malang', 'Sidoarjo', 'Gresik', 'Kediri'],
        'DI Yogyakarta': ['Yogyakarta', 'Sleman', 'Bantul', 'Kulon Progo', 'Gunung Kidul'],
        'Bali': ['Denpasar', 'Badung', 'Gianyar', 'Tabanan', 'Buleleng'],
    }

    for prov_name, cities in provinces_data.items():
        province, created = Province.objects.get_or_create(name=prov_name)
        for city_name in cities:
            City.objects.get_or_create(name=city_name, province=province)
    
    print("Seed data successful!")

if __name__ == '__main__':
    seed()
