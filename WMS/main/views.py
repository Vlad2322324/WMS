from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CellForm, ZoneForm
from django.urls import reverse


def create_new_pallet_view(request):
    if request.method == 'POST':
        pallet_id = request.POST.get('pallet_id')

        try:
            # Создаем новую паллету
            create_new_pallet(pallet_id)

            # Перенаправляем пользователя на страницу прикрепления паллеты к ячейке
            return redirect('attach_pallet_to_cell')
        except Exception as e:
            message = f"Произошла ошибка при создании паллеты: {e}"
    else:
        message = None

    return render(request, 'create_new_pallet.html', {'message': message})


def attach_pallet_to_cell_view(request):
    if request.method == 'POST':
        pallet_id = request.POST.get('pallet_id')
        cell_id = request.POST.get('cell_id')

        try:
            pallet = Pallet.objects.get(pallet_id=pallet_id)
            cell = Cell.objects.get(cell_id=cell_id)
            message = attach_pallet_to_cell(pallet, cell)
        except Pallet.DoesNotExist:
            message = "Такой паллеты не существует."
        except Cell.DoesNotExist:
            message = "Такой ячейки не существует."

        return render(request, 'attach_pallet_to_cell.html', {'message': message})

    return render(request, 'attach_pallet_to_cell.html')


def find_free_cell(needZone):
    cells_in_zone = Cell.objects.filter(zone=needZone)

    for cell in cells_in_zone:

        if not cell.pallet:
            return cell.cell_id

    return None


def create_new_pallet(pallet_id):
    try:
        # Проверяем, существует ли паллета с указанным ID
        if Pallet.objects.filter(pallet_id=pallet_id).exists():
            return f"Паллета с ID {pallet_id} уже существует."

        # Создаем новую паллету
        new_pallet = Pallet.objects.create(pallet_id=pallet_id)
        return f"Новая паллета с ID {pallet_id} успешно создана."
    except Exception as e:
        return f"Произошла ошибка при создании паллеты: {e}"


def attach_pallet_to_cell(pallet, cell):  # добавить проверку!!!
    try:
        if cell.pallet is not None:
            return "Выбранная ячейка уже занята другой паллетой."

        cell.pallet = pallet
        cell.save()
        return f"Паллета {pallet.pallet_id} успешно прикреплена к ячейке {cell.cell_id}."
    except Exception as e:
        return f"Произошла ошибка: {e}"


def attach_pallet_to_cell_view(request):
    if request.method == 'POST':
        pallet_id = request.POST.get('pallet_id')
        cell_id = request.POST.get('cell_id')

        try:
            pallet = Pallet.objects.get(pallet_id=pallet_id)
            cell = Cell.objects.get(cell_id=cell_id)
            message = attach_pallet_to_cell(pallet, cell)
        except Pallet.DoesNotExist:
            message = "Такой паллеты не существует."
        except Cell.DoesNotExist:
            message = "Такой ячейки не существует."

        return render(request, 'attach_pallet_to_cell.html', {'message': message})

    return render(request, 'attach_pallet_to_cell.html')


def index(request):
    return render(request, 'index.html')


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


def purchase_order_list(request):
    purchase_orders = PurchaseOrder.objects.all()
    if request.method == 'POST':
        delivery_id = request.POST.get('delivery_id')
        purchase_orders_with_selected_delivery = PurchaseOrder.objects.filter(delivery_id=delivery_id)
        if purchase_orders_with_selected_delivery.exists():
            print(f"Содержимое таблицы с выбранным delivery_id {delivery_id}:")
            for order in purchase_orders_with_selected_delivery:
                print("ID поставки:", order.delivery_id)
                print("ID продукта:", order.product_id)
                print("Количество:", order.quantity)
                print("Сумма:", order.amount)
                print("ID поставщика:", order.supplier_id)
                print("")

            # В данном месте вы можете добавить код для создания объекта AcceptancePlan
            # на основе выбранных поставок purchase_orders_with_selected_delivery

            # После этого можно выполнить редирект на страницу погрузки в зону приемки
            return redirect(reverse('load_to_acceptance_zone'))

    # Дополнительный код (например, вывод уникальных идентификаторов поставок) оставлен без изменений

    unique_delivery_ids = PurchaseOrder.objects.values_list('delivery_id', flat=True).distinct()
    return render(request, 'purchase_order_list.html',
                  {'unique_delivery_ids': unique_delivery_ids, 'purchase_orders': purchase_orders})


def attach_product_to_pallet(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        delivery_id = request.POST.get('delivery_id')
        pallet_id = request.POST.get('pallet_id')
        quantity = request.POST.get('quantity')

    purchase_orders = PurchaseOrder.objects.filter(product_id=product_id, delivery_id=delivery_id)
    pallet = Pallet.objects.get(pallet_id=pallet_id)
    pallet_create = ProductOnPallet.objects.create(pallet_id=pallet,
                                                   product_id=ProductDirectory.objects.get(product_id=product_id),
                                                   quantity=quantity)

    return render(request, 'attach_product_to_pallet.html', {})
