from django.views.generic import DetailView

from blog.models import Blog


class BlogDetailView(DetailView):
    model = Blog

