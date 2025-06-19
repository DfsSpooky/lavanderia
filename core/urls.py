from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_order/', views.add_order, name='add_order'),
    path('order_status/<int:order_id>/', views.order_status, name='order_status'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('update_payment_status/<int:order_id>/', views.update_payment_status, name='update_payment_status'),
    path('manage_customer/<str:customer_code>/', views.manage_customer_orders, name='manage_customer_orders'),
    path('customer/<str:customer_code>/', views.customer_status, name='customer_status'),
    path('receive_order/', views.receive_order, name='receive_order'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('download_order_pdf/<int:order_id>/', views.download_order_pdf, name='download_order_pdf'),
    path('payment_audit/', views.payment_audit, name='payment_audit'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('search_customers/', views.search_customers, name='search_customers'),
    path('accounts/', include('core.auth_urls', namespace='accounts')),
    path('settings/', views.manage_settings, name='manage_settings'),
    path('deliver_order/<int:order_id>/', views.mark_order_as_delivered, name='deliver_order'),
    # === INICIO DE CÓDIGO AÑADIDO ===
    # URLs para la Tienda
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # URLs para Ventas
    path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/', views.sales_history, name='sales_history'),
    path('sales/receipt/<int:sale_id>/', views.sale_receipt_pdf, name='sale_receipt_pdf'),
    # === FIN DE CÓDIGO AÑADIDO ===
    path('order/ticket/<int:order_id>/', views.print_order_ticket, name='print_order_ticket'),

]