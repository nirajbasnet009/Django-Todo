from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,UpdateView,DeleteView
from django.views.generic.edit import CreateView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.urls import reverse_lazy
from . models import Task
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def home(request):
#     return render(request, 'todo/home.html')

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description','complete']

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('task-list')

class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
    
    # Adding search features in the todos list
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task-list')
 
class CustomRegisterView(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')
    
    # this will save the form and login the user automatically after successful registration
    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super().form_valid(form)
    
    # this will prevent the logged in user to go back to the register page
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super().get(self,*args,**kwargs)