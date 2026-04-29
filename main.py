import heapq


def generar_grafo():
    """
    Genera un grafo dirigido ponderado sintético.
    Cada nodo representa una entidad y cada arista representa una conexión con costo.
    """

    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("D", 5)],
        "C": [("B", 1), ("D", 8)],
        "D": [("E", 2)],
        "E": [("F", 3)],
        "F": [],

        # Nodos desconectados para probar casos sin solución
        "X": [("Y", 1)],
        "Y": []
    }

    return grafo


def dijkstra(grafo, inicio, fin):
    """
    Encuentra la ruta de menor costo entre dos nodos usando Dijkstra.
    """

    cola_prioridad = [(0, inicio, [inicio])]
    nodos_visitados = set()

    while cola_prioridad:
        costo_actual, nodo_actual, ruta_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == fin:
            return costo_actual, ruta_actual

        if nodo_actual in nodos_visitados:
            continue

        nodos_visitados.add(nodo_actual)

        for vecino, costo_arista in grafo.get(nodo_actual, []):
            if vecino not in nodos_visitados:
                nuevo_costo = costo_actual + costo_arista
                nueva_ruta = ruta_actual + [vecino]

                heapq.heappush(
                    cola_prioridad,
                    (nuevo_costo, vecino, nueva_ruta)
                )

    return None, None


def validar_arista_obligatoria(ruta, nodo_u, nodo_v):
    """
    Valida si la arista obligatoria (nodo_u, nodo_v)
    aparece dentro de la ruta final.
    """

    for indice in range(len(ruta) - 1):
        if ruta[indice] == nodo_u and ruta[indice + 1] == nodo_v:
            return True

    return False


def ruta_minima_con_arista_obligatoria(
    grafo,
    origen,
    destino,
    nodo_u,
    nodo_v
):
    """
    Calcula la ruta de menor costo desde origen hasta destino,
    incluyendo obligatoriamente la arista (nodo_u, nodo_v).
    """

    costo_arista_obligatoria = None

    # 1. Validar que la arista obligatoria exista en el grafo
    for vecino, costo in grafo.get(nodo_u, []):
        if vecino == nodo_v:
            costo_arista_obligatoria = costo
            break

    if costo_arista_obligatoria is None:
        return {
            "estatus": "No existe solución válida",
            "razon": f"La arista obligatoria ({nodo_u}, {nodo_v}) no existe en el grafo."
        }

    # 2. Buscar la ruta mínima desde el origen hasta nodo_u
    costo_1, ruta_1 = dijkstra(grafo, origen, nodo_u)

    if ruta_1 is None:
        return {
            "estatus": "No existe solución válida",
            "razon": f"No existe ruta desde {origen} hasta {nodo_u}."
        }

    # 3. Buscar la ruta mínima desde nodo_v hasta el destino
    costo_2, ruta_2 = dijkstra(grafo, nodo_v, destino)

    if ruta_2 is None:
        return {
            "estatus": "No existe solución válida",
            "razon": f"No existe ruta desde {nodo_v} hasta {destino}."
        }

    # 4. Combinar rutas
    ruta_final = ruta_1 + ruta_2
    costo_total = costo_1 + costo_arista_obligatoria + costo_2

    return {
        "estatus": "Solución válida",
        "ruta": ruta_final,
        "costo_total": costo_total,
        "arista_obligatoria": (nodo_u, nodo_v),
        "arista_aparece_en_ruta": validar_arista_obligatoria(
            ruta_final,
            nodo_u,
            nodo_v
        )
    }


if __name__ == "__main__":
    grafo = generar_grafo()

    print("Caso 1: solución válida")
    resultado = ruta_minima_con_arista_obligatoria(
        grafo=grafo,
        origen="A",
        destino="F",
        nodo_u="B",
        nodo_v="D"
    )
    print(resultado)

    print("\nCaso 2: sin solución")
    resultado = ruta_minima_con_arista_obligatoria(
        grafo=grafo,
        origen="X",
        destino="F",
        nodo_u="B",
        nodo_v="D"
    )
    print(resultado)

    print("\nCaso 3: caso borde - arista obligatoria inexistente")
    resultado = ruta_minima_con_arista_obligatoria(
        grafo=grafo,
        origen="A",
        destino="F",
        nodo_u="C",
        nodo_v="A"
    )
    print(resultado)