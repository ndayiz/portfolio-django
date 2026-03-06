from django.urls import path
from .views import home, project_detail, robots_txt, sitemap_xml

urlpatterns = [
    path("", home, name="home"),
    path("projects/<int:pk>/", project_detail, name="project_detail"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
]