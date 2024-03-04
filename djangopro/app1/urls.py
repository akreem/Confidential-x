from django.urls import path
from . import views

urlpatterns = [
    path("main", views.main, name="main"),
    path("", views.index, name="index"),
    path("home", views.findcivil, name="home"),
    path("home1", views.home1, name="home1"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("societes", views.get_soc, name="societes"),
    path("addsocietes", views.create_societe, name="addsocietes"),
    path("enqextintupdate", views.enqextint_update, name="enqextintupdate"),
    path("asyncenqext/<param>", views.asyncenqext, name="asyncenqext"),
    path("asyncenqextsave", views.asyncenqextCommit, name="asyncenqextsave"),
    path("runcommit/<idtrav>", views.asyncenqextRunCommit, name="asyncenqextRunCommit"),
    path("findcour", views.findcour, name="findcour"),
    path("appliedprev/<param>", views.appliedprev, name="appliedprev"),
    path("profile/<cin>", views.profile, name="profile"),
    path("exportapp4/<param>", views.exportapp4, name="exportapp4"),
    path("cdjobs", views.cdjobs, name="cdjobs"),
    path("cdetails/<param>", views.cd_details, name="cdetails"),
    
]