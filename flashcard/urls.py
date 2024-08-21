from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("create-folder", views.create_folder, name="create_folder"),
    path("create-set", views.create_set, name="create_set"),
    path("folder/<int:folder_id>", views.folder, name="folder"),
    path("search/", views.search, name="search"),
    path("add-set-to-folder", views.add_set_to_folder, name="add-set-to-folder"),
    path("remove-set-from-folder/<int:set_id>", views.remove_set_from_folder, name="remove-set-from-folder"),
    path("delete-folder/<int:folder_id>", views.delete_folder, name="delete-folder"),
    path("delete-set/<int:set_id>", views.delete_set, name="delete-set"),
    path("set/<int:set_id>", views.set, name="set"),
    path("about/", views.about, name="about"),

    # API route
    path("get-cards/<int:set_id>", views.get_cards, name="get-cards")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)