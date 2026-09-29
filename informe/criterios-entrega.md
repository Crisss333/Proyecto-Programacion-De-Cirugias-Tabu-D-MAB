# Revisión de la Entrega 1

Este archivo ayuda al equipo a revisar el informe; la pauta oficial y el PDF
compilado prevalecen si hubiera alguna diferencia.

| Requisito de la pauta | Ubicación en `main.tex` |
|---|---|
| Resumen de 150–200 palabras y palabras clave | Resumen preliminar (194 palabras) |
| Motivación, problema, pregunta y objetivo | Introducción |
| Síntesis de 3–6 estudios relacionados | Párrafo comparativo en la introducción (seis estudios) |
| Gancho de la arquitectura híbrida | Propuesta metodológica: selección online de movimientos con D-MAB |
| Componentes MH, ML, datos y orquestación offline/online | Subsecciones 2.2, 2.3 y 2.4 |
| Métricas, baselines, ablación y criterio de parada | Subsecciones 2.1–2.4 y tabla 1 |
| Datos sensibles y recursos de cómputo | Subsección 2.4: datos sintéticos, número de corridas y evaluaciones, tiempo mediano |
| Conclusión y referencias | Conclusión en página propia (menos de media página) y sección de referencias |
| Extensión máxima de cinco páginas de contenido | Cinco páginas de contenido; portada institucional y referencias aparte |

El documento carga directamente `pucv_inf_2024.sty`, la portada de
asignatura adaptada y el encabezado gráfico de la plantilla institucional:
papel carta, fuente Times de 12 puntos, márgenes de 2,5 cm, interlineado
sencillo, sangría de 1 cm, separación de 10 puntos entre párrafos y folio
inferior derecho. No reutiliza contenido del informe anterior de GWO/BCO.

Para redactar se consultaron los tres documentos de la clase de metodología
de la investigación (`DII9000_Metodología_de_la_Investigación__clase_1` y
sus complementarios 1 y 2), la pauta `OII464__Entrega_1`, la presentación
`Presentación_Hospitales__Optativo_` y el repositorio docente
[`Saicooh/OII464_Hospitales`](https://github.com/Saicooh/OII464_Hospitales).
Los PDF de clase no se redistribuyen aquí; las seis publicaciones
citadas sí tienen su referencia y enlace persistente en `referencias.bib`.

El taller menciona cuatro instancias JSON, mientras este repositorio evalúa
doce instancias YAML sintéticas disponibles en la copia local del caso. El
informe identifica esta diferencia y no afirma haber reproducido un benchmark
oficial de cuatro JSON. Los resultados nuevos usan **semillas distintas en
las mismas doce instancias**; son una validación de estabilidad en ese
catálogo, no evidencia de generalización a instancias no vistas.
