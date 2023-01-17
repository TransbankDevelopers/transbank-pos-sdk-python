response_codes = {
    0: "Aprobado",
    1: "Rechazado",
    2: "Host no Responde",
    3: "Conexión Fallo",
    4: "Transacción ya Fue Anulada",
    5: "No existe Transacción para Anular",
    6: "Tarjeta no Soportada",
    7: "Transacción Cancelada desde el POS",
    8: "No puede Anular Transacción Debito",
    9: "Error Lectura Tarjeta",
    10: "Monto menor al mínimo permitido",
    11: "No existe venta",
    12: "Transacción No Soportada",
    13: "Debe ejecutar cierre ",
    14: "No hay Tono",
    15: "Archivo BITMAP.DAT no encontrado. Favor cargue",
    16: "Error Formato Respuesta del HOST",
    17: "Error en los 4 últimos dígitos.",
    18: "Menú invalido",
    19: "ERROR_TARJ_DIST",
    20: "Tarjeta Invalida",
    21: "Anulación no Permitida",
    22: "TIMEOUT",
    24: "Impresora Sin Papel",
    25: "Fecha Invalida",
    26: "Debe Cargar Llaves",
    27: "Debe Actualizar",
    60: "Error en Número de Cuotas",
    61: "Error en Armado de Solicitud",
    62: "Problema con el Pinpad interno",
    65: "Error al Procesar la Respuesta del Host",
    67: "Superó Número Máximo de Ventas, Debe Ejecutar Cierre",
    68: "Error Genérico, Falla al Ingresar Montos",
    70: "Error de formato Campo de Boleta MAX 6",
    71: "Error de Largo Campo de Impresión",
    72: "Error de Monto Venta, Debe ser Mayor que 0",
    73: "Terminal ID no configurado",
    74: "Debe Ejecutar CIERRE",
    75: "Comercio no tiene Tarjetas Configuradas",
    76: "Supero Número Máximo de Ventas, Debe Ejecutar CIERRE",
    77: "Debe Ejecutar Cierre",
    78: "Esperando Leer Tarjeta",
    79: "Solicitando Confirmar Monto",
    80: "Selección de Cuotas",
    81: "Solicitando Ingreso de Clave",
    82: "Enviando transacción al Host",
    83: "Seleccion menu credito/redcompra",
    84: "Opere tarjeta",
    85: "Seleccion de cuotas",
    86: "Ingreso de cuotas",
    87: "Confirmacion de cuotas",
    88: "Error Cantidad Cuotas",
    93: "Declinada",
    94: "Error al Procesar Respuesta",
    95: "Error al Imprimir TASA"
}


def get_message(code: int):
    message = response_codes.get(code, 'No encontrado')
    return message
