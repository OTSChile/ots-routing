def aplicar_reglas_vehiculo(vehiculo, reglas):
    if not vehiculo.get("disponible", True):  # Si 'disponible' no existe, asume que es True
        return None  # Si el vehículo no está disponible, retorna None o podría retornar el vehículo sin cambios

    # Encuentra y aplica las reglas específicas para el tipo de vehículo.
    for regla in reglas:
        if regla["tipo"] == vehiculo["tipo"]:
            vehiculo_modificado = vehiculo.copy()
            # Aplica las reglas de tolerancia al vehículo
            vehiculo_modificado["capacidad_peso"] *= (1 + regla.get("tolerancia_carga", 0) / 100)
            vehiculo_modificado["capacidad_volumen"] *= (1 + regla.get("tolerancia_volumen", 0) / 100)
            vehiculo_modificado["bultos_maximo"] = regla.get("bultos_maximo", vehiculo.get("bultos_maximo", 0))
            return vehiculo_modificado
    return vehiculo
