from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
def register_view (request):
   if request.method == 'POST':
    form=UserCreationForm(request.POST)
    if form.is_valid():
        user=form.save()
        login(request,user)
        return redirect('/')
   else:
        initial_data = {'username':'','password1':'','password2':''}
        form=UserCreationForm(initial=initial_data)
   return render(request, 'user/register.html',{'form':form})
        
        

def login_view (request):
    form = AuthenticationForm() 

    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('/')
    """else:
        initial_data = {'username':'','password1':''}
        form=UserCreationForm(initial=initial_data)"""
    return render(request, 'user/login.html',{'form':form})
        

def dashboard_view (request):
  return render(request, 'dashboard.html')

def logout_view (request):
   logout(request)
   return redirect('login')
