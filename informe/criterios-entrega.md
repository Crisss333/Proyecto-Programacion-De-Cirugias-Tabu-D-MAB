# Revisión de la Entrega 1

Este archivo ayuda al equipo a revisar el informe; la pauta oficial y el PDF
compilado prevalecen si hubiera alguna diferencia.

| Requisito de la pauta | Ubicación en `main.tex` |
|---|---|
| Resumen de 150–200 palabras y palabras clave | Resumen de 182 palabras y cinco palabras clave |
| Motivación, problema, pregunta y objetivo | Introducción |
| Síntesis de 3–6 estudios relacionados | Un párrafo comparativo: cinco estudios de 2024–2026 y fundamento de D-MAB de 2008 |
| Gancho de la arquitectura híbrida | Selección online de movimientos con D-MAB en la evolución de Tabu; cartera fija con respaldo |
| Componentes MH, ML, datos y orquestación offline/online | Subsecciones 2.2–2.5; reparto fijo separado del aprendizaje interno |
| Métricas, baselines, ablación y criterio de parada | Subsecciones 2.1, 2.4 y 2.5; Tabla 1; 6.060 evaluaciones totales |
| Datos sensibles, cómputo y riesgos metodológicos | Subsección 2.5: datos sintéticos, costo medido y controles de cómputo y reparación |
| Conclusión de 3–5 oraciones, máximo media página | Cinco oraciones en página propia, con limitaciones y pasos del semestre |
| Extensión máxima de cinco páginas sin referencias | Cinco páginas físicas antes de referencias, incluida la portada; referencias en una sexta página |

El documento carga directamente `pucv_inf_2024.sty`, la portada de
asignatura adaptada y el encabezado gráfico de la plantilla institucional:
papel carta, fuente Times de 12 puntos, márgenes de 2,5 cm, interlineado
sencillo, sangría de 1 cm, separación de 10 puntos entre párrafos y folio
inferior derecho. Las variables se definen inmediatamente debajo de las dos
ecuaciones. La conclusión no comparte página con otras secciones.

Para redactar se consultaron los tres documentos de la clase de metodología
de la investigación (`DII9000_Metodología_de_la_Investigación__clase_1` y
sus complementarios 1 y 2), la pauta `OII464__Entrega_1`, la presentación
`Presentación_Hospitales__Optativo_`, la diapositiva de taxonomía ML → MH
y el repositorio docente
[`Saicooh/OII464_Hospitales`](https://github.com/Saicooh/OII464_Hospitales).
Los PDF de clase no se redistribuyen aquí; las seis publicaciones
citadas sí tienen su referencia y enlace persistente en `referencias.bib`.

El taller menciona cuatro instancias JSON, mientras este repositorio evalúa
doce instancias YAML sintéticas del catálogo oficial. El informe declara
este catálogo; no presenta los resultados como reproducción de los cuatro
JSON de la presentación. Los resultados usan **semillas distintas en
las mismas doce instancias**; son una validación de estabilidad en ese
catálogo, no evidencia de generalización a instancias no vistas.
