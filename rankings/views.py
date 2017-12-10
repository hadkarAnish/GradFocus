from django.views import generic
from django.db import connection
from .models import City, University, Program, Student, Course
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin


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


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = City
    template_name = 'rankings/index.html'
    context_object_name = 'all_cities'

    def get_queryset(self):
        return City.objects.all()


class IndexViewStudent(generic.ListView):
    model = Student
    template_name = 'rankings/student_index.html'
    context_object_name = 'all_students'

    def get_queryset(self):
        return Student.objects.all()


# details views


class DetailsView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = City
    template_name = 'rankings/details.html'


class UniversityDetailsView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = University
    template_name = 'rankings/university_details.html'


class ProgramDetailsView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = Program
    template_name = 'rankings/program_details.html'


# class ISDetailsView(generic.DetailView):
class ISListsView(LoginRequiredMixin, generic.ListView):
    login_url = '/login_user/'
    redirect_field_name = ''
    template_name = 'rankings/is_details.html'
    context_object_name = 'all_is_ranks'

    def get_queryset(self):
        return Program.objects.select_related('university').filter(pName="IS")


class BAListsView(LoginRequiredMixin, generic.ListView):
    login_url = '/login_user/'
    redirect_field_name = ''
    template_name = 'rankings/ba_details.html'
    context_object_name = 'all_ba_ranks'

    def get_queryset(self):
        return Program.objects.select_related('university').filter(pName="BA")


class MBAListsView(LoginRequiredMixin, generic.ListView):
    login_url = '/login_user/'
    redirect_field_name = ''
    template_name = 'rankings/mba_details.html'
    context_object_name = 'all_mba_ranks'

    def get_queryset(self):
        return Program.objects.select_related('university').filter(pName="MBA")


class MatchesView(LoginRequiredMixin, generic.ListView):
    login_url = '/login_user/'
    redirect_field_name = ''
    template_name = 'rankings/matches_details.html'
    context_object_name = 'students_matches'

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("select s.sfirstname,s.slastname, u.name ,p.pName, p.rank "
                           "from rankings_student s,rankings_matches m,rankings_program p, rankings_university u "
                           "where s.id=m.student_id and p.id=m.program_id and u.id=p.university_id")
            row = cursor.fetchall()
            return row


class CityCreate(LoginRequiredMixin, CreateView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = City
    # what fields do u want to user to fill
    fields = ['name', 'livingExpense', 'minTemperature', 'maxTemperature', 'logo']


# update views
class CityUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = City
    fields = ['name', 'livingExpense', 'minTemperature', 'maxTemperature', 'logo']


class UniversityUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = University
    fields = ['name', 'type', 'logo']


class ProgramUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = Program
    fields = ['pName', 'rank', 'acceptedGRE', 'acceptedGMAT', 'acceptedTOEFL', 'minCGPA', 'feePerCredit', 'avgWorkExp']


class CourseUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = Course
    fields = ['courseName', 'courseDescription']


# Delete Functions
class CityDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = City
    success_url = reverse_lazy('rankings:index')


class UniversityDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = University
    success_url = reverse_lazy('rankings:index')


class ProgramDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = Program
    success_url = reverse_lazy('rankings:index')


class CourseDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login_user/'
    redirect_field_name = ''
    model = Course
    success_url = reverse_lazy()


class AboutPageView(TemplateView):
    template_name = 'rankings/about_details.html'


# login logout

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'rankings/login.html', context)


def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'rankings/login.html', {'error_message': 'Your account has been disabled'})
    else:
        return render(request, 'rankings/login.html', {'error_message': 'Invalid login'})
