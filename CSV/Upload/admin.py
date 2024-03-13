from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import admin, messages
from django.shortcuts import render
from . models import Alums
from django import forms


class CSVImportForm(forms.Form):
    csv_upload = forms.FileField()

class AlumsAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload_csv/', self.upload_csv)]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                Alums.objects.update_or_create(
                    name = fields[0],
                    balance = fields[1]
                )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CSVImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


admin.site.register(Alums, AlumsAdmin)