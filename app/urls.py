from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views
from .forms import (
    LoginForm,
    MyPasswordChangeForm,
    MyPasswordResetForm,
    MySetPasswordForm)
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('', views.ProductView.as_view(), name='home'),
                  path('<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
                  path('postcomment/', views.ProductDetailView.as_view(), name='post-comment'),
                  path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
                  path('cart/', views.show_cart, name='show-cart'),
                  path('pluscart/', views.plus_cart, name='plus-cart'),
                  path('minuscart/', views.minus_cart, name='minus-cart'),
                  path('removecart/', views.remove_cart, name='remove-cart'),
                  path('buy/', views.buy_now, name='buy-now'),
                  path('profile/', views.ProfileView.as_view(), name='profile'),
                  path('address/', views.address, name='address'),
                  path('orders/', views.orders, name='orders'),
                  path('search/', views.SearchProductView.as_view(), name='search'),

                  path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='users/passwordchange.html',
                                                                                form_class=MyPasswordChangeForm,
                                                                                success_url='/passwordchangedone/')
                       , name='change-password'),
                  path('passwordchangedone/',
                       auth_views.PasswordChangeDoneView.as_view(template_name='users/passwordchangedone.html'),
                       name='password-change-done'),
                  path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
                                                                               form_class=MyPasswordResetForm),
                       name='password_reset'),

                  path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
                      template_name='users/password_reset_done.html'),
                       name='password_reset_done'),

                  path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name='users/password_reset_confirm.html', form_class=MySetPasswordForm),
                       name='password_reset_confirm'),

                  path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='users/password_reset_complete.html',),
                       name='password_reset_complete'),

                  path('mobile/<str:data>', views.MobileDetailView.as_view(), name='mobiledata'),
                  path('mobile/', views.MobileDetailView.as_view(), name='mobile'),
                  path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html',
                                                                       authentication_form=LoginForm), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                  path('registration/', views.CustomerRegistrationView.as_view(), name='customer-registration'),
                  path('checkout/', views.checkout, name='checkout'),
                  path('paymentdone/', views.payment_done, name='payment-done'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
