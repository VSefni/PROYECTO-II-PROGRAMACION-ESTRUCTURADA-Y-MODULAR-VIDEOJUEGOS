import json


def LeerDatosVentas():
    try:
        with open("ventas_videojuegos.json", "r", encoding="UTF-8") as f:
            datos = json.load(f)
        return datos["videojuegos"]
    except FileNotFoundError as e:
        print("Archivo no encontrado: " + e.getMessage())
    return []


def CalcularVentasTotales(datos):
    totales = {
        "na": 0,
        "eu": 0,
        "jp": 0,
        "otros": 0,
        "global": 0
    }

    for juego in datos:
        try:
            totales["na"] += juego["ventas_na"]
            totales["eu"] += juego["ventas_eu"]
            totales["jp"] += juego["ventas_jp"]
            totales["otros"] += juego["ventas_otros"]
            totales["global"] += juego["ventas_global"]
        except:
            print("Ha ocurrido un error al calcular las ventas totales de: " + juego["nombre"])

    return totales


def TopVentasPorRegion(datos, region, n):
    ventas = []

    for juego in datos:
        juegoTupla = (juego["nombre"], juego["ventas_" + region])
        ventas.append(juegoTupla)

    listaSorted = sorted(ventas, key=lambda x: x[1], reverse=True)
    return listaSorted[:n]


def AnalizarPorGenero(datos):
    analizado = {}

    for juego in datos:
        try:
            if juego["genero"] not in analizado:
                analizado.update({
                    juego["genero"]: {
                        "cantidad_juegos": 1,
                        "ventas_global": juego["ventas_global"],
                        "ventas_na": juego["ventas_na"],
                        "ventas_eu": juego["ventas_eu"],
                        "ventas_jp": juego["ventas_jp"]
                    }
                })
            else:
                analizado[juego["genero"]] = {
                    "cantidad_juegos": analizado[juego["genero"]]["cantidad_juegos"] + 1,
                    "ventas_global": analizado[juego["genero"]]["ventas_global"] + juego["ventas_global"],
                    "ventas_na": analizado[juego["genero"]]["ventas_na"] + juego["ventas_na"],
                    "ventas_eu": analizado[juego["genero"]]["ventas_eu"] + juego["ventas_eu"],
                    "ventas_jp": analizado[juego["genero"]]["ventas_jp"] + juego["ventas_jp"]
                }
        except:
            print("Error al analizar el juego: " + juego["nombre"])

    return analizado


def CalcularVentasPromedioPorPlataforma(datos):
    suma = {
        "wii": 0,
        "nes": 0,
        "gb": 0,
    }
    contwii = 0
    contnes = 0
    contgb = 0
    for i in datos:
        if i["plataforma"] == "Wii":
            suma["wii"] += i["ventas_global"]
            contwii = contwii + 1
        elif i["plataforma"] == "NES":
            suma["nes"] = i["ventas_global"]
            contnes = contnes + 1
        elif i["plataforma"] == "GB":
            suma["gb"] = i["ventas_global"]
            contgb = contgb + 1
    promediowii = suma["wii"] / contwii
    promediones = suma["nes"] / contnes
    promediogb = suma["gb"] / contgb

    retorno = {
        "Wii": promediowii,
        "NES": promediones,
        "GB": promediogb
    }

    return retorno

def FiltrarPorRangoAnios(datos, anio_inicio, anio_fin):
    juegos = []
    for i in datos:
        if anio_inicio <= i["anio"] <= anio_fin:
            juegos.append(i["nombre"])
    return juegos

def GenerarReporteCompleto(datos):
    if not datos:
        print("No hay datos para generar el reporte.")
        return

    totales = CalcularVentasTotales(datos)
    print(f"\n[ESTADÍSTICAS GENERALES]")
    print(f"Total de juegos analizados: {len(datos)}")
    print(
        f"Ventas Totales (Millones): NA: {totales['na']} | EU: {totales['eu']} | JP: {totales['jp']} | Global: {totales['global']}")

    print(f"\n[TOP 5 VENTAS POR REGIÓN]")
    for reg in ['na', 'eu', 'jp', 'global']:
        top = TopVentasPorRegion(datos, reg, 5)
        for i, (nombre, venta) in enumerate(top, 1):
            print(f" {i}. {nombre[:30]:<30} | {venta}M")

    print(f"\n[ANÁLISIS POR GÉNERO]")
    generos = AnalizarPorGenero(datos)

    for gen, stat in generos.items():
        print(f"{gen:<15} | {stat['cantidad_juegos']:<8} | {stat['ventas_global']:<15}")

    print(f"\n[PROMEDIO DE VENTAS POR PLATAFORMA (TOP 5)]")
    prom_plat = CalcularVentasPromedioPorPlataforma(datos)

    plat_ordenadas = sorted(prom_plat.items(), key=lambda x: x[1], reverse=True)

    for plat, prom in plat_ordenadas[:3]:
        print(f"Plataforma: {plat:<10} | Promedio Global: {prom}M")

    print(f"\n[FILTRO POR AÑO]")
    fecinicio = input("Introduce tu fecha de incio: ")
    fecfin = input("Introduce tu fecha de fin: ")
    recientes = FiltrarPorRangoAnios(datos, fecinicio, fecfin)
    print(f"Juegos lanzados entre {fecinicio} y {fecfin}: {len(recientes)}")


if __name__ == '__main__':
    while True:
        print("Reporte Juegos")
        print("-----------------------------------")
        print("1. Ver reporte")
        print("2. Top ventas region")
        print("3. Análisis por género")
        print("4. Ventas promedio por plataforma")
        print("5. Filtrar por rango de años")
        print("6. Calcular ventas totales")
        print("7. Ver todos los datos")
        print("0. Salir")
        opcion = input("Introduce una opcion: ")
        if int(opcion) == 0:
            break
        else:
            datos = LeerDatosVentas()
            match int(opcion):
                case 1:
                    print(datos)
                case 2:
                    topVentas = TopVentasPorRegion(datos, "na", 10)
                    print(topVentas)
                case 3:
                    analizarPorGenero = AnalizarPorGenero(datos)
                    print(analizarPorGenero)
                case 4:
                    calcularVentasPromedioPorPlataforma = CalcularVentasPromedioPorPlataforma(datos)
                    print(calcularVentasPromedioPorPlataforma)
                case 5:
                    filtrarRangoAnios = FiltrarPorRangoAnios(datos, 2000, 2026)
                    print(filtrarRangoAnios)
                case 6:
                    calcularVentasTotales = CalcularVentasTotales(datos)
                    print(calcularVentasTotales)
                case 7:
                    GenerarReporteCompleto(datos)
                case _:
                    print("Opción no existente, inténtalo de nuevo.")
