from django.shortcuts import render,reverse,redirect,resolve_url

# from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.views.generic import CreateView

from .forms import SignupForm,LoginForm,UpdateDefaultProfile,UpdateCustomProfile
from django.contrib import messages
from customers.models import Customer
from orders.models import Order
from registers.models import Profile
from products.models import Product,HistConf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.http import HttpResponse, HttpResponseRedirect
import json

from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from registers.filters import CustomerFilter

# from datetime import datetime
# from django.utils import timezone
from datetime import datetime, timedelta