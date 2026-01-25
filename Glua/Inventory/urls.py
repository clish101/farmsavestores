from django.contrib import admin
from django.urls import path
from . import views
from .views import stockingListView, modifyDrugUpdateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Redirect to dashboard by default after login
    path('create/', views.createDrug, name='create'),
    path('addstock/<int:pk>/', views.addStock, name='addstock'),
    path('stocking/', stockingListView.as_view(), name='stocking'),
    path('modify/<int:pk>/', modifyDrugUpdateView.as_view(), name='modify'),
    path('stocked/', views.StockAdded, name='stocked'),
    path('sell/<int:pk>/', views.sellDrug, name='sell'),
    path('lock/<int:pk>/', views.lockDrug, name='lock_item'),
    path('search/', views.search, name='search'),
    path('bin-report/search/', views.binsearch, name='bin_search'),
    path('search/stock/', views.searchstock, name='searchstock'),
    path('history/', views.salehistory, name='history'),
    path('today/', views.todaysales, name='today'),
    path('bin-report/', views.bin_report, name='bin_report'),
    path('bin-report/download/', views.download_bin_report_excel, name='download_bin_report_excel'),
    path('out-of-stock/', views.out_of_stock, name='out_of_stock'),
    path('expiring-soon/', views.expiring_soon, name='expiring_soon'),
    path('vaccines/', views.home, name='home'),
    path('low-stock/', views.low_stock_view, name='low_stock'),
    path('get_online_offline_users/', views.get_online_offline_users, name='get_online_offline_users'),
    path('locked-products/', views.locked_products, name='locked_products'),
    path('locked-products/search/', views.locked_search, name='locked_search'),
    path('locked-products/post/<int:lock_id>/', views.post_locked_product, name='post_locked_product'),
    path('locked-products/unlock/<int:lock_id>/', views.unlock_product, name='unlock_product'),
    path('add_user/', views.add_user, name='add_user'),  # URL for adding a user
    path('user_management/', views.user_management, name='user_management'),  # URL for the user management page
    path('colors/', views.show_colors, name='show_colors'),
    path('bin_filter/', views.bin_filter, name='bin_filter'),
    path('logout-inactivity/', views.logout_due_to_inactivity, name='logout_due_to_inactivity'),
    path('marketing_items/', views.marketing_items, name='marketing_items'),
    path('marketing-search/', views.marketing_search, name='marketing_search'),  
    path('issue_item/', views.issue_item, name='issue_item'),
    path('issued-items/', views.issued_items_report, name='issued_items_report'),
    path('issued-items/search/', views.issued_items_search, name='issued_items_search'),
    path('issued-items/filter/', views.issued_items_filter, name='issued_items_filter'),
    path('marketing-items/create/', views.create_marketing_item, name='create_marketing_item'),
    path('picking-list/', views.picking_list_view, name='picking_list'),
    path("add_to_picking_list/<int:drug_id>/", views.add_to_picking_list, name="add_to_picking_list"),
    path('cannisters/', views.cannister_list, name='cannister_list'),
    path('cannisters/issue/<int:cannister_id>/', views.issue_cannister, name='issue_cannister'),
    path('bin-card/', views.bin_card, name='bin_card'),
    path('bin-card/download/', views.download_bin_card_excel, name='download_bin_card_excel'),
    path('bin-card/search/', views.bin_search, name='can_search'),
    path('bin-card/filter/', views.can_filter, name='can_filter'),
    path('bin-card/return/<int:issued_cannister_id>/', views.return_cannister, name='return_cannister'),
    path('search-cannister/', views.search_cannister, name='search_cannister'),
    path('download/top-sold/', views.download_top_sold, name='download_top_sold'),
    # Client management paths
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.create_client, name='create_client'),
    path('clients/edit/<int:pk>/', views.edit_client, name='edit_client'),
    path('clients/delete/<int:pk>/', views.delete_client, name='delete_client'),
]

