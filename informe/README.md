# Informe de Entrega 1

- Fuente principal: [`main.tex`](main.tex).
- Portada de asignatura: [`Portadas/portada_principal.tex`](Portadas/portada_principal.tex).
- Bibliografía APA/Biber: [`referencias.bib`](referencias.bib).
- PDF final: [`Entrega_1_Tabu_DMAB.pdf`](Entrega_1_Tabu_DMAB.pdf).
- [Correspondencia con la pauta y fuentes](criterios-entrega.md).

Autores: José Basualto, Cristopher Dauros y Carlos Ruz.

## Formato institucional

El informe **usa directamente** `pucv_inf_2024.sty` y el encabezado gráfico
`Portadas/imagenes/encabezado.png` de la plantilla de la Escuela de Ingeniería
Informática PUCV facilitada para el proyecto. Sus copias conservan los mismos
hashes SHA-256 que los archivos originales. La portada para asignaturas se
adaptó con título, autores, ramo y fecha; se corrigió el folio de la portada
para que no aparezca numerada.

Se mantienen papel carta, cuerpo Times de 12 puntos, márgenes de 2,5 cm,
interlineado sencillo, sangría de 1 cm, 10 puntos entre párrafos, títulos del
paquete institucional y folio inferior derecho. El resumen usa numeración
romana y el cuerpo, arábiga. No se copiaron dedicatoria, índices ni texto del
manual de la plantilla porque no forman parte de este informe de asignatura.

El PDF compilado tiene **siete páginas físicas**: portada, cinco páginas de
contenido (resumen y cuatro de cuerpo) y una de referencias. La portada se
trata como preliminar institucional aparte del límite de cinco páginas de
contenido de la pauta, según la decisión del equipo en este chat. El resumen
contiene 195 palabras, dentro del rango de 150–200.

## Compilación

Se requiere una distribución LaTeX con `biblatex` y Biber. En un entorno con
Biber funcional, desde este directorio:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -jobname=Entrega_1_Tabu_DMAB main.tex
```

La compilación manual equivalente es `pdflatex`, `biber` y dos pasadas más de
`pdflatex`, siempre con el nombre de trabajo `Entrega_1_Tabu_DMAB`. En el
Mac donde se generó el PDF, el lanzador universal de Biber 2.21 falló al
extraer su arquitectura. Se ejecutó su binario ARM64 obtenido con `lipo`, y
la secuencia manual terminó correctamente. Es una particularidad de esa
instalación de TeX, no una dependencia del documento.

El informe presenta la propuesta y una validación preliminar, con seis
estudios relacionados. Los resultados no demuestran una mejora general de
D-MAB. Las fuentes docentes consultadas fueron la pauta OII464, los tres
PDF de metodología de investigación, la presentación del problema y el
[repositorio docente](https://github.com/Saicooh/OII464_Hospitales). Ninguno
de esos originales se modificó.
