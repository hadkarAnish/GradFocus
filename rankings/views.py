from django.views import generic
from .models import City, University
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.shortcuts import render, get_object_or_404


class UserFormView(View):
    form_class = UserForm
    template_name = 'rankings/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # clean normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user.set_password(password)
            user.save()

            # return user objects if creds are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('rankings:index')

        return render(request, self.template_name, {'form': form})
        # to request.user.username to access this user's name etc


class IndexView(generic.ListView):
    template_name = 'rankings/index.html'
    context_object_name = 'all_cities'

    def get_queryset(self):
        return City.objects.all()


class IndexView2(generic.ListView):
    template_name = 'rankings/index.html'
    context_object_name = 'all_universities'

    def get_queryset(self):
        return University.objects.all()


class DetailsView(generic.DetailView):
    model = City
    template_name = 'rankings/details.html'


class CityCreate(CreateView):
    model = City
    # what fields do u want to user to fill
    fields = ['name', 'livingExpense', 'minTemperature', 'maxTemperature', 'logo']


class CityUpdate(UpdateView):
    model = City
    fields = ['name', 'livingExpense', 'minTemperature', 'maxTemperature', 'logo']


class CityDelete(DeleteView):
    model = City
    success_url = reverse_lazy('rankings:index')


class UniversityCreate(CreateView):
    model = University

    # https://stackoverflow.com/questions/10382838/how-to-set-foreignkey-in-createview
    def form_valid(self, form):
        form.instance.city = self.request.user
        fields = ['name', 'type', 'logo', 'city_id', 'isFavourite']
        return super(UniversityCreate, self).form_valid(form)
        # def form_valid(self, form):
        #     university = form.save(commit=False)
        #     university.city = self.request.user
        #     fields = ['name', 'livingExpense', 'minTemperature', 'maxTemperature']
        #     # article.save()  # This is redundant, see comments.
        #     return super(CreateArticle, self).form_valid(form)


class UniversityUpdate(UpdateView):
    model = University
    fields = ['name', 'type', 'logo', 'isFavourite']
    # model = University
    #
    # def form_valid(self, form):
    #     form.instance.city = self.request.user
    #     return super(UniversityUpdate, self).form_valid(form)


class UniversityDelete(DeleteView):
    model = University
    success_url = reverse_lazy('rankings:details')

# def create_university(request, city_id):
#     form = UniversityForm(request.POST or None, request.FILES or None)
#     city = get_object_or_404(City, pk=city_id)
#     if form.is_valid():
#         city_university = city.university_set.all()
#         for s in city_university:
#             if s.university_title == form.cleaned_data.get("name"):
#                 context = {
#                     'city': city,
#                     'form': form,
#                     'error_message': 'You already added that university',
#                 }
#                 return render(request, 'rankings/create_university.html', context)
#         university = form.save(commit=False)
#         university.city = city
#         university.type = type
#
#         university.save()
#         return render(request, 'rankings/details.html', {'city': city})
#     context = {
#         'city': city,
#         'form': form,
#     }
#     return render(request, 'rankings/create_university.html', context)
