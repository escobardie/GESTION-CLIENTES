# from django.shortcuts import render, redirect
from .services import ventas_ultimos_7_dias, pagos_por_mes_actual, pagos_recientes, productos_mas_vendidos
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ClienteOnlyMixin


class DashboardEstadisticasView(LoginRequiredMixin, ClienteOnlyMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        ventas_data = ventas_ultimos_7_dias(usuario)
        pagos_total = pagos_por_mes_actual(usuario)
        pagos_list = pagos_recientes(usuario)
        productos_top = productos_mas_vendidos(usuario)

        context.update({
            'ventas_labels': [v['fecha'] for v in ventas_data],
            'ventas_totales': [v['total'] for v in ventas_data],
            'pagos_total_mes': pagos_total,
            'pagos_list': pagos_list,
            'productos_top': productos_top,
            'usuario_login': usuario
        })
        return context

class VentasAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        ventas = ventas_ultimos_7_dias(usuario)
        return JsonResponse({
            'labels': [v['fecha'] for v in ventas],
            'totales': [v['total'] for v in ventas]
        })

class PagosAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        total = pagos_por_mes_actual(usuario)
        return JsonResponse({'total': total})

class PagosRecientesAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        pagos = pagos_recientes(usuario)
        return JsonResponse({'pagos': pagos})

class ProductosMasVendidosAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        productos = productos_mas_vendidos(usuario)
        return JsonResponse({'productos': productos})