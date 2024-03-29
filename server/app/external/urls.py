from django.urls import path
from . import views


urlpatterns = [
    path('v1/import/project/', views.ExternalExportProject.as_view(), name='external-export-project'),
    path('v1/import/product/', views.ExternalExportProduct.as_view(), name='external-export-product'),
    path('v1/import/update-billing/', views.ExternalExportBillingUpdate.as_view(), name='external-export-update-billing'),
]
