from django.shortcuts import render
from dal import autocomplete

from home.models import SchoolCategory


def home(request):
    return render(request, "home/home.html")


class SchoolCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return SchoolCategory.objects.none()

        qs = SchoolCategory.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
