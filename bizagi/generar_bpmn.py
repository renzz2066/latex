"""Genera los diagramas BPMN 2.0 de la tesis.

Para cada diagrama produce:
  - bizagi/<nombre>.bpmn        -> se importa en Bizagi Modeler (BPMN 2.0 con diagrama)
  - imagenes/<nombre>.pdf/.png  -> versión dibujada para la tesis (misma disposición)

Ejecutar:  python bizagi/generar_bpmn.py   (desde la carpeta latex)
"""
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle

BASE = Path(__file__).resolve().parent
IMG = BASE.parent / "imagenes"

COL_W, ROW_H = 150, 120          # ancho de columna y alto de fila
TASK_W, TASK_H = 122, 80
EV, GW = 36, 50                  # diámetro de evento y lado de compuerta
POOL_STRIP, LANE_STRIP, X0 = 40, 34, 40


# --------------------------------------------------------------------------- definición
DIAGRAMAS = {
    "bpmn_actual_gestion": {
        "pool": "Gestión tributaria predial con Sispredios (situación actual)",
        "lanes": [("Contribuyente", 1), ("Caja", 1), ("Rentas", 1), ("Ejecutoría coactiva", 1)],
        "nodes": [
            ("ini", "start", "Presenta declaración jurada", 0, 0, 0),
            ("t1", "task", "Registrar predio, pisos y propietarios en Sispredios", 2, 0, 1),
            ("t2", "task", "Emitir las deudas anuales en la cuenta corriente", 2, 0, 2),
            ("g1", "xor", "¿Paga antes del vencimiento?", 0, 0, 3),
            ("t3", "task", "Pagar en caja o en el banco", 0, 0, 4),
            ("t4", "task", "Registrar el pago o importar el archivo del banco", 1, 0, 5),
            ("t5", "task", "Cuadrar la caja al cierre del día", 1, 0, 6),
            ("f1", "end", "Deuda cancelada", 1, 0, 7),
            ("t6", "task", "Armar listados a mano en hojas de cálculo", 2, 0, 4),
            ("t7", "task", "Enviar cartas de aviso a todos los deudores", 2, 0, 5),
            ("t8", "task", "Emitir valores (OP o RD)", 2, 0, 6),
            ("g2", "xor", "¿Firma convenio?", 2, 0, 7),
            ("t9", "task", "Registrar el fraccionamiento", 2, 0, 8),
            ("f2", "end", "Deuda fraccionada", 2, 0, 9),
            ("t10", "task", "Abrir expediente de cobranza coactiva", 3, 0, 8),
            ("f3", "end", "Cobranza coactiva", 3, 0, 9),
        ],
        "flows": [("ini", "t1", ""), ("t1", "t2", ""), ("t2", "g1", ""), ("g1", "t3", "Sí"),
                  ("t3", "t4", ""), ("t4", "t5", ""), ("t5", "f1", ""), ("g1", "t6", "No"),
                  ("t6", "t7", ""), ("t7", "t8", ""), ("t8", "g2", ""), ("g2", "t9", "Sí"),
                  ("t9", "f2", ""), ("g2", "t10", "No"), ("t10", "f3", "")],
    },
    "bpmn_actual_soporte": {
        "pool": "Atención de soporte técnico de Sispredios (situación actual)",
        "lanes": [("Personal municipal", 1), ("Desarrollador (Consultoría Informática)", 2)],
        "nodes": [
            ("ini", "start", "Ocurre una incidencia", 0, 0, 0),
            ("t1", "task", "Reportar la incidencia o el pedido de cambio", 0, 0, 1),
            ("t2", "task", "Analizar la incidencia (único desarrollador)", 1, 0, 2),
            ("g1", "xor", "¿Dónde está el error?", 1, 0, 3),
            ("t3", "task", "Modificar el código en Visual FoxPro", 1, 0, 4),
            ("t4", "task", "Recompilar el ejecutable completo (27–28 MB)", 1, 0, 5),
            ("t5", "task", "Copiar el ejecutable en cada equipo", 1, 0, 6),
            ("t6", "task", "Adaptar la corrección en la copia de cada municipalidad", 1, 0, 7),
            ("t7", "task", "Corregir los datos con un programa escrito para el caso", 1, 1, 4),
            ("t8", "task", "Reanudar el trabajo detenido", 0, 0, 8),
            ("f1", "end", "Incidencia atendida", 0, 0, 9),
        ],
        "flows": [("ini", "t1", ""), ("t1", "t2", ""), ("t2", "g1", ""), ("g1", "t3", "Código"),
                  ("t3", "t4", ""), ("t4", "t5", ""), ("t5", "t6", ""), ("t6", "t8", ""),
                  ("g1", "t7", "Datos"), ("t7", "t8", ""), ("t8", "f1", "")],
    },
    "bpmn_mejorado_gestion": {
        "pool": "Gestión tributaria predial con el sistema web (situación mejorada)",
        "lanes": [("Contribuyente", 1), ("Caja", 1), ("Rentas", 1), ("Ejecutoría coactiva", 1),
                  ("Sistema web y modelo de ML", 1)],
        "nodes": [
            ("ini", "start", "Presenta declaración jurada", 0, 0, 0),
            ("t1", "task", "Registrar el predio en el sistema web", 2, 0, 1),
            ("t2", "service", "Calcular y emitir las deudas automáticamente", 4, 0, 2),
            ("g1", "xor", "¿Paga antes del vencimiento?", 0, 0, 3),
            ("t3", "task", "Pagar en caja", 0, 0, 4),
            ("t4", "task", "Cobrar y emitir recibo correlativo", 1, 0, 5),
            ("t5", "task", "Cerrar la caja del día por cajero", 1, 0, 6),
            ("f1", "end", "Deuda cancelada", 1, 0, 7),
            ("t6", "service", "Modelo ML: grupo, deuda esperada y acción sugerida", 4, 0, 4, True),
            ("t7", "task", "Priorizar la cobranza con la lista (tramos A, B y C)", 2, 0, 5, True),
            ("t8", "task", "Enviar recordatorios y valores a los priorizados", 2, 0, 6),
            ("g2", "xor", "¿Firma convenio?", 2, 0, 7),
            ("t9", "task", "Registrar el fraccionamiento", 2, 0, 8),
            ("f2", "end", "Deuda fraccionada", 2, 0, 9),
            ("t10", "task", "Recibir el valor transferido y asignarlo a un auxiliar", 3, 0, 8),
            ("f3", "end", "Cobranza coactiva", 3, 0, 9),
        ],
        "flows": [("ini", "t1", ""), ("t1", "t2", ""), ("t2", "g1", ""), ("g1", "t3", "Sí"),
                  ("t3", "t4", ""), ("t4", "t5", ""), ("t5", "f1", ""), ("g1", "t6", "No"),
                  ("t6", "t7", ""), ("t7", "t8", ""), ("t8", "g2", ""), ("g2", "t9", "Sí"),
                  ("t9", "f2", ""), ("g2", "t10", "No"), ("t10", "f3", "")],
    },
    "bpmn_mejorado_soporte": {
        "pool": "Atención de soporte técnico con el sistema web (situación mejorada)",
        "lanes": [("Personal municipal", 1), ("Desarrolladores", 1),
                  ("Sistema web", 1)],
        "nodes": [
            ("ini", "start", "Ocurre una incidencia", 0, 0, 0),
            ("t1", "task", "Reportar la incidencia o el pedido de cambio", 0, 0, 1),
            ("t2", "task", "Analizar la incidencia", 1, 0, 2),
            ("t3", "task", "Corregir el código en la única base de código", 1, 0, 3, True),
            ("t4", "task", "Revisar e integrar el cambio (pull request)", 1, 0, 4, True),
            ("t5", "service", "Desplegar la nueva versión para todas las municipalidades", 2, 0, 5, True),
            ("t6", "task", "Recargar el navegador y continuar", 0, 0, 6),
            ("f1", "end", "Incidencia atendida", 0, 0, 7),
        ],
        "flows": [("ini", "t1", ""), ("t1", "t2", ""), ("t2", "t3", ""), ("t3", "t4", ""),
                  ("t4", "t5", ""), ("t5", "t6", ""), ("t6", "f1", "")],
    },
}


# --------------------------------------------------------------------------- disposición
def disponer(d):
    lanes, y = [], 0
    for nombre, filas in d["lanes"]:
        lanes.append({"name": nombre, "y": y, "h": filas * ROW_H})
        y += filas * ROW_H
    alto = y
    ncol = max(n[5] for n in d["nodes"]) + 1
    ancho = POOL_STRIP + LANE_STRIP + X0 + ncol * COL_W
    nodos = {}
    for n in d["nodes"]:
        nid, tipo, nombre, lane, fila, col = n[:6]
        nuevo = len(n) > 6 and n[6]
        cx = POOL_STRIP + LANE_STRIP + X0 + col * COL_W + COL_W / 2 - 40
        cy = lanes[lane]["y"] + fila * ROW_H + ROW_H / 2
        w, h = {"task": (TASK_W, TASK_H), "service": (TASK_W, TASK_H),
                "start": (EV, EV), "end": (EV, EV), "xor": (GW, GW)}[tipo]
        nodos[nid] = dict(id=nid, tipo=tipo, nombre=nombre, lane=lane, col=col, fila=fila,
                          cx=cx, cy=cy, w=w, h=h, nuevo=nuevo)
    return lanes, nodos, ancho - 40, alto


def ruta(a, b):
    """Puntos de la flecha de a hacia b (ortogonal)."""
    ax, ay, bx, by = a["cx"], a["cy"], b["cx"], b["cy"]
    if abs(ay - by) < 1:                                   # misma fila
        return [(ax + a["w"] / 2, ay), (bx - b["w"] / 2, by)]
    abajo = by > ay
    if a["tipo"] == "xor":                                 # compuerta: sale por arriba/abajo
        y0 = ay + (a["h"] / 2 if abajo else -a["h"] / 2)
        return [(ax, y0), (ax, by), (bx - b["w"] / 2, by)]
    if abs(ax - bx) < 1:                                   # misma columna
        return [(ax, ay + (a["h"] / 2 if abajo else -a["h"] / 2)),
                (bx, by - (b["h"] / 2 if abajo else -b["h"] / 2))]
    xm = bx - b["w"] / 2 - 14                              # codo justo antes del destino
    return [(ax + a["w"] / 2, ay), (xm, ay), (xm, by), (bx - b["w"] / 2, by)]


# --------------------------------------------------------------------------- BPMN XML
def xml_bpmn(nombre, d, lanes, nodos, ancho, alto):
    tag = {"task": "task", "service": "serviceTask", "start": "startEvent", "end": "endEvent",
           "xor": "exclusiveGateway"}
    flows = [(f"flujo_{i}", s, t, l) for i, (s, t, l) in enumerate(d["flows"], 1)]
    inc = {n: [] for n in nodos}
    out = {n: [] for n in nodos}
    for fid, s, t, _ in flows:
        out[s].append(fid)
        inc[t].append(fid)
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL" '
         'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
         'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
         'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
         'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
         f'id="def_{nombre}" targetNamespace="http://tesis.sanbartolo/bpmn" '
         'exporter="generar_bpmn.py" exporterVersion="1.0">',
         f'  <collaboration id="colab_{nombre}">',
         f'    <participant id="pool_{nombre}" name="{escape(d["pool"])}" processRef="proc_{nombre}"/>',
         '  </collaboration>',
         f'  <process id="proc_{nombre}" name="{escape(d["pool"])}" isExecutable="false">',
         '    <laneSet id="lanes">']
    for i, ln in enumerate(lanes):
        L.append(f'      <lane id="lane_{i}" name="{escape(ln["name"])}">')
        for n in nodos.values():
            if n["lane"] == i:
                L.append(f'        <flowNodeRef>{n["id"]}</flowNodeRef>')
        L.append('      </lane>')
    L.append('    </laneSet>')
    for n in nodos.values():
        L.append(f'    <{tag[n["tipo"]]} id="{n["id"]}" name="{escape(n["nombre"])}">')
        L += [f'      <incoming>{f}</incoming>' for f in inc[n["id"]]]
        L += [f'      <outgoing>{f}</outgoing>' for f in out[n["id"]]]
        L.append(f'    </{tag[n["tipo"]]}>')
    for fid, s, t, l in flows:
        nm = f' name="{escape(l)}"' if l else ""
        L.append(f'    <sequenceFlow id="{fid}"{nm} sourceRef="{s}" targetRef="{t}"/>')
    L.append('  </process>')
    L.append(f'  <bpmndi:BPMNDiagram id="dia_{nombre}">')
    L.append(f'    <bpmndi:BPMNPlane id="plano_{nombre}" bpmnElement="colab_{nombre}">')
    L.append(f'      <bpmndi:BPMNShape id="pool_{nombre}_di" bpmnElement="pool_{nombre}" isHorizontal="true">'
             f'<dc:Bounds x="0" y="0" width="{ancho:.0f}" height="{alto:.0f}"/></bpmndi:BPMNShape>')
    for i, ln in enumerate(lanes):
        L.append(f'      <bpmndi:BPMNShape id="lane_{i}_di" bpmnElement="lane_{i}" isHorizontal="true">'
                 f'<dc:Bounds x="{POOL_STRIP}" y="{ln["y"]:.0f}" width="{ancho - POOL_STRIP:.0f}" '
                 f'height="{ln["h"]:.0f}"/></bpmndi:BPMNShape>')
    for n in nodos.values():
        extra = ' isMarkerVisible="true"' if n["tipo"] == "xor" else ""
        L.append(f'      <bpmndi:BPMNShape id="{n["id"]}_di" bpmnElement="{n["id"]}"{extra}>'
                 f'<dc:Bounds x="{n["cx"] - n["w"] / 2:.0f}" y="{n["cy"] - n["h"] / 2:.0f}" '
                 f'width="{n["w"]:.0f}" height="{n["h"]:.0f}"/></bpmndi:BPMNShape>')
    for fid, s, t, _ in flows:
        L.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">')
        L += [f'        <di:waypoint x="{x:.0f}" y="{y:.0f}"/>' for x, y in ruta(nodos[s], nodos[t])]
        L.append('      </bpmndi:BPMNEdge>')
    L += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</definitions>', '']
    return "\n".join(L)


# --------------------------------------------------------------------------- dibujo
def dibujar(nombre, d, lanes, nodos, ancho, alto):
    plt.rcParams["font.family"] = "Times New Roman"
    esc = 163                      # px por pulgada: el ancho entra en una página horizontal
    fig = plt.figure(figsize=(ancho / esc, alto / esc))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-2, ancho + 2)
    ax.set_ylim(alto + 2, -2)
    ax.axis("off")
    neg, gris = "#222222", "#e8e8e8"
    ax.add_patch(Rectangle((0, 0), ancho, alto, fill=False, lw=1.2, ec=neg))
    ax.add_patch(Rectangle((0, 0), POOL_STRIP, alto, fc="#f4f4f4", ec=neg, lw=1.2))
    ax.text(POOL_STRIP / 2, alto / 2, "\n".join(textwrap.wrap(d["pool"], int(alto / 7.5))), rotation=90,
            ha="center", va="center", fontsize=7, fontweight="bold", linespacing=1.0)
    for ln in lanes:
        ax.add_patch(Rectangle((POOL_STRIP, ln["y"]), ancho - POOL_STRIP, ln["h"], fill=False, lw=0.8, ec=neg))
        ax.add_patch(Rectangle((POOL_STRIP, ln["y"]), LANE_STRIP, ln["h"], fc="#fafafa", ec=neg, lw=0.8))
        ax.text(POOL_STRIP + LANE_STRIP / 2, ln["y"] + ln["h"] / 2,
                "\n".join(textwrap.wrap(ln["name"], 16 if ln["h"] <= ROW_H else 30)),
                rotation=90, ha="center", va="center", fontsize=7, linespacing=1.0)
    for fid, (s, t, l) in enumerate(d["flows"]):
        p = ruta(nodos[s], nodos[t])
        xs, ys = zip(*p)
        ax.plot(xs[:-1] + (xs[-1],), ys[:-1] + (ys[-1],), color=neg, lw=0.9, solid_joinstyle="miter")
        ax.annotate("", xy=p[-1], xytext=p[-2],
                    arrowprops=dict(arrowstyle="-|>", color=neg, lw=0.9, mutation_scale=9, shrinkA=0, shrinkB=0))
        if l:
            (x0, y0), (x1, y1) = p[0], p[1]
            if abs(y0 - y1) < 1:
                ax.text(x0 + 6, y0 - 4, l, fontsize=6.5, ha="left", va="bottom")
            else:
                ax.text(x0 + 5, y0 + (12 if y1 > y0 else -12), l, fontsize=6.5, ha="left", va="center")
    for n in nodos.values():
        x, y, w, h = n["cx"] - n["w"] / 2, n["cy"] - n["h"] / 2, n["w"], n["h"]
        if n["tipo"] in ("task", "service"):
            ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=9",
                                        fc=gris if n["nuevo"] else "white", ec=neg,
                                        lw=1.8 if n["nuevo"] else 1.0))
            if n["tipo"] == "service":   # marcador de tarea de servicio (engranaje simplificado)
                ax.add_patch(Circle((x + 10, y + 10), 4.2, fill=False, ec=neg, lw=0.9))
                ax.add_patch(Circle((x + 10, y + 10), 1.6, fc=neg, ec=neg, lw=0))
            ax.text(n["cx"], n["cy"], "\n".join(textwrap.wrap(n["nombre"], 15)), ha="center",
                    va="center", fontsize=7, linespacing=1.05)
        elif n["tipo"] in ("start", "end"):
            ax.add_patch(Circle((n["cx"], n["cy"]), EV / 2, fc="white", ec=neg,
                                lw=3.0 if n["tipo"] == "end" else 1.1))
            ax.text(n["cx"], n["cy"] + EV / 2 + 4, "\n".join(textwrap.wrap(n["nombre"], 16)),
                    ha="center", va="top", fontsize=6.5, linespacing=1.0)
        else:
            c, r = (n["cx"], n["cy"]), GW / 2
            ax.add_patch(Polygon([(c[0], c[1] - r), (c[0] + r, c[1]), (c[0], c[1] + r), (c[0] - r, c[1])],
                                 fc="white", ec=neg, lw=1.1))
            k = r * 0.38
            ax.plot([c[0] - k, c[0] + k], [c[1] - k, c[1] + k], color=neg, lw=1.6)
            ax.plot([c[0] - k, c[0] + k], [c[1] + k, c[1] - k], color=neg, lw=1.6)
            ax.text(c[0], c[1] - r - 4, "\n".join(textwrap.wrap(n["nombre"], 18)), ha="center",
                    va="bottom", fontsize=6.5, linespacing=1.0)
    fig.savefig(IMG / f"{nombre}.pdf")
    fig.savefig(IMG / f"{nombre}.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    for nombre, d in DIAGRAMAS.items():
        lanes, nodos, ancho, alto = disponer(d)
        (BASE / f"{nombre}.bpmn").write_text(xml_bpmn(nombre, d, lanes, nodos, ancho, alto), encoding="utf-8")
        dibujar(nombre, d, lanes, nodos, ancho, alto)
        print(nombre, f"{ancho:.0f}x{alto:.0f}")
