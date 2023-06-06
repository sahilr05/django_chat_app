from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Interest
from .types import UserState
from .forms import EditUserForm, EmailPhoneLoginForm
from .forms import MyAccountForm
from .forms import UserForm
from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate

class MyLoginView(LoginView):
    template_name = 'login.html'
    form_class = EmailPhoneLoginForm
    success_url = 'add_interest'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:add_interest')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email_or_phone = cd['email_or_phone']
            if '@' in email_or_phone:  # Email login
                kwargs = {'email': email_or_phone}
            else:  # Phone number login
                kwargs = {'phone_number': email_or_phone}
            
            email = User.objects.filter(**kwargs).first().email

            user = authenticate(request, email=email, password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in!', 'success')
                return redirect('accounts:add_interest')
            else:
                messages.error(request, 'Your email or password is incorrect!', 'danger')
        return render(request, self.template_name, {'form': form})


@login_required
def edit_user(request, pk):
    if not request.user.is_superuser:
        return redirect("checkerapp:home")
    user_info = User.objects.get(id=pk)

    form = EditUserForm(request.POST or None, instance=user_info)
    if form.is_valid():
        form.save()
        messages.success(request, f"Account info updated ! !")
        return redirect("accounts:my_account")

    context = {"form": form}
    return render(request, "edit_user.html", context)



@login_required
def my_account(request):
    user_info = User.objects.get(user_id=request.user.pk)
    if user_info:
        form = MyAccountForm(request.POST or None, instance=user_info)
    else:
        form = MyAccountForm()
    if form.is_valid():
        form.save()
        messages.success(request, f"Account info updated ! !")
        return redirect("accounts:add_interest")

    context = {"form": form}
    return render(request, "my_account.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, f"Password Changed !")
            return redirect("checkerapp:home")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    context = {"form": PasswordChangeForm(request.user)}
    return render(request, "change_pass.html", context)


def delete_interest(request, pk):
    user = request.user
    interest = Interest.objects.get(interest_id=pk)
    user.interests.remove(interest)
    return redirect("accounts:add_interest")

def add_interest(request):
    if request.method == "POST":
        user = request.user
        selected_interests = request.POST.getlist("interest_listxblocks")
        interest_qs = Interest.objects.filter(interest_id__in=selected_interests)
        for interest in interest_qs:
            user.interests.add(interest)
        return redirect("accounts:add_interest",)

    # form = InterestForm()
    user_interest_list = request.user.interests.all()
    all_interest = Interest.objects.exclude(pk__in=user_interest_list.values_list('pk', flat=True))
    context = {
        # "form": form,
        "user_interest_list": user_interest_list,
        "all_interest": all_interest,
        "flag": True if user_interest_list.count() else False
    }
    return render(request, "add_interest.html", context)

def signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data.get("email")
            phone_number = user_form.cleaned_data.get("phone_number")
            password = user_form.cleaned_data.get("password")
            gender = user_form.cleaned_data.get("gender")
            data = user_form.cleaned_data
            del data["confirm_password"]
            user = User.objects.create_user(
                **user_form.cleaned_data
            )
            user.save()
            return redirect("accounts:login")

    context = {"form": UserForm()}
    return render(request, "signup.html", context)


@login_required
def toggle_status(request):
    new_status = UserState.ONLINE if request.user.status == UserState.OFFLINE else UserState.OFFLINE
    user = request.user
    user.status = new_status
    user.save()

    return redirect(request.META.get('HTTP_REFERER'))
