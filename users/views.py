from django.shortcuts import  render, redirect
from .forms import NuevoUsuarioForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm 

def register_request(request):
	if request.method == "POST":
		form = NuevoUsuarioForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registro Exitoso" )
			return redirect("main:homepage")
		messages.error(request, "Registro Incorrecto, vuelva a intentarlo")
	form = NuevoUsuarioForm()
	return render (request=request, template_name="users/users.html", context={"register_request": form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Usuario y/o contraseña incorrecto")
		else:
			messages.error(request,"Usuario y/o contraseña incorrecto")
	form = AuthenticationForm()
	return render(request=request, template_name="users/users.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "Has cerrado Sesion") 
	return redirect("/users/")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'change_password_form': form
    })

def configuration_users(request):
	return render(request, "users/configuration_users.html")