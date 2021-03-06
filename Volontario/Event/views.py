

from django.shortcuts import render, get_object_or_404
from .models import Event
from .forms import EventForm
from .models import Task
from .forms import TaskForm
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages


############################################################################################################
def event_list(request):
    
    events = Event.objects.all
    

    return render(request, 'event/event_list.html', {'events':events})


###########################################################################################################
def task_list(request):
    
    tasks = Task.objects.all


    return render(request, 'event/task_list.html',{'tasks':tasks})
###########################################################################################################


#############################################################################
def event_detal(request, pk):
    
    detal = get_object_or_404(Event,pk=pk)
    tasks = Task.objects.all().filter(event_id=pk)
    users = User.objects.all().filter(event_id=pk)
    
     

    
    return render(request, 'event/detail.html', {'events': detal, 'tasks':tasks, 'users':users})
    

##########################################################################################################
def event_new(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.publication_date = timezone.now()
            event.save()
            messages.info(request, 'Utworzono')  
            return redirect('Event.views.event_detal', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'event/event_edit.html', {'form': form})
##########################################################################################################
def event_edit(request, pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.publication_date = timezone.now()
            event.save()
            messages.info(request, 'Zmodyfikowano')
            return redirect('Event.views.event_detal', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'event/event_edit.html', {'form': form})


##########################################################################################################
def event_remove(request, pk):
    event = get_object_or_404(Event,pk=pk)
    event.delete()
    return redirect('Event.views.event_list')
##########################################################################################################
def new_task(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            
            task = form.save(commit=False)
            task.event_id = pk
            task.save()
            
                        
            return redirect('Event.views.event_detal', pk=event.pk)
    else:
        form = TaskForm()
    return render(request, 'event/task_edit.html', {'form': form})
##########################################################################################################
def task_remove(request, pk, task_id):
    event = get_object_or_404(Event,pk=pk)
    task = get_object_or_404(Task,id=task_id)
    task.delete()
    return redirect('Event.views.event_detal', pk=event.pk)
##########################################################################################################    
def login_user(request):
  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            
            if user.is_active:
                
                login(request, user)
                 
                return redirect('Event.views.event_list')

            else:
                
                return HttpResponse("Konto wylaczone")
        else:
            
            
            return HttpResponse("Bledny login lub haslo")

    
    else:
            
           return render(request, 'event/login.html', {})

##############################################################################################################
def event_user(request,pk):
    events = get_object_or_404(Event,pk=pk)
    users = User.objects.filter(event_id=pk)
    current_user= request.user
    cur_id = current_user.id
    if request.user.is_authenticated():
        
        if users.filter(id=cur_id).exists(): 
            return redirect('Event.views.event_detal', pk=events.pk)
             
        else:
            current_user.event_id.add(pk)
            return redirect('Event.views.event_detal', pk=events.pk)
            
    else:
        return HttpResponse("Jesteś nie zalogowany ;)")
###############################################################################################################    
def user_task(request,pk,task_id):
    events = get_object_or_404(Event,pk=pk)
    users = User.objects.filter(task=task_id)
    users2 = User.objects.filter(event_id=pk)
    current_user= request.user

    cur_id = current_user.id
    if request.user.is_authenticated():
        
        if users.filter(id=cur_id).exists(): 
            return redirect('Event.views.event_detal', pk=events.pk)
        else:
            current_user.task.add(task_id)
            if users2.filter(id=cur_id).exists():
               return redirect('Event.views.event_detal', pk=events.pk)
            else: 
                current_user.event_id.add(pk)
                return redirect('Event.views.event_detal', pk=events.pk )
            
    else:
        return HttpResponse("Jesteś nie zalogowany ;)")

def user_remove(request, pk,usr):
    events = get_object_or_404(Event,pk=pk)
    current_user= request.user
    cur_id = current_user.id
    user = get_object_or_404(User,id=usr)
    tasks = Task.objects.filter(event_id=pk)

    if request.user.is_authenticated():
         
        user.event_id.remove(pk)
        for task1 in tasks: 
            id_task = task1.id
            user.task.remove(id_task)
        return redirect('Event.views.event_detal', pk=events.pk)    
    else:
        return HttpResponse("Blad")
    
def user_remove_task(request, pk,usr,tk):
    events = get_object_or_404(Event,pk=pk)
    current_user= request.user
    cur_id = current_user.id
    user = get_object_or_404(User,id=usr)
    

    if request.user.is_authenticated():
         
        user.task.remove(tk)
        return redirect('Event.views.event_detal', pk=events.pk)    
    else:
        return HttpResponse("Blad")

def user_view(request,pk,task_id):
   detal = get_object_or_404(Event,pk=pk)
   tasks = Task.objects.all().filter(event_id=pk)
   users = User.objects.all().filter(event_id=pk)
   users1 = User.objects.all().filter(task=task_id)
   task1 = get_object_or_404(Task,id=task_id)
     

    
   return render(request, 'event/detail.html', { 'events': detal, 'tasks':tasks, 'users':users, 'users1':users1, 'task1':task1})