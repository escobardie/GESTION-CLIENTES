# analytics/services.py
from . import models
from apps.ventas.models import Venta, VentaProducto
from apps.pagos.models import Pagos
from apps.cliente.models import Cliente
from django.utils.timezone import now
from datetime import timedelta, datetime
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth
from decimal import Decimal



def ventas_ultimos_7_dias(usuario):
    # .annotate(fecha_solo=TruncDate('fecha_venta'))
    # Agrega un nuevo campo fecha_solo a cada objeto, conteniendo solo la fecha (sin la hora) de fecha_venta.

    # .filter(usuario=usuario, fecha_solo=dia)
    # Filtra las ventas hechas por ese usuario en esa fecha específica (dia).

    # .aggregate(suma=Sum('total_venta'))['suma'] or 0
    # Suma el total de ventas para ese día. Si no hay resultados, devuelve 0.

    # .append(...)
    # Agrega esa información (fecha y total) a la lista datos.
    print("Entro una services.py ventas_ultimos_7_dias")
    hoy = now().date()
    datos = []
    for i in range(6, -1, -1):  # Últimos 7 días
        dia = hoy - timedelta(days=i)
        total = Venta.objects \
        .annotate(fecha_solo=TruncDate('fecha_venta')) \
        .filter(usuario=usuario,fecha_solo=dia) \
        .aggregate(suma=Sum('total_venta'))['suma'] or 0
        datos.append({'fecha': dia.strftime('%d/%m'), 'total': float(total)})
    return datos


def pagos_por_mes_actual(usuario):
    print("Entro una services.py pagos_por_mes_actual")
    hoy = now()
    pagos = Pagos.objects.filter(usuario=usuario, fecha_pago__year=hoy.year, fecha_pago__month=hoy.month)
    # total = pagos.aggregate(suma=Sum('monto'))['suma'] or 0 ## original
    # return float(total) ## original
    total = pagos.aggregate(suma=Sum('monto'))['suma'] or Decimal('0.00')
    return total

def pago_ultimos_6_meses(usuario):
    """
    Devuelve el total de pagos por mes en los últimos 6 meses para el usuario.
    """
    hoy = now().date()
    datos = []

    for i in range(5, -1, -1):  # últimos 6 meses
        primer_dia_mes = (hoy.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        siguiente_mes = (primer_dia_mes.replace(day=28) + timedelta(days=4)).replace(day=1)

        total = (
            Pagos.objects
            .filter(usuario=usuario, fecha_pago__gte=primer_dia_mes, fecha_pago__lt=siguiente_mes)
            .aggregate(suma=Sum('monto'))['suma'] or 0
        )

        datos.append({
            'mes': primer_dia_mes.strftime('%b %Y'),  # ejemplo: 'May 2025'
            'total': float(total)
        })

    return datos

def pagos_recientes(usuario, limit=10): ## TODO: OJO POR ACA
    # .filter(usuario=usuario)
    # Filtra los pagos para que solo devuelva los que pertenecen al usuario especificado.

    # .select_related('cliente')
    # Optimiza la consulta trayendo también los datos del cliente asociado, en una sola consulta SQL.

    # .order_by('-fecha_pago')
    # Ordena los pagos desde el más reciente al más antiguo.

    # [:limit]
    # Limita el número de pagos devueltos a limit (por ejemplo, 10).

    # pagos = Pagos.objects.select_related('cliente').order_by('-fecha_pago')[:limit]
    # pagos = Pagos.objects.filter(usuario=usuario).order_by('-fecha_pago')[:limit]
    pagos = Pagos.objects.filter(usuario=usuario).select_related('cliente').order_by('-fecha_pago')[:limit]
    return [{
        'usuario' : str(p.usuario), ## TODO: esto es solo de prueba, borrar luego
        'cliente': str(p.cliente) if p.cliente else 'Anónimo',
        'monto': float(p.monto),
        'fecha': p.fecha_pago.strftime('%d/%m/%Y %H:%M')
    } for p in pagos]


def productos_mas_vendidos(usuario, limit=5):
    # .filter(usuario=usuario)
    # Filtra los VentaProducto que pertenecen al usuario dado.

    # .values('producto__nombre_producto')
    # Agrupa por nombre del producto (relación con modelo Producto).

    # .annotate(cantidad=Sum('cantidad'))
    # Suma la cantidad vendida de cada producto.

    # .order_by('-cantidad')
    # Ordena los productos más vendidos primero.

    # [:limit]
    # Limita los resultados a los limit productos más vendidos.


    # productos = VentaProducto.objects.values('producto__nombre_producto') \
    #     .annotate(cantidad=Sum('cantidad')) \
    #     .order_by('-cantidad')[:limit]
    productos = VentaProducto.objects.filter(usuario=usuario) \
    .values('producto__nombre_producto') \
    .annotate(cantidad=Sum('cantidad')) \
    .order_by('-cantidad')[:limit]

    return [{'nombre': p['producto__nombre_producto'], 'cantidad': p['cantidad']} for p in productos]


def cant_cliente_actuales(usuario):
    cantidad_clientes = Cliente.objects.filter(usuario=usuario).count()
    return cantidad_clientes