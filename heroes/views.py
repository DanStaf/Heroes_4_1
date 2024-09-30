from django.shortcuts import render, redirect

# Create your views here.


from heroes.models import Hero
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from heroes.serializers import HeroSerializer


def main_view(request):

    context = {}
    return render(request, 'heroes/home.html', context=context)


class HeroList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'heroes/hero_list.html'

    def get(self, request):
        queryset = Hero.objects.all()
        return Response({'heroes': queryset})


class HeroDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'heroes/hero_detail.html'

    def get(self, request, pk):
        hero = get_object_or_404(Hero, pk=pk)
        serializer = HeroSerializer(hero)
        return Response({'serializer': serializer, 'hero': hero})

    def post(self, request, pk):
        hero = get_object_or_404(Hero, pk=pk)
        serializer = HeroSerializer(hero, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'hero': hero})
        serializer.save()
        return redirect('heroes:hero_list')
