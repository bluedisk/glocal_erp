from django.shortcuts import render
from django.forms import ModelForm
from teacher.models import Teacher, Subject, SubjectCategory
from dal import autocomplete


class SubjectCategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = SubjectCategory.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SubjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Subject.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'birth', 'subject1', 'subject2', 'postcode',
                  'addr1', 'addr2', 'email', 'phone', 'portrait', 'document']


def regist(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            return render(request, "teacher/result.html", {"teacher": teacher})
    else:
        form = TeacherForm()

    return render(request, "teacher/regist.html", {"form": form})
