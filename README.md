# Proyecto Programación De Cirugías (Tabu + D-MAB)

Proyecto de la asignatura **Diseños Híbridos para Optimización**. Estudiamos si
un controlador de aprendizaje en línea puede elegir mejores movimientos para
Tabu Search al programar anestesia y cirugía con salas, personal y esperas
máximas. La Entrega 1 presenta la propuesta y un protocolo reproducible; los
resultados empíricos se documentan con sus límites.

## Idea central

Cada solución ordena las cirugías y asigna una sala a anestesia y otra a
cirugía. Un planificador estricto asigna personal elegible y comprueba la
disponibilidad de recursos y la espera máxima entre etapas. Ambas etapas
pueden usar salas diferentes y no se impone equilibrio entre pabellones.

Tabu Search prueba cinco movimientos: intercambio, inserción, cambio de sala
de anestesia, cambio de sala de cirugía y cambio de ambas salas. **D-MAB**
usa recompensas observadas durante la corrida para escoger cuál probar en
cada candidato. Se compara con el mismo Tabu que elige movimientos
uniformemente y con UCB1 sin reinicio Page–Hinkley, una ablación del
controlador dinámico. FIFO, SPT y LPT son reglas clásicas de referencia.

El objetivo primario es

`makespan + 1e-6 × suma de inicios + 0,5 × bloqueo total + 1,4 × bloqueo máximo`.

También se reportan makespan, bloqueo, tiempo de ejecución y variación entre
semillas por separado. D-MAB **no se entrena fuera de línea** ni detecta
directamente óptimos locales; adapta sus preferencias según la recompensa de
los movimientos.

## Entrega 1

- [Informe en LaTeX](informe/main.tex), [PDF compilado](informe/Entrega_1_Tabu_DMAB.pdf)
  y [matriz de criterios de la entrega](informe/criterios-entrega.md).
- [Metodología experimental completa](docs/metodologia-experimental.md).
- [Resultados de validación](experiments/results/validation_20_39/ANALYSIS.md),
  [ablación D-MAB frente a UCB1](experiments/results/validation_20_39/ABLATION.md),
  [corridas individuales](experiments/results/validation_20_39/runs.csv),
  [manifiesto reproducible](experiments/results/validation_20_39/manifest.json),
  [gráfico comparativo](experiments/results/validation_20_39/comparison.png),
  [diferencias emparejadas](experiments/results/validation_20_39/paired_differences.png)
  y [convergencia ilustrativa](experiments/results/validation_20_39/convergence.png).
- [Resultados exploratorios anteriores](experiments/results/exploratory_0_19/README.md),
  archivados por separado de la validación.

En los 240 pares instancia–semilla, D-MAB mejoró el objetivo de Tabu uniforme
en 106, tuvo una diferencia menor que 0,25 minutos en 39 y lo empeoró en 95.
**No hay una ventaja general demostrada.** El bloqueo mediano fue cero en todo
el catálogo, por lo que estas instancias distinguen sobre todo el makespan.

## Instalar y reproducir

Se requiere Python 3.11 o posterior. Desde la raíz del repositorio:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/python -m pytest -q
.venv/bin/python -m experiments.run_study --seed-start 20 --seed-count 20
.venv/bin/python -m experiments.verify_results
.venv/bin/python -m experiments.analyze_ablation
.venv/bin/python -m experiments.finalize_analysis
.venv/bin/python -m experiments.plot_paired_differences
.venv/bin/python -m experiments.plot_convergence --seed 20
.venv/bin/python -m experiments.audit_replay --seed 20
```

El estudio ejecuta las tres políticas en **12 instancias sintéticas × 20
semillas nuevas**, con **3.030 evaluaciones** por corrida, incluidas 30
soluciones iniciales compartidas. Es una ejecución de varios minutos. El
archivo `runs.csv` se actualiza tras cada corrida y el comando se puede
reanudar; el manifiesto impide reanudar con otra configuración o datos.
Las doce instancias son las mismas del piloto exploratorio; solo cambian las
semillas. La validación comprueba robustez frente al azar de la búsqueda
dentro de este catálogo, no desempeño en instancias aún no vistas.

## Organización

| Ruta | Contenido |
|---|---|
| [`informe/`](informe/) | Informe de la primera entrega, fuentes y PDF. |
| [`src/surgery_optim/`](src/surgery_optim/) | Datos, planificador estricto, función objetivo, Tabu y D-MAB. |
| [`instances/standard/`](instances/standard/) | Doce instancias YAML sintéticas de 15 a 30 cirugías. |
| [`experiments/run_study.py`](experiments/run_study.py) | Protocolo de evaluación emparejada y generación de CSV/gráficos. |
| [`experiments/results/validation_20_39/`](experiments/results/validation_20_39/) | Corridas de validación con semillas 20–39. |
| [`experiments/results/exploratory_0_19/`](experiments/results/exploratory_0_19/) | Archivo de pilotos anteriores, sin combinarlo con la validación. |
| [`tests/`](tests/) | Restricciones, factibilidad, reproducibilidad y paridad histórica. |

## Procedencia y alcance

El [repositorio oficial del caso](https://github.com/Saicooh/OII464_Hospitales)
se utilizó como referencia y **no se modificó**. Las instancias estándar se
copiaron de la copia local del catálogo sintético usada en el proyecto
exploratorio; no son pacientes reales ni se presentan como los cuatro JSON
históricos del taller. El código de este repositorio extrae y adapta solo
las partes pertinentes de esa copia de trabajo; la correspondencia por
módulo, el protocolo y los hashes de código e instancias están en la
[documentación metodológica](docs/metodologia-experimental.md) y el
[manifiesto](experiments/results/validation_20_39/manifest.json).

Las mejoras de D-MAB son una **hipótesis experimental**, no un resultado
garantizado. Ninguna corrida demuestra optimalidad global. Los resultados
deben interpretarse dentro de este catálogo sintético y presupuesto fijo.
