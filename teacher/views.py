import re
from django.core.exceptions import ValidationError
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
        fields = ['name', 'birth', 'subjects', 'postcode',
                  'addr1', 'addr2', 'email', 'phone', 'portrait', 'document']

        widgets = {
            'subjects': autocomplete.ModelSelect2Multiple(url='subject-autocomplete')
        }

    phone_ex = re.compile(r"^(02|01.|[0-9]{3})[-.\s]*([0-9]+)[-.\*\s]*([0-9]{4})")
    birth_ex = re.compile(r"^(?:19|10)?([0-9]{2})[\.년\s\-/]*([0-9]{1,2})[\.월\s\-/]*([0-9]{1,2})[일\s\.]*$")

    def clean_birth(self):
        matchs = self.birth_ex.match(self.cleaned_data['birth'])

        if not matchs:
            raise ValidationError('"%s"는 잘못된 형식 입니다.' % self.cleaned_data['birth'])

        return "19%02d/%02d/%02d" % tuple(int(n) for n in matchs.groups())

    def clean_phone(self):
        matchs = self.phone_ex.match(self.cleaned_data['phone'])

        if not matchs:
            raise ValidationError('"%s"는 잘못된 형식 입니다.' % self.cleaned_data['phone'])

        return "-".join(matchs.groups())


def regist(request):

    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save()
            return render(request, "teacher/result.html", {"teacher": teacher})
    else:
        form = TeacherForm()

    return render(request, "teacher/regist.html", {"form": form})
