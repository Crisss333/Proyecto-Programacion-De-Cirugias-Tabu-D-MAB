# Informe de Entrega 1

- Fuente editable: main.tex.
- PDF listo para revisar: Entrega_1_Tabu_DMAB.pdf.
- [Correspondencia con la pauta y fuentes](criterios-entrega.md).
- Autores: José Basualto, Cristopher Dauros y Carlos Ruz.
- El documento presenta una **propuesta** Tabu Search + D-MAB. La mejora del controlador sigue siendo una hipótesis y los resultados exploratorios no se presentan como demostración.

## Formato

El diseño breve toma del formato oficial PUCV: papel carta, cuerpo Times de 12 pt, márgenes de 2,5 cm, interlineado sencillo, sangría de 1 cm, 10 pt entre párrafos, títulos en negrita y página abajo a la derecha. Se omitieron portada separada, índices y dedicatoria del manual de formato para cumplir la pauta OII464 de máximo cinco páginas antes de las referencias. El archivo main.tex es autónomo: incluye las referencias y no necesita otros archivos del repositorio.

## Compilación

Desde este directorio, ejecutar:

    latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=Entrega_1_Tabu_DMAB main.tex

La compilación verificada produjo 4 páginas: 3 de contenido y 1 de referencias. El resumen está dentro de las 150–200 palabras requeridas. Las entradas bibliográficas de artículos se contrastaron con las fuentes de editoriales o repositorios de autores; el artículo arXiv de 2026 se indica explícitamente como preprint.

Las fuentes docentes consultadas fueron la pauta OII464__Entrega_1 (1)-2.pdf, el directorio Template_Latex__Formato_Informes, la presentación Presentación_Hospitales__Optativo_ (3).pdf y los tres PDF de metodología DII9000 entregados para la asignatura. El repositorio docente es [Saicooh/OII464_Hospitales](https://github.com/Saicooh/OII464_Hospitales). Estos archivos originales no se modificaron.
