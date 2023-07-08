from django.urls import path
from . import views

urlpatterns = [
    path('createcustomer',views.CreateCustomer.as_view({'post':'create'}),name='create-customer'),
    path('customer/update/<pk>',views.UpdateCustomer.as_view({'put':'put'}),name='product-create-list'),
    path('singlecustomer',views.SingleGetCustomer.as_view({'get':'get'}),name='singlecustomer'),
    path('customer/delete/<pk>',views.DeleteCustomer.as_view({'delete':'delete'}),name='customer-delete'),
    path('productcreate',views.ProductCreate.as_view({'post':'post'}),name='product-create'),
    path('listproduct',views.ProductAllList.as_view({'get':'get'}),name='list-product'),
    path('product-detail/<pk>',views.ProductDetail.as_view({'get': 'get_product', 'post': 'post'}),name='product-detail'),
    path('product/updatedetail/<pk>',views.ProductUpdateDetail.as_view({'put':'update'}),name='product-detail-update'),







]