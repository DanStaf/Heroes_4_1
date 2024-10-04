from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from heroes.forms import HeroForm, HeroStatusForm, ParentForm, ParentStatusForm, CellForm, TrainingForm
# Create your views here.


from heroes.models import Hero, HeroStatus, Parent, ParentStatus, Cell, Training
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
        return Response({'object_list': queryset})


class HeroDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'heroes/hero_detail.html'

    def get(self, request, pk):
        hero = get_object_or_404(Hero, pk=pk)
        serializer = HeroSerializer(hero)
        return Response({'serializer': serializer, 'object': hero})

    def post(self, request, pk):
        hero = get_object_or_404(Hero, pk=pk)
        serializer = HeroSerializer(hero, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'object': hero})
        serializer.save()
        return redirect('heroes:hero_list')


#####


class HeroListView(LoginRequiredMixin, ListView):
    model = Hero
    login_url = "/users/login/"


class HeroDetailView(LoginRequiredMixin, DetailView):
    model = Hero
    login_url = "/users/login/"


class HeroCreateView(LoginRequiredMixin, CreateView):
    model = Hero
    form_class = HeroForm
    success_url = reverse_lazy('heroes:hero_list')
    login_url = "/users/login/"


class HeroUpdateView(LoginRequiredMixin, UpdateView):
    model = Hero
    form_class = HeroForm
    success_url = reverse_lazy('heroes:hero_list')
    login_url = "/users/login/"


class HeroDeleteView(LoginRequiredMixin, DeleteView):
    model = Hero
    success_url = reverse_lazy('heroes:hero_list')
    login_url = "/users/login/"


#####


class HeroStatusListView(LoginRequiredMixin, ListView):
    model = HeroStatus
    login_url = "/users/login/"


class HeroStatusDetailView(LoginRequiredMixin, DetailView):
    model = HeroStatus
    login_url = "/users/login/"


class HeroStatusCreateView(LoginRequiredMixin, CreateView):
    model = HeroStatus
    form_class = HeroStatusForm
    success_url = reverse_lazy('heroes:hero_status_list')
    login_url = "/users/login/"


class HeroStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = HeroStatus
    form_class = HeroStatusForm
    success_url = reverse_lazy('heroes:hero_status_list')
    login_url = "/users/login/"


class HeroStatusDeleteView(LoginRequiredMixin, DeleteView):
    model = HeroStatus
    success_url = reverse_lazy('heroes:hero_status_list')
    login_url = "/users/login/"


#####


class ParentListView(LoginRequiredMixin, ListView):
    model = Parent
    login_url = "/users/login/"


class ParentDetailView(LoginRequiredMixin, DetailView):
    model = Parent
    login_url = "/users/login/"


class ParentCreateView(LoginRequiredMixin, CreateView):
    model = Parent
    form_class = ParentForm
    success_url = reverse_lazy('heroes:parent_list')
    login_url = "/users/login/"


class ParentUpdateView(LoginRequiredMixin, UpdateView):
    model = Parent
    form_class = ParentForm
    success_url = reverse_lazy('heroes:parent_list')
    login_url = "/users/login/"


class ParentDeleteView(LoginRequiredMixin, DeleteView):
    model = Parent
    success_url = reverse_lazy('heroes:parent_list')
    login_url = "/users/login/"


#####


class ParentStatusListView(LoginRequiredMixin, ListView):
    model = ParentStatus
    login_url = "/users/login/"


class ParentStatusDetailView(LoginRequiredMixin, DetailView):
    model = ParentStatus
    login_url = "/users/login/"


class ParentStatusCreateView(LoginRequiredMixin, CreateView):
    model = ParentStatus
    form_class = ParentStatusForm
    success_url = reverse_lazy('heroes:parent_status_list')
    login_url = "/users/login/"


class ParentStatusUpdateView(LoginRequiredMixin, UpdateView):
    model = ParentStatus
    form_class = ParentStatusForm
    success_url = reverse_lazy('heroes:parent_status_list')
    login_url = "/users/login/"


class ParentStatusDeleteView(LoginRequiredMixin, DeleteView):
    model = ParentStatus
    success_url = reverse_lazy('heroes:parent_status_list')
    login_url = "/users/login/"


#####


class CellListView(LoginRequiredMixin, ListView):
    model = Cell
    login_url = "/users/login/"


class CellDetailView(LoginRequiredMixin, DetailView):
    model = Cell
    login_url = "/users/login/"


class CellCreateView(LoginRequiredMixin, CreateView):
    model = Cell
    form_class = CellForm
    success_url = reverse_lazy('heroes:cell_list')
    login_url = "/users/login/"


class CellUpdateView(LoginRequiredMixin, UpdateView):
    model = Cell
    form_class = CellForm
    success_url = reverse_lazy('heroes:cell_list')
    login_url = "/users/login/"


class CellDeleteView(LoginRequiredMixin, DeleteView):
    model = Cell
    success_url = reverse_lazy('heroes:cell_list')
    login_url = "/users/login/"


#####


class TrainingListView(LoginRequiredMixin, ListView):
    model = Training
    login_url = "/users/login/"


class TrainingDetailView(LoginRequiredMixin, DetailView):
    model = Training
    login_url = "/users/login/"


class TrainingCreateView(LoginRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    success_url = reverse_lazy('heroes:training_list')
    login_url = "/users/login/"


class TrainingUpdateView(LoginRequiredMixin, UpdateView):
    model = Training
    form_class = TrainingForm
    success_url = reverse_lazy('heroes:training_list')
    login_url = "/users/login/"


class TrainingDeleteView(LoginRequiredMixin, DeleteView):
    model = Training
    success_url = reverse_lazy('heroes:training_list')
    login_url = "/users/login/"


#####
