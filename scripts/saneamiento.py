import pandas as pd
import hashlib

archivo_original = "./datos/telemetria_envios.csv"
archivo_limpio = "./datos/telemetria_limpios.csv"

def obtener_sha256(ruta_fichero):
    sha = hashlib.sha256()
    with open(ruta_fichero, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha.update(bloque)
    return sha.hexdigest()

print("===============LIMPIEZA CSV===============")

print("\nTabla original")
datos = pd.read_csv(archivo_original)
print(datos)

print("\nTotal de registros:", len(datos))

print("\n--------Informacion de las columnas--------")
print(datos.info())

print("\n--------Registro de peso_kg--------")
print(datos["peso_kg"].describe().round(2))

print("\n--------Registro de temp_celsius--------")
print(datos["temp_celsius"].describe().round(2))

print("\n--------Registro de estado_envio--------")
print(datos["estado_envio"].value_counts(dropna=False))

datos_limpiar = datos.drop_duplicates()

datos_limpiar = datos_limpiar.dropna(subset=["temp_celsius", "peso_kg", "destino"])

datos_limpiar = datos_limpiar[datos_limpiar["temp_celsius"] < 50]
datos_limpiar = datos_limpiar[datos_limpiar["peso_kg"] > 0]
datos_limpiar = datos_limpiar[datos_limpiar["estado_envio"] != "DESCONOCIDO_ERROR"]

print("\nTotal de registros despues de la limpieza:", len(datos_limpiar))

datos_limpiar.to_csv(archivo_limpio, index=False)
print("Datos limpios guardados en:", archivo_limpio)

print("\n--------Prueba Hash--------")

print("Codigo Hash original:", obtener_sha256(archivo_original))
print("Codigo Hash nuevo:", obtener_sha256(archivo_limpio))