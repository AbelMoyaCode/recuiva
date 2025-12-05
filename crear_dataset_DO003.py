#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script temporal para generar el dataset DO-003 en formato CSV
con codificación UTF-8 BOM para compatibilidad con Excel.

Autor: Abel Moya
Fecha: 2 de diciembre de 2025
"""

import csv
import os

# Datos del dataset DO-003 (basado en el PDF del Collar de la Reina)
dataset = [
    {
        "ID": 1,
        "Pregunta": "¿Qué era el famoso collar de la reina en la historia?",
        "Respuesta": "Era un collar de diamantes muy costoso encargado originalmente para María Antonieta.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Correcto",
        "Coincide": ""
    },
    {
        "ID": 2,
        "Pregunta": "¿Qué papel tuvo el cardenal de Rohan en la estafa?",
        "Respuesta": "Era un cardenal manipulado para creer que la reina quería que él comprara el collar.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Correcto",
        "Coincide": ""
    },
    {
        "ID": 3,
        "Pregunta": "¿Por qué la reputación de María Antonieta ya estaba dañada antes del escándalo del collar?",
        "Respuesta": "Porque circulaban muchos chismes sobre su vida lujosa y alejamiento del pueblo.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 4,
        "Pregunta": "¿Quién era Jeanne de Valois-Saint-Rémy y cómo participó en el engaño?",
        "Respuesta": "Era una falsa condesa que planeó la estafa y fingió ser cercana a la reina.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Correcto",
        "Coincide": ""
    },
    {
        "ID": 5,
        "Pregunta": "¿Qué engaño se realizó en los jardines de Versalles durante la noche?",
        "Respuesta": "Hicieron que el cardenal creyera reunirse con una mujer disfrazada de María Antonieta.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 6,
        "Pregunta": "¿Por qué los joyeros confiaron en que recibirían el pago del collar?",
        "Respuesta": "Porque había un contrato donde parecía que la reina aprobaba la compra.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 7,
        "Pregunta": "¿Qué hizo Jeanne con el collar una vez que lo obtuvo?",
        "Respuesta": "Mandó desarmar el collar y vender los diamantes.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Correcto",
        "Coincide": ""
    },
    {
        "ID": 8,
        "Pregunta": "¿Cómo se enteró finalmente María Antonieta de lo que estaba ocurriendo?",
        "Respuesta": "Los joyeros acudieron a reclamar el pago y estalló el escándalo.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Correcto",
        "Coincide": ""
    },
    {
        "ID": 9,
        "Pregunta": "¿Qué consecuencias políticas tuvo el caso del collar?",
        "Respuesta": "Aumentó el odio hacia la monarquía y debilitó la imagen pública de la reina.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 10,
        "Pregunta": "¿Por qué se considera que el caso del collar influyó en la Revolución Francesa?",
        "Respuesta": "Reforzó la idea de que la corte era corrupta y ajena al pueblo.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 11,
        "Pregunta": "¿Qué buscaba el cardenal de Rohan al participar en el escándalo del collar?",
        "Respuesta": "Reconquistar el favor político de la reina.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 12,
        "Pregunta": "¿Cómo se usaron las cartas falsas en el plan?",
        "Respuesta": "Eran cartas falsificadas para que el cardenal creyera que hablaba con la reina.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 13,
        "Pregunta": "¿Qué papel tuvo la mujer que se hizo pasar por la reina en el jardín?",
        "Respuesta": "Solo apareció un momento para engañar al cardenal.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 14,
        "Pregunta": "¿Por qué los joyeros aceptaron rebajar el precio del collar?",
        "Respuesta": "Jeanne los convenció de que sería más fácil que la reina pagara luego.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 15,
        "Pregunta": "¿Qué pasó con Jeanne después de que estalló el escándalo?",
        "Respuesta": "Fue juzgada públicamente y terminó perdiendo credibilidad.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 16,
        "Pregunta": "¿Qué representaba el collar para la sociedad francesa?",
        "Respuesta": "Era un símbolo del exceso y lujo de la nobleza.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 17,
        "Pregunta": "¿Qué muestra el caso del collar sobre la relación entre la corte y el pueblo?",
        "Respuesta": "Que había mucha desconfianza hacia la realeza.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 18,
        "Pregunta": "¿Qué oportunidad aprovechó la prensa para criticar a la reina?",
        "Respuesta": "El escándalo del collar se usó para atacar su imagen.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Parcial",
        "Coincide": ""
    },
    {
        "ID": 19,
        "Pregunta": "¿Cómo el cardenal de Rohan organizó el engaño a la reina?",
        "Respuesta": "Porque Jeanne lo manipuló haciéndole creer que la reina lo quería de vuelta.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Incorrecto",
        "Coincide": ""
    },
    {
        "ID": 20,
        "Pregunta": "¿Qué ocurrió al final con el collar cuando la reina quiso quemarlo?",
        "Respuesta": "La reina mandó destruirlo para demostrar inocencia.",
        "Score": "",
        "Clasificacion_Auto": "",
        "Clasificacion_Manual": "Incorrecto",
        "Coincide": ""
    }
]

# Ruta del archivo de salida
output_file = "DO-003_collar_reina.csv"

# Crear el archivo CSV con UTF-8 BOM
print(f"📝 Creando dataset DO-003 en formato CSV...")
print(f"📁 Ruta: {os.path.abspath(output_file)}")

with open(output_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
    # Definir columnas
    fieldnames = [
        'ID',
        'Pregunta',
        'Respuesta del usuario',
        'Score %',
        'Clasificación Auto',
        'Clasificación Manual',
        '¿Coincide?'
    ]
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Escribir encabezados
    writer.writeheader()
    
    # Escribir datos
    for row in dataset:
        writer.writerow({
            'ID': row['ID'],
            'Pregunta': row['Pregunta'],
            'Respuesta del usuario': row['Respuesta'],
            'Score %': row['Score'],
            'Clasificación Auto': row['Clasificacion_Auto'],
            'Clasificación Manual': row['Clasificacion_Manual'],
            '¿Coincide?': row['Coincide']
        })

print("✅ Archivo CSV creado exitosamente!")
print(f"📊 Total de casos: {len(dataset)}")
print(f"📍 Distribución:")
print(f"   - Correctos: {sum(1 for r in dataset if r['Clasificacion_Manual'] == 'Correcto')}")
print(f"   - Parciales: {sum(1 for r in dataset if r['Clasificacion_Manual'] == 'Parcial')}")
print(f"   - Incorrectos: {sum(1 for r in dataset if r['Clasificacion_Manual'] == 'Incorrecto')}")
print("")
print("🔹 Ahora puedes:")
print("   1. Abrir el archivo en Excel (se verán correctamente las tildes y ñ)")
print("   2. Llenar las columnas 'Score %' y 'Clasificación Auto' con los resultados de tu sistema")
print("   3. Marcar 'Sí' o 'No' en la columna '¿Coincide?' comparando Auto vs Manual")
print("   4. Calcular las métricas finales al pie de la tabla")
