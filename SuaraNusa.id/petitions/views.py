from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count, Sum, Q
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Petition, Support, Province, City
from .forms import UserRegisterForm, PetitionForm

def home(request):
    total_petitions = Petition.objects.count()
    total_users = User.objects.count()
    total_supports = Support.objects.count()
    
    popular_petitions = Petition.objects.annotate(
        support_count_val=Count('supports')
    ).order_by('-support_count_val')[:3]
    
    recent_petitions = Petition.objects.order_by('-created_at')[:6]
    
    context = {
        'total_petitions': total_petitions,
        'total_users': total_users,
        'total_supports': total_supports,
        'popular_petitions': popular_petitions,
        'recent_petitions': recent_petitions,
    }
    return render(request, 'petitions/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Selamat datang, {user.username}! Akun Anda berhasil dibuat.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

class PetitionListView(ListView):
    model = Petition
    template_name = 'petitions/petition_list.html'
    context_object_name = 'petitions'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset().filter(status='aktif')
        search_query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        province_id = self.request.GET.get('province')
        city_id = self.request.GET.get('city')

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
        if category:
            queryset = queryset.filter(category=category)
        if province_id:
            queryset = queryset.filter(city__province_id=province_id)
        if city_id:
            queryset = queryset.filter(city_id=city_id)
            
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['provinces'] = Province.objects.all()
        context['categories'] = Petition.CATEGORY_CHOICES
        return context

class PetitionDetailView(DetailView):
    model = Petition
    template_name = 'petitions/petition_detail.html'
    context_object_name = 'petition'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_has_supported'] = Support.objects.filter(
                user=self.request.user, petition=self.object
            ).exists()
        return context

class PetitionCreateView(LoginRequiredMixin, CreateView):
    model = Petition
    form_class = PetitionForm
    template_name = 'petitions/petition_form.html'
    success_url = reverse_lazy('petition_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Petisi berhasil dibuat!")
        return super().form_valid(form)

@login_required
def support_petition(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    if petition.status == 'selesai':
        messages.error(request, "Petisi ini sudah selesai.")
        return redirect('petition_detail', pk=pk)
        
    support, created = Support.objects.get_or_create(user=request.user, petition=petition)
    
    if created:
        messages.success(request, f"Terima kasih telah mendukung petisi: {petition.title}")
        # Check if target reached
        if petition.support_count >= petition.target_support:
            petition.status = 'selesai'
            petition.save()
    else:
        messages.info(request, "Anda sudah mendukung petisi ini.")
        
    return redirect('petition_detail', pk=pk)

def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).all().order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)
