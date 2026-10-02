# -*- coding: utf-8 -*-
"""Genera las figuras (diagramas) usadas en la documentación técnica."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)

PURPLE = "#7c3aed"
GOLD = "#d4af37"
GREY = "#4b5563"
LIGHT = "#ede9fe"
LIGHT_GOLD = "#fef3c7"
LIGHT_GREY = "#f3f4f6"
BLUE = "#2563eb"
RED = "#dc2626"
GREEN = "#059669"


def _canvas(w=10, h=6):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10 * h / w)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=LIGHT, ec=PURPLE, fs=9, bold=False, tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                linewidth=1.4, edgecolor=ec, facecolor=fc, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            zorder=3, color=tc, fontweight="bold" if bold else "normal", linespacing=1.3)


def band(ax, x, y, w, h, text, fc=LIGHT_GREY, ec=GREY, fs=10):
    """Franja con el rótulo colocado FUERA, por encima del rectángulo."""
    ax.add_patch(Rectangle((x, y), w, h, linewidth=1.2, edgecolor=ec, facecolor=fc, zorder=1))
    ax.text(x + 0.05, y + h + 0.12, text, ha="left", va="bottom", fontsize=fs,
            fontweight="bold", color=ec, zorder=3)


def arrow(ax, p1, p2, text="", color=GREY, style="-|>", rad=0.0, fs=8, dx=0.0, dy=0.12):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14,
                                 linewidth=1.4, color=color, zorder=4,
                                 connectionstyle=f"arc3,rad={rad}"))
    if text:
        mx, my = (p1[0] + p2[0]) / 2 + dx, (p1[1] + p2[1]) / 2 + dy
        ax.text(mx, my, text, fontsize=fs, color=color, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"), zorder=5)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("->", path)


# --------------------------------------------------------------------------- 1
def arquitectura_general():
    fig, ax = _canvas(10, 8.2)
    ax.set_ylim(0, 8.2)
    # --- cliente
    band(ax, 0.2, 6.0, 9.6, 2.4, "Cliente \u2014 Frontend Nuxt 4 (SSR + PWA)")
    box(ax, 0.5, 7.35, 2.1, 0.95, "pages/\nVistas por ruta", fs=8.5)
    box(ax, 2.9, 7.35, 2.1, 0.95, "composables/\ndomain (estado)", fs=8.5)
    box(ax, 5.3, 7.35, 2.1, 0.95, "services/api/\nclientes HTTP", fs=8.5)
    box(ax, 7.7, 7.35, 1.8, 0.95, "services/db/\nDexie offline", fs=8.5, ec=GOLD, fc=LIGHT_GOLD)
    box(ax, 0.5, 6.2, 4.4, 0.8, "Pinia (auth, sync) + Nuxt UI + Tailwind v4", fs=8.5, fc=LIGHT_GREY, ec=GREY)
    box(ax, 5.3, 6.2, 4.2, 0.8, "Service Worker (Workbox): cach\u00e9 y offline", fs=8.5, fc=LIGHT_GREY, ec=GREY)
    arrow(ax, (1.55, 7.35), (1.55, 7.0))
    arrow(ax, (3.95, 7.35), (3.95, 7.0))
    arrow(ax, (6.35, 7.35), (6.35, 7.0))
    arrow(ax, (8.6, 7.35), (8.6, 7.0))

    # --- backend
    band(ax, 0.2, 3.1, 9.6, 2.3, "Backend \u2014 FastAPI (Python) + SQLAlchemy 2.0", fc="#f5f3ff", ec=PURPLE)
    box(ax, 0.5, 4.3, 2.2, 0.95, "routers/\n14 routers REST", fs=8.5)
    box(ax, 3.0, 4.3, 2.2, 0.95, "services/\nnegocio financiero", fs=8.5)
    box(ax, 5.5, 4.3, 2.2, 0.95, "dependencies/\nJWT + roles", fs=8.5)
    box(ax, 8.0, 4.3, 1.5, 0.95, "scheduler\nAPScheduler", fs=8, ec=GOLD, fc=LIGHT_GOLD)
    box(ax, 0.5, 3.3, 4.4, 0.75, "Pydantic v2 (esquemas de entrada/salida)", fs=8.5, fc=LIGHT_GREY, ec=GREY)
    box(ax, 5.5, 3.3, 4.0, 0.75, "Servicios: push, auditor\u00eda, reportes", fs=8.5, fc=LIGHT_GREY, ec=GREY)
    arrow(ax, (1.6, 4.3), (1.6, 4.05))
    arrow(ax, (4.1, 4.3), (4.1, 4.05))
    arrow(ax, (6.6, 4.3), (6.6, 4.05))
    arrow(ax, (8.75, 4.3), (8.75, 4.05))

    # --- datos
    band(ax, 0.2, 0.3, 9.6, 2.2, "Persistencia y servicios externos", fc="#ecfdf5", ec=GREEN)
    box(ax, 0.5, 1.6, 2.6, 0.8, "MySQL (producci\u00f3n)\nSQLite (desarrollo)", fs=8.5, ec=GREEN, fc="#d1fae5")
    box(ax, 3.5, 1.6, 2.6, 0.8, "17 tablas\n(entidades del dominio)", fs=8.5, ec=GREEN, fc="#d1fae5")
    box(ax, 6.5, 1.6, 3.0, 0.8, "Auditor\u00eda + idempotencia\n(tablas de control)", fs=8.5, ec=GREEN, fc="#d1fae5")
    box(ax, 0.5, 0.5, 4.3, 0.8, "IndexedDB (Dexie)\ncach\u00e9 + outbox + auditor\u00eda local", fs=8.5, ec=GOLD, fc=LIGHT_GOLD)
    box(ax, 5.2, 0.5, 4.3, 0.8, "Web Push (VAPID) \u00b7 Exportaci\u00f3n Excel/PDF", fs=8.5, ec=GOLD, fc=LIGHT_GOLD)

    arrow(ax, (5.0, 6.0), (5.0, 5.78), "HTTPS + Bearer", dx=1.5, dy=-0.05)
    arrow(ax, (5.0, 3.1), (5.0, 2.88), "SQLAlchemy", dx=1.3, dy=-0.05)
    save(fig, "fig1_arquitectura.png")


# --------------------------------------------------------------------------- 2
def flujo_credito():
    fig, ax = _canvas(10, 5.0)
    y = 4.15
    steps = [
        (0.15, "Registro\nde cliente"),
        (1.75, "Solicitud\n(Pendiente)"),
        (3.35, "Evaluaci\u00f3n\ny validaci\u00f3n"),
        (4.95, "Aprobaci\u00f3n\no rechazo"),
        (6.55, "Creaci\u00f3n de\npr\u00e9stamo"),
        (8.4, "Desembolso\n(capital \u2212)"),
    ]
    for x, t in steps:
        box(ax, x, y - 0.8, 1.5, 1.1, t, fs=8.5)
    for i in range(len(steps) - 1):
        x1 = steps[i][0] + 1.5
        x2 = steps[i + 1][0]
        arrow(ax, (x1, y - 0.25), (x2, y - 0.25))

    box(ax, 0.2, 2.0, 2.9, 1.1, "Generaci\u00f3n de cuotas\nmensuales autom\u00e1ticas", fs=8.5, ec=BLUE, fc="#dbeafe")
    arrow(ax, (9.3, y - 0.8), (8.6, 3.16), rad=-0.25)
    box(ax, 3.6, 2.0, 3.0, 1.1, "Cobro de cuotas\n(saldo \u2212 capital pagado)", fs=8.5, ec=BLUE, fc="#dbeafe")
    arrow(ax, (3.1, 2.55), (3.6, 2.55))
    box(ax, 7.1, 2.0, 2.6, 1.1, "Mora diaria sobre\ncuotas vencidas", fs=8.5, ec=RED, fc="#fee2e2")
    arrow(ax, (6.6, 2.55), (7.1, 2.55))

    box(ax, 0.2, 0.4, 2.2, 1.1, "Renovaci\u00f3n\n(saldo \u2192 nuevo)", fs=8.5, ec=GOLD, fc=LIGHT_GOLD)
    box(ax, 2.9, 0.4, 2.4, 1.1, "Pr\u00e9stamo perdido\n(capital \u2212 saldo)", fs=8.5, ec=RED, fc="#fee2e2")
    box(ax, 5.8, 0.4, 1.9, 1.1, "Pagado\n(saldo = 0)", fs=8.5, ec=GREEN, fc="#d1fae5")
    box(ax, 8.1, 0.4, 1.6, 1.1, "Reportes de\nganancia/p\u00e9rdida", fs=8.5, fc=LIGHT_GREY, ec=GREY)
    arrow(ax, (2.6, 2.0), (1.3, 1.5), rad=0.1)
    arrow(ax, (5.1, 2.0), (4.1, 1.5), rad=0.1)
    arrow(ax, (7.6, 2.0), (6.75, 1.5), rad=0.1)
    arrow(ax, (7.7, 0.95), (8.1, 0.95))
    save(fig, "fig2_flujo_credito.png")


# --------------------------------------------------------------------------- 3
def flujo_pago():
    fig, ax = _canvas(10, 5.4)
    box(ax, 0.2, 4.3, 2.3, 1.1, "Cuota en estado\n*pendiente*", fs=8.5, fc=LIGHT_GREY, ec=GREY)
    arrow(ax, (2.5, 4.85), (3.2, 4.85), "registro")
    box(ax, 3.2, 4.3, 2.6, 1.1, "Desglose del pago:\ncapital + inter\u00e9s + mora", fs=8.5, ec=PURPLE, fc=LIGHT)
    arrow(ax, (5.8, 4.85), (6.5, 4.85), "valida")
    box(ax, 6.5, 4.3, 3.2, 1.1, "Backend: cuadre \u2264 0,01\ny valor \u2264 cuota + mora", fs=8.5, ec=PURPLE, fc=LIGHT)

    box(ax, 3.2, 2.4, 3.0, 1.1, "Saldo pendiente \u2212= capital\nMovimiento: pago_recibido", fs=8.5, ec=BLUE, fc="#dbeafe")
    arrow(ax, (6.5, 4.5), (5.6, 3.5), rad=0.2)
    box(ax, 6.9, 2.4, 2.8, 1.1, "Cambio de estado\nde la cuota", fs=8.5, ec=BLUE, fc="#dbeafe")
    arrow(ax, (7.9, 4.3), (8.3, 3.5), rad=0.15)

    box(ax, 1.0, 0.5, 2.6, 1.2, "pagado\n(abono \u2265 cuota)", fs=8.5, ec=GREEN, fc="#d1fae5")
    box(ax, 4.2, 0.5, 2.6, 1.2, "parcial\n(0 < abono < cuota)", fs=8.5, ec=GOLD, fc=LIGHT_GOLD)
    box(ax, 7.4, 0.5, 2.4, 1.2, "pr\u00e9stamo pagado\nsi saldo \u2264 0", fs=8.5, ec=GREEN, fc="#d1fae5")
    arrow(ax, (5.0, 2.4), (2.4, 1.7), rad=0.15)
    arrow(ax, (6.0, 2.4), (5.6, 1.7))
    arrow(ax, (8.4, 2.4), (8.6, 1.7))
    arrow(ax, (2.5, 4.3), (1.6, 1.7), rad=-0.25, color=GOLD, text="idempotencia")
    save(fig, "fig3_flujo_pago.png")


# --------------------------------------------------------------------------- 4
def estados():
    fig, ax = _canvas(10, 6.6)
    ytop, ybot = 4.6, 2.6
    box(ax, 0.3, ytop, 2.4, 1.1, "Pr\u00e9stamo ACTIVO", fs=9, bold=True, ec=BLUE, fc="#dbeafe")
    box(ax, 3.6, ytop, 2.4, 1.1, "Pr\u00e9stamo PAGADO", fs=9, bold=True, ec=GREEN, fc="#d1fae5")
    box(ax, 6.9, ytop, 2.6, 1.1, "Pr\u00e9stamo PERDIDO", fs=9, bold=True, ec=RED, fc="#fee2e2")
    box(ax, 3.6, ybot, 2.6, 1.1, "Pr\u00e9stamo RENOVADO\n+ nuevo pr\u00e9stamo activo", fs=9, bold=True, ec=GOLD, fc=LIGHT_GOLD)
    arrow(ax, (2.7, ytop + 0.55), (3.6, ytop + 0.55), "saldo \u2264 0")
    arrow(ax, (1.5, ytop + 1.2), (8.1, ytop + 1.2), rad=-0.2, text="incobrable", dy=0.35)
    arrow(ax, (2.72, ytop + 0.35), (4.3, ybot + 1.18), rad=-0.15, text="renovar", dy=0.4)
    arrow(ax, (0.9, ytop), (0.9, ybot + 1.18), rad=-0.15)
    box(ax, 0.3, ybot, 2.4, 1.1, "Cuota: pendiente\nvencido \u00b7 parcial \u00b7 pagado", fs=8.5, ec=GREY, fc=LIGHT_GREY)
    ax.text(5.0, 1.5, "Estados terminales: PAGADO, PERDIDO y RENOVADO.\nNo admiten pagos, renovaciones ni marcado como perdido.",
            fontsize=8.5, ha="center", va="center", color=GREY, style="italic", linespacing=1.4)
    save(fig, "fig4_estados.png")


# --------------------------------------------------------------------------- 5
def capas_frontend():
    fig, ax = _canvas(10, 5.6)
    capas = [
        ("Vistas (app/pages)", "Rutas, layouts, middlewares, estados de carga y error", 4.6, LIGHT),
        ("Componentes (app/components)", "Kit UI reutilizable + componentes de dominio", 3.7, LIGHT),
        ("Composables de dominio", "Estado reactivo, cach\u00e9 y orquestaci\u00f3n de casos de uso", 2.8, "#dbeafe"),
        ("Servicios de API (app/services/api)", "HTTP tipado: rutas, payloads y tipos de respuesta", 1.9, "#d1fae5"),
        ("Cliente HTTP (useApi)", "Bearer, refresh autom\u00e1tico, normalizaci\u00f3n de errores, blob", 1.0, LIGHT_GOLD),
        ("Backend FastAPI / IndexedDB", "Fuente de verdad y persistencia offline", 0.1, LIGHT_GREY),
    ]
    for title, desc, y, color in capas:
        box(ax, 0.6, y, 8.8, 0.8, "", fc=color, ec=GREY)
        ax.text(0.85, y + 0.55, title, fontsize=9.5, fontweight="bold", va="center", color="#111827")
        ax.text(0.85, y + 0.25, desc, fontsize=8.5, va="center", color="#374151")
    for i in range(len(capas) - 1):
        y1 = capas[i][2]
        y2 = capas[i + 1][2] + 0.8
        arrow(ax, (5.0, y1), (5.0, y2))
    save(fig, "fig5_capas_frontend.png")


# --------------------------------------------------------------------------- 6
def entorno_relaciones():
    fig, ax = _canvas(13, 8.4)
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 8.4)
    ent = {
        "usuarios": (0.2, 5.7, ["id (PK)", "nombre", "email (uq)", "rol", "estado"]),
        "tokens": (0.2, 3.75, ["id (PK)", "usuario_id (FK)", "access_token", "refresh_token", "activo"]),
        "auditoria": (0.2, 1.8, ["id (PK)", "usuario_id (FK)", "tabla_afectada", "tipo_operacion", "valores / ip"]),
        "push_subscriptions": (0.2, 0.3, ["id (PK)", "usuario_id (FK)", "endpoint (uq)"]),
        "capital": (2.9, 6.2, ["id (PK)", "monto_total", "updated_at"]),
        "tipos_prestamo": (2.9, 4.4, ["id (PK)", "nombre", "interes_mensual", "max_cuotas"]),
        "clientes": (2.9, 2.6, ["id (PK)", "nombre", "cedula (uq)", "estado"]),
        "prestamos_renovaciones": (2.9, 0.8, ["id (PK)", "prestamo_anterior_id", "prestamo_nuevo_id", "fecha"]),
        "prestamos": (5.6, 5.5, ["id (PK)", "cliente_id (FK)", "tipo_prestamo_id (FK)", "monto_total", "saldo_pendiente", "estado"]),
        "prestamo_cuotas": (5.6, 3.4, ["id (PK)", "prestamo_id (FK)", "numero_cuota", "valor_cuota", "estado"]),
        "movimientos_capital": (5.6, 1.0, ["id (PK)", "tipo_movimiento", "valor", "fecha", "prestamo_id (FK)"]),
        "pagos": (8.3, 5.5, ["id (PK)", "prestamo_id / cuota_id", "tipo_pago_id (FK)", "valor_pagado", "capital / inter\u00e9s / mora"]),
        "moras": (8.3, 3.4, ["id (PK)", "prestamo_id (FK)", "cuota_id (FK)", "fecha", "valor"]),
        "prestamos_perdidos": (8.3, 1.3, ["id (PK)", "prestamo_id (FK)", "fecha", "valor_perdido"]),
        "tipos_pago": (10.7, 6.2, ["id (PK)", "nombre", "estado"]),
        "configuracion_sistema": (10.7, 4.6, ["clave (PK)", "valor", "tipo_valor"]),
        "idempotency_keys": (10.7, 3.0, ["key (PK)", "response", "status_code"]),
    }
    pos = {}
    for name, (x, y, fields) in ent.items():
        w = 2.4
        h = 0.27 * len(fields) + 0.6
        core = name in ("prestamos", "prestamo_cuotas", "pagos")
        box(ax, x, y, w, h, "", fs=8, fc=LIGHT if core else LIGHT_GREY,
            ec=PURPLE if core else GREY)
        ax.text(x + w / 2, y + h - 0.2, name, ha="center", va="center", fontsize=8.4,
                fontweight="bold", color="#111827", zorder=4)
        ax.plot([x + 0.08, x + w - 0.08], [y + h - 0.34, y + h - 0.34],
                color="#9ca3af", lw=0.8, zorder=3)
        for i, f in enumerate(fields):
            ax.text(x + 0.14, y + h - 0.52 - i * 0.27, f, fontsize=6.8, va="center",
                    color="#374151", zorder=4)
        pos[name] = (x, y, w, h)

    rel = [
        ("usuarios", "tokens"), ("usuarios", "auditoria"), ("usuarios", "push_subscriptions"),
        ("clientes", "prestamos"), ("tipos_prestamo", "prestamos"), ("tipos_pago", "pagos"),
        ("prestamos", "prestamo_cuotas"), ("prestamos", "pagos"), ("prestamo_cuotas", "pagos"),
        ("prestamos", "moras"), ("prestamo_cuotas", "moras"), ("prestamos", "prestamos_renovaciones"),
        ("prestamos", "prestamos_perdidos"), ("prestamos", "movimientos_capital"),
    ]
    for a, b in rel:
        xa, ya, wa, ha = pos[a]
        xb, yb, wb, hb = pos[b]
        if abs(xa - xb) < 0.1:                      # misma columna: vertical
            if ya > yb:
                p1, p2 = (xa + wa / 2, ya), (xb + wb / 2, yb + hb)
            else:
                p1, p2 = (xa + wa / 2, ya + ha), (xb + wb / 2, yb)
        elif ya == yb:                              # misma fila: horizontal
            if xa < xb:
                p1, p2 = (xa + wa, ya + ha / 2), (xb, yb + hb / 2)
            else:
                p1, p2 = (xa, ya + ha / 2), (xb + wb, yb + hb / 2)
        else:                                       # diagonal suave
            if xa < xb:
                p1 = (xa + wa, ya + ha / 2)
                p2 = (xb, yb + hb / 2)
            else:
                p1 = (xa, ya + ha / 2)
                p2 = (xb + wb, yb + hb / 2)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#9ca3af", lw=1.1, zorder=1)
    ax.text(6.6, 0.15, "Todas las relaciones son 1:N salvo prestamos \u2192 prestamos_perdidos (1:1) y "
                       "prestamos \u2192 prestamos_renovaciones (1:N).",
            fontsize=7.5, ha="center", color="#6b7280")
    save(fig, "fig6_entorno_relaciones.png")


# --------------------------------------------------------------------------- 7
def microservicios():
    fig, ax = _canvas(10, 7.6)
    ax.set_ylim(0, 7.6)
    band(ax, 0.2, 5.6, 9.6, 1.3, "Capa de acceso", fc=LIGHT_GREY, ec=GREY)
    box(ax, 0.6, 5.85, 2.4, 0.9, "Web (SPA/SSR)", fs=8.5, fc="white", ec=GREY)
    box(ax, 3.4, 5.85, 2.4, 0.9, "App m\u00f3vil / PWA", fs=8.5, fc="white", ec=GREY)
    box(ax, 6.2, 5.85, 3.2, 0.9, "API p\u00fablica (partners)", fs=8.5, fc="white", ec=GREY)

    band(ax, 0.2, 4.15, 9.6, 0.95, "API Gateway + WAF + balanceador (alta disponibilidad)",
         fc="#f5f3ff", ec=PURPLE)
    box(ax, 3.4, 4.35, 3.2, 0.55, "OAuth2 / OIDC + rate limiting", fs=8.5, ec=PURPLE, fc=LIGHT)

    servicios = ["Identity", "Clientes", "Originaci\u00f3n", "Cartera", "Cobranza", "Pagos",
                 "Notificaciones", "Reportes"]
    ax.text(5.0, 4.05, "Microservicios de dominio (contenedores en orquestador)", fontsize=8.5,
            ha="center", va="center", color=GREY, zorder=6,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none"))
    centers = []
    for i, s in enumerate(servicios):
        x = 0.35 + i * 1.2
        box(ax, x, 2.7, 1.1, 0.85, s, fs=7.5, ec=BLUE, fc="#dbeafe")
        centers.append(x + 0.55)

    band(ax, 0.2, 0.15, 9.6, 1.5, "Datos y plataforma", fc="#ecfdf5", ec=GREEN)
    box(ax, 0.5, 0.4, 2.0, 1.0, "PostgreSQL\n(cluster con r\u00e9plica)", fs=8, ec=GREEN, fc="#d1fae5")
    box(ax, 2.8, 0.4, 2.0, 1.0, "Redis\n(cache + colas)", fs=8, ec=GREEN, fc="#d1fae5")
    box(ax, 5.1, 0.4, 2.0, 1.0, "Object storage\n(archivos)", fs=8, ec=GREEN, fc="#d1fae5")
    box(ax, 7.4, 0.4, 2.1, 1.0, "Observabilidad\n(logs, m\u00e9tricas)", fs=8, ec=GREEN, fc="#d1fae5")

    arrow(ax, (5.0, 5.85), (5.0, 5.15))
    arrow(ax, (5.0, 4.35), (5.0, 4.05))
    ax.plot([centers[0], centers[-1]], [4.05, 4.05], color="#9ca3af", lw=1.2, zorder=4)
    for c in centers:
        arrow(ax, (c, 4.05), (c, 3.57), color="#9ca3af")
    for c in (centers[2], centers[4], centers[6]):
        arrow(ax, (c, 2.7), (c, 1.67), color="#9ca3af")
    save(fig, "fig7_microservicios.png")


# --------------------------------------------------------------------------- 8
def mapa_navegacion():
    fig, ax = _canvas(10, 6.4)
    ax.set_ylim(0, 6.4)

    band(ax, 0.2, 4.4, 2.6, 1.6, "Acceso", fc=LIGHT_GREY, ec=GREY)
    box(ax, 0.4, 5.3, 2.2, 0.6, "/login", fs=8.5, fc="white", ec=GREY)
    box(ax, 0.4, 4.55, 2.2, 0.6, "/perfil", fs=8.5, fc="white", ec=GREY)

    band(ax, 3.3, 4.1, 6.5, 1.9, "Operaci\u00f3n diaria", fc="#f5f3ff", ec=PURPLE)
    box(ax, 3.6, 5.15, 2.9, 0.7, "/  Tablero e indicadores", fs=8.5, ec=PURPLE, fc=LIGHT)
    box(ax, 6.7, 5.15, 2.9, 0.7, "/clientes  \u00b7  alta y b\u00fasqueda", fs=8.5, ec=PURPLE, fc=LIGHT)
    box(ax, 3.6, 4.25, 2.9, 0.7, "/prestamos  \u00b7  creaci\u00f3n y detalle", fs=8.5, ec=PURPLE, fc=LIGHT)
    box(ax, 6.7, 4.25, 2.9, 0.7, "/pagos  \u00b7  cobro por pr\u00e9stamo", fs=8.5, ec=PURPLE, fc=LIGHT)

    band(ax, 0.2, 1.6, 9.6, 1.9, "Gesti\u00f3n, cobranza y control", fc="#ecfdf5", ec=GREEN)
    for x, t in ((0.4, "/cobranza"), (2.7, "/moras"), (5.0, "/capital"), (7.3, "/reportes")):
        box(ax, x, 2.55, 2.2, 0.7, t, fs=8.5, ec=GREEN, fc="#d1fae5")
    for x, t in ((0.4, "/usuarios"), (3.6, "/tipos-prestamo"), (6.8, "/tipos-pago")):
        box(ax, x, 1.7, 3.0, 0.7, t, fs=8.5, ec=GREY, fc="white")

    arrow(ax, (2.8, 5.05), (3.3, 5.05))
    arrow(ax, (6.5, 4.1), (6.5, 3.5))
    save(fig, "fig8_mapa_navegacion.png")


# --------------------------------------------------------------------------- 9
def flujo_tareas():
    fig, ax = _canvas(10, 3.4)
    ax.set_ylim(0, 3.4)
    band(ax, 0.2, 0.5, 9.6, 2.0, "La jornada con LoanSoft, en seis momentos",
         fc=LIGHT_GREY, ec=GREY, fs=10)
    pasos = [
        "1. Preparar\nusuarios y cat\u00e1logos",
        "2. Registrar\na los clientes",
        "3. Crear\nel pr\u00e9stamo",
        "4. Cobrar\nlas cuotas",
        "5. Dar seguimiento\n(cobranza y avisos)",
        "6. Cerrar con\nel tablero y reportes",
    ]
    xs = []
    for i, t in enumerate(pasos):
        x = 0.4 + i * 1.58
        box(ax, x, 1.5, 1.4, 1.0, t, fs=8, ec=PURPLE, fc=LIGHT)
        xs.append(x)
    for i in range(5):
        arrow(ax, (xs[i] + 1.46, 2.0), (xs[i + 1] - 0.06, 2.0))
    ax.text(5.0, 0.8, "Cada momento deja listo el dato que usa el siguiente.",
            ha="center", fontsize=8.5, color=GREY)
    save(fig, "fig9_flujo_tareas.png")


if __name__ == "__main__":
    arquitectura_general()
    flujo_credito()
    flujo_pago()
    estados()
    capas_frontend()
    entorno_relaciones()
    microservicios()
    mapa_navegacion()
    flujo_tareas()
    print("figuras listas")
