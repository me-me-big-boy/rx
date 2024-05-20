from django.shortcuts import render
from django.views import View

from rx.models import Medicine


class Overview(View):
    def get(self, request):
        medicines = Medicine.objects.all()
        return render(request, "rx/index.html", {"medicines": medicines})
