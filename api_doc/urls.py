from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="api_doc/start.html", content_type="text/html"), name="api-doc-start"),
    url(r'^auth$', TemplateView.as_view(template_name="api_doc/auth.html", content_type="text/html"), name="api-doc-auth"),
    url(r'^req-resp$', TemplateView.as_view(template_name="api_doc/reqres.html", content_type="text/html"), name="api-doc-req-resp"),
    url(r'^links$', TemplateView.as_view(template_name="api_doc/links.html", content_type="text/html"), name="api-doc-links")


]

