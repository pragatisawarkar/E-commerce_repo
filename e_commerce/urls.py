from django.conf.urls import url
from sample import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    url('user_role_create',views.UserRoleCreateAPIView.as_view()),
    url('product_create',views.ProductCreateAPIView.as_view()),

    url('customer_create',views.CustomerCreateAPIView.as_view()),
    url('vendor_create',views.VendorCreateAPIView.as_view()),

    url('customer_login',views.CustomerLoginApiView.as_view()),
    url('vendor_login',views.VendorLoginAPIView.as_view()),

    url('place_order',views.PlaceOrderAPIView.as_view()),
    url('accept_order',views.AcceptOrderAPIView.as_view()),
]
