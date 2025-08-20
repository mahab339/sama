import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.html import format_html
from .models import Client, Calculation, ClientType


def export_to_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]
    
    # Add related fields
    if modeladmin.model == Calculation:
        field_names.extend(['client_id', 'client_type'])
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    writer = csv.writer(response)
    writer.writerow(field_names)
    
    for obj in queryset:
        row = []
        for field in field_names:
            if hasattr(obj, field):
                value = getattr(obj, field)
                if field == 'client_type' and hasattr(obj, 'client'):
                    value = obj.client.get_client_type_display()
                row.append(str(value) if value is not None else '')
            elif field == 'client_id' and hasattr(obj, 'client'):
                row.append(str(obj.client.id))
            elif field == 'client_type' and hasattr(obj, 'client'):
                row.append(obj.client.get_client_type_display())
            else:
                row.append('')
        writer.writerow(row)
    
    return response
export_to_csv.short_description = "Export selected items to CSV"


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_type_display', 'created_at', 'last_seen', 'calculations_count', 'view_calculations')
    list_filter = ('client_type', 'created_at', 'last_seen')
    search_fields = ('id', 'client_type')
    readonly_fields = ('id', 'created_at', 'last_seen')
    date_hierarchy = 'created_at'
    actions = [export_to_csv]
    
    def client_type_display(self, obj):
        return obj.get_client_type_display()
    client_type_display.short_description = 'Client Type'
    
    def calculations_count(self, obj):
        return obj.calculations.count()
    calculations_count.short_description = 'Total Calculations'
    
    def view_calculations(self, obj):
        url = f"{reverse('admin:calculator_calculation_changelist')}?client__id__exact={obj.id}"
        return format_html('<a href="{}">View Calculations</a>', url)
    view_calculations.short_description = 'Calculations'


class HasErrorFilter(admin.SimpleListFilter):
    title = 'error status'
    parameter_name = 'has_error'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Has Error'),
            ('no', 'No Error'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(error__isnull=True).exclude(error__exact='')
        if self.value() == 'no':
            return queryset.filter(error__isnull=True) | queryset.filter(error__exact='')
        return queryset


class CalculationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_info', 'expression_preview', 'result', 'error_preview', 'created_at')
    list_filter = (HasErrorFilter, 'client__client_type', 'created_at')
    search_fields = ('expression', 'result', 'client__id')
    readonly_fields = ('id', 'created_at', 'client_info', 'expression_full')
    date_hierarchy = 'created_at'
    actions = [export_to_csv]
    
    def client_info(self, obj):
        return f"{obj.client.id} ({obj.client.get_client_type_display()})"
    client_info.short_description = 'Client (Type)'
    
    def expression_preview(self, obj):
        return obj.expression
    expression_preview.short_description = 'Expression'
    
    def expression_full(self, obj):
        return format_html('<pre>{}</pre>', obj.expression)
    expression_full.short_description = 'Full Expression'
    
    def error_preview(self, obj):
        return obj.error or ''
    error_preview.short_description = 'Error'


admin.site.register(Client, ClientAdmin)
admin.site.register(Calculation, CalculationAdmin)
