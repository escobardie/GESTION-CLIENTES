# from django.shortcuts import render, redirect
from .services import ventas_ultimos_7_dias, pagos_por_mes_actual, pagos_recientes, productos_mas_vendidos, cant_cliente_actuales, pago_ultimos_6_meses, pagos_ultimos_7_dias, cant_b_entregados_hoy,visitas_servisclientes_recientes
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
        pagos_semana_data = pagos_ultimos_7_dias(usuario)
        pagos_total_mese_actual = pagos_por_mes_actual(usuario)
        pago_ultimos_6meses = pago_ultimos_6_meses(usuario)
        pagos_list = pagos_recientes(usuario)
        productos_top = productos_mas_vendidos(usuario)
        cant_clientes = cant_cliente_actuales(usuario)
        cant_total_b_entregados_hoy = cant_b_entregados_hoy(usuario)
        visitas_servis_list = visitas_servisclientes_recientes(usuario)

        context.update({
            'ventas_labels': [v['fecha'] for v in ventas_data],
            'ventas_totales': [v['total'] for v in ventas_data],
            'pagos_semana_labels': [v['fecha'] for v in pagos_semana_data],
            'pagos_semana_totales': [v['total'] for v in pagos_semana_data],
            'pago_ultimos_6_meses_labels': [v['mes'] for v in pago_ultimos_6meses],
            'pago_ultimos_6_meses_totales': [v['total'] for v in pago_ultimos_6meses],
            'pagos_total_mes': pagos_total_mese_actual,
            'pagos_list': pagos_list,
            'productos_top': productos_top,
            'usuario_login': usuario,
            'cant_clientes': cant_clientes,
            'cant_b_entregados_hoy': cant_total_b_entregados_hoy,
            'visitas_servis_list': visitas_servis_list
        })
        return context

class PagosSemanaAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        pagos = pagos_ultimos_7_dias(usuario)
        return JsonResponse({
            'labels': [v['fecha'] for v in pagos],
            'totales': [v['total'] for v in pagos]
        })

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

class Pagos6MesesAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        pagos_6_meses = pago_ultimos_6_meses(usuario)
        # return JsonResponse({'pagos_6_meses': pagos_6_meses})
        return JsonResponse({
            'labels': [v['mes'] for v in pagos_6_meses],
            'totales': [v['total'] for v in pagos_6_meses]
        })


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

class CountClientesAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        count_clientes = cant_cliente_actuales(usuario)
        return JsonResponse({'count_clientes': count_clientes})

class CantBEntregadosHoyAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        total = cant_b_entregados_hoy(usuario)
        return JsonResponse({'total': total})

class VisitaServisClteAPI(LoginRequiredMixin, ClienteOnlyMixin, View):
    def get(self, request):
        usuario = request.user
        visitas_servisCltes = visitas_servisclientes_recientes(usuario)
        return JsonResponse({'visitas_servisCltes': visitas_servisCltes})