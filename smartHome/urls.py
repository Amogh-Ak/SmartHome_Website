from os import name
from typing import Set
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.messages.api import success
from smartHome.forms import ChangePasswordForm, LoginForm, ResetPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path("devices/",views.devices_info,name="devices"),
    path("devices/<slug:data>",views.devices_info,name="devicesdata"),

    path("register/",views.CustomerRegisterView.as_view(),name="customerRegister"),
    path("accounts/login/",auth_views.LoginView.as_view(template_name="smartHome/login.html",authentication_form=LoginForm),name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'),name="logout"),

    path("changePassword/",auth_views.PasswordChangeView.as_view(template_name="smartHome/changePassword.html",form_class=ChangePasswordForm, success_url='/passwordChangeDone/'),name='changePassword'),
    path("passwordChangeDone/", auth_views.PasswordChangeDoneView.as_view(template_name="smartHome/changePasswordDone.html"),name="changePasswordDone"),
    
    path('passwordReset/',auth_views.PasswordResetView.as_view(template_name="smartHome/passwordReset.html",form_class=ResetPasswordForm),name='resetPassword'),
    path('passwordReset/done/',auth_views.PasswordResetDoneView.as_view(template_name="smartHome/passwordResetDone.html"),name="password_reset_done"),
    path("passwordResetConfirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="smartHome/passwordResetConfirm.html", form_class=SetPasswordForm),name="password_reset_confirm"),
    path('passwordResetComplete',auth_views.PasswordResetCompleteView.as_view(template_name="smartHome/passwordResetComplete.html"),name="password_reset_complete"),

    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("address/",views.address,name="address"),

    path("add-to-cart/",views.add_to_cart,name='add-to-cart'),
    path("cart/",views.show_cart,name="showcart"),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    
    path('cart/checkout/',views.checkout,name="checkout"),
    path('paymentdone/',views.payment_done, name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    
    path("search",views.search_bar,name="search"),
]
