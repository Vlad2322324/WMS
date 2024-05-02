from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Zone, Cell
from .forms import CellForm, ZoneForm

def cell_list(request):
    cells = Cell.objects.all()
    return render(request, 'cell_list.html', {'cells': cells})

def add_cell(request):
    if request.method == 'POST':
        form = CellForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cell_list')
    else:
        form = CellForm()
    return render(request, 'add_cell.html', {'form': form})

def zone_list(request):
    zones = Zone.objects.all()
    return render(request, 'zone_list.html', {'zones': zones})

def add_zone(request):
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zone_list')
    else:
        form = ZoneForm()
    return render(request, 'add_zone.html', {'form': form})