from decimal import Decimal
from typing import List
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed
from django.db.models.query import QuerySet
from django.contrib import messages
from django.utils.timezone import now, timedelta, make_aware
from datetime import datetime, timedelta
from .models import RecordModel, CategoryModel
from .forms import CategoryNewForm, RecordForm, HistorialCategoryForm,  HistorialRecordForm
from .enums import TypeCategoryEnum
from collections import defaultdict


# Create your views here.
def custom_404_view(request: HttpRequest, exception) -> HttpResponse:
    """Custom Implementation of 404 Page

    Args:
        request (HttpRequest):
        exception (_type_):

    Returns:
        HttpResponse: HTML render response
    """
    return render(request, "404.html", status=404)

# ------------------------ Historial Week ------------------------


def get_week_dates():
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    dates = [start_of_week + timedelta(days=i) for i in range(7)]
    return dates


def get_weekly_data():
    dates = get_week_dates()
    weekly_data = defaultdict(lambda: {'income': 0, 'expense': 0})

    for date in dates:
        start_date = make_aware(datetime.combine(date, datetime.min.time()))
        end_date = make_aware(datetime.combine(date, datetime.max.time()))

        records = RecordModel.objects.filter(
            register_date__range=(start_date, end_date))
        for record in records:
            if str(record.fk_id_category.fk_id_type) == 'INCOME':
                weekly_data[date]['income'] += float(record.mount)
            elif str(record.fk_id_category.fk_id_type) == 'EXPENSE':
                weekly_data[date]['expense'] += float(record.mount)

    return dates, weekly_data

# ------------------------------------------------------------------


def index_view(request: HttpRequest) -> HttpResponse:
    """Home Page

    Args:
        request (HttpRequest):

    Returns:
        HttpResponse: HTML render response
    """
    mount_labels: List[str] = [
        category.note for category in RecordModel.objects.filter(
            fk_id_category__fk_id_type=TypeCategoryEnum.INCOME.value)]

    mounts_data: List[float] = [float(record.mount) for record in RecordModel.objects.filter(
        fk_id_category__fk_id_type=TypeCategoryEnum.INCOME.value)]

    expense_labels: List[str] = [
        category.note for category in RecordModel.objects.filter(
            fk_id_category__fk_id_type=TypeCategoryEnum.EXPENSE.value)]

    expenses_data: List[float] = [float(record.mount) for record in RecordModel.objects.filter(
        fk_id_category__fk_id_type=TypeCategoryEnum.EXPENSE.value)]

    total_income: List[Decimal] = float(sum([record.mount for record in RecordModel.objects.filter(
        fk_id_category__fk_id_type=TypeCategoryEnum.INCOME.value)]))

    total_expense: List[Decimal] = float(sum([record.mount for record in RecordModel.objects.filter(
        fk_id_category__fk_id_type=TypeCategoryEnum.EXPENSE.value)]))

    dates, weekly_data = get_weekly_data()
    labels_week = [date.strftime("%A") for date in dates]
    incomes_week = [weekly_data[date]['income'] for date in dates]
    expenses_week = [weekly_data[date]['expense'] for date in dates]

    return render(request, "index.html", {"labels_general": ["INCOME", "EXPENSE"],
                                          "data_general": [total_income, total_expense],
                                          "labels_mounts": mount_labels, "mounts_data": mounts_data,
                                          "labels_expenses": expense_labels, "expenses_data": expenses_data,
                                          "labels_week": labels_week, "incomes_week": incomes_week,
                                          "expenses_week": expenses_week})


def record_view(request: HttpRequest, id_record: int) -> HttpResponse:
    if request.method == "POST":
        form_record = RecordForm(request.POST)
        if form_record.is_valid():
            form_record.save(commit=True)
            messages.success(request, 'Registro creado exitosamente')
            return redirect('records')

        messages.error(
            request, 'Error al guardar el registro. Por favor, revisa los datos')
        return redirect('records')

    record = get_object_or_404(RecordModel, id=id_record)
    return render(request, "record.html", {"record": record})


def category_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form_category = CategoryNewForm(request.POST)
        if form_category.is_valid():
            form_category.save(commit=True)
            messages.success(
                request, '¡La categoría se ha guardado correctamente!')
            return redirect('categories')

        messages.error(
            request, 'Error al guardar la categoría. Por favor, revisa los datos.')
        return redirect('categories')

    categories: QuerySet = CategoryModel.objects.all()
    return render(request, "category.html", {"categories": categories, "form": CategoryNewForm()})


def records_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form_record = RecordForm(request.POST)
        if form_record.is_valid():
            form_record.save(commit=True)
            messages.success(request, 'Registro creado exitosamente')
            return redirect('records')

        messages.error(
            request, 'Error al guardar el registro. Por favor, revisa los datos')
        return redirect('records')

    records = RecordModel.objects.all()
    return render(request, "record.html", {"records": records, "form": RecordForm()})


def delete_category_view(request: HttpRequest, id_category: int) -> HttpResponse:
    if request.method == "POST":
        category = CategoryModel.objects.filter(id=id_category).first()
        if category is not None:
            category.delete()
            messages.success(
                request, '¡La categoría se ha eliminado exitosamente!')
            return redirect('categories')

        messages.error(
            request, '¡La categoría no existe!')
        return redirect('categories')

    return HttpResponseNotAllowed(['POST'])


def delete_record_view(request: HttpRequest, id_record: int) -> HttpResponse:
    if request.method == "POST":
        record = RecordModel.objects.filter(id=id_record).first()
        if record is not None:
            record.delete()
            messages.success(
                request, '¡El registro se ha eliminado exitosamente!')
            return redirect('records')

        messages.error(
            request, '¡El registro no existe!')
        return redirect('records')

    return HttpResponseNotAllowed(['POST'])


def update_category_view(request: HttpRequest, id_category: int) -> HttpResponse:
    category = CategoryModel.objects.filter(id=id_category).first()
    if category is not None:
        if request.method == "GET":
            if category is not None:
                form_category = CategoryNewForm(instance=category)
                return render(request, "category_update.html", {"form": form_category})

        form_category = CategoryNewForm(request.POST, instance=category)
        if form_category.is_valid():
            form_category.save(commit=True)
            messages.success(
                request, '¡La categoría se ha actualizado correctamente!')
            return redirect('categories')

        messages.error(
            request, 'Ocurrió un error al actualizar la categoría')
        return redirect('categories')

    messages.error(
        request, '¡La categoría no existe!')
    return redirect('categories')


def update_record_view(request: HttpRequest, id_record: int) -> HttpResponse:
    record = RecordModel.objects.filter(id=id_record).first()
    if record is not None:
        if request.method == "GET":
            if record is not None:
                form_record = RecordForm(instance=record)
                return render(request, "record_update.html", {"form": form_record})

        form_record = RecordForm(request.POST, instance=record)
        if form_record.is_valid():
            form_record.save(commit=True)
            messages.success(
                request, '¡El registro se ha actualizado correctamente!')
            return redirect('records')

        messages.error(
            request, 'Ocurrió un error al actualizar el registro')
        return redirect('records')

    messages.error(
        request, '¡El registro no existe!')
    return redirect('records')


def historial_view(request: HttpRequest) -> HttpResponse:
    records = RecordModel.objects.all()

    if request.method == 'POST':
        fk_id_type = request.POST.get('fk_id_type', None)
        fk_id_category = request.POST.get('fk_id_category', None)
        note = request.POST.get('note', None)
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)

        filter_kwargs = {}
        if fk_id_type:
            filter_kwargs['fk_id_category__fk_id_type_id'] = fk_id_type
        if fk_id_category:
            filter_kwargs['fk_id_category_id'] = fk_id_category
        if note:
            filter_kwargs['note__icontains'] = note
        if start_date:
            filter_kwargs['register_date__gte'] = start_date
        if end_date:
            filter_kwargs['register_date__lte'] = end_date

        records = RecordModel.objects.filter(**filter_kwargs)

    return render(request, "historial.html", {"records": records, "form_category": HistorialCategoryForm(), "form_record": HistorialRecordForm()})
