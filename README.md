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
cada candidato, con UCB1 escalado por un factor de exploración C. Se compara con el mismo Tabu que elige movimientos
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
- Resultados citados por el informe: [validación de la Entrega 1](experiments/results/validation_20_39/ANALYSIS.md)
  (semillas 20–39), archivada.
- [Resultados exploratorios anteriores](experiments/results/exploratory_0_19/README.md),
  archivados por separado de la validación.

En la Entrega 1, en los 240 pares instancia–semilla, D-MAB mejoró el objetivo
de Tabu uniforme en 106, tuvo una diferencia menor que 0,25 minutos en 39 y lo
empeoró en 95. **No hay una ventaja general demostrada.** El bloqueo mediano
fue cero en todo el catálogo, por lo que estas instancias distinguen sobre
todo el makespan.

## Versión 2: calibración y nueva validación

Una revisión mostró que, con C = 1, la exploración de UCB1 (≈0,16) era unas
diez veces mayor que la recompensa media (≈0,016): D-MAB elegía los
movimientos casi por turnos. La versión 2 agrega el factor C de Da Costa et
al., números aleatorios comunes entre políticas, conteo de movimientos que el
decodificador repara, una tolerancia única para `max_wait` y pruebas de
Wilcoxon con corrección de Holm.

- [Calibración en semillas exploratorias 0–5](experiments/results/calibration_0_5/CALIBRATION.md):
  **reducir C empeora** (C = 0,02: +2 min de media); la diversidad de
  movimientos importa más que explotar la recompensa inmediata. La memoria
  tabú por atributo también empeoró. Se eligió C = 0,1 y λ = 1.
- [Validación en semillas nuevas 40–59](experiments/results/validation_40_59/ANALYSIS.md),
  [pruebas estadísticas](experiments/results/validation_40_59/statistics.csv),
  [ablación D-MAB frente a UCB1](experiments/results/validation_40_59/ABLATION.md),
  [corridas](experiments/results/validation_40_59/runs.csv),
  [manifiesto](experiments/results/validation_40_59/manifest.json),
  [gráfico comparativo](experiments/results/validation_40_59/comparison.png),
  [diferencias emparejadas](experiments/results/validation_40_59/paired_differences.png)
  y [convergencia](experiments/results/validation_40_59/convergence.png).

| Comparación (240 pares) | Media dif. | Gana / empata / pierde | p Wilcoxon | p Holm |
|---|---:|---:|---:|---:|
| D-MAB vs Tabu mixto | +0,58 min | 101 / 13 / 126 | 0,16 | 0,16 |
| UCB1 vs Tabu mixto | +1,18 min | 100 / 14 / 126 | 0,028 | 0,084 |
| D-MAB vs UCB1 | −0,61 min | 103 / 61 / 76 | 0,059 | 0,12 |

La pequeña ventaja de la calibración **no se replicó**: D-MAB calibrado no
supera a Tabu uniforme (diferencia no significativa, ligeramente en contra) y
ninguna de las 36 pruebas por instancia es significativa tras Holm. UCB1 sin
reinicio tiende a ser peor que uniforme y que D-MAB, lo que sugiere que el
valor de Page–Hinkley aquí es **devolver exploración**, no detectar cambios
útiles. Alrededor del 30 % de los candidatos sale del decodificador distinto
de la propuesta, de modo que la recompensa a menudo se atribuye a un
movimiento que no se aplicó tal cual.

## Instalar y reproducir

Se requiere Python 3.11 o posterior. Desde la raíz del repositorio:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/python -m pytest -q
.venv/bin/python -m experiments.calibrate --workers 2   # opcional, semillas 0–5
.venv/bin/python -m experiments.run_study --seed-start 40 --seed-count 20
.venv/bin/python -m experiments.verify_results
.venv/bin/python -m experiments.analyze_ablation
.venv/bin/python -m experiments.finalize_analysis
.venv/bin/python -m experiments.plot_paired_differences
.venv/bin/python -m experiments.plot_convergence --seed 40
.venv/bin/python -m experiments.audit_replay --seed 40
```

El estudio ejecuta las tres políticas en **12 instancias sintéticas × 20
semillas nuevas**, con **3.030 evaluaciones** por corrida, incluidas 30
soluciones iniciales compartidas. Tarda entre 15 y 45 minutos según el
equipo. El
archivo `runs.csv` se actualiza tras cada corrida y el comando se puede
reanudar; el manifiesto impide reanudar con otra configuración o datos.
Las doce instancias son las mismas del piloto exploratorio; solo cambian las
semillas. La validación comprueba robustez frente al azar de la búsqueda
dentro de este catálogo, no desempeño en instancias aún no vistas.

## Comparación de carteras con presupuesto equivalente

El [estudio de carteras](experiments/results/portfolios_60_79/ANALYSIS.md)
compara Tabu prolongado, dos reinicios de Tabu, una cartera fija Tabu+D-MAB y
dos asignaciones aprendidas con LinUCB. Usa semillas nuevas 60–79 y **6.060
evaluaciones por alternativa**, cobrando también inicializaciones y pruebas.
La variante con respaldo conserva una ejecución completa de Tabu de 3.030;
esa protección se distingue de superar a Tabu con el presupuesto completo.

El [protocolo](docs/protocolo-carteras.md) explica estados, aprendizaje y
controles. Los resultados incluyen soluciones revalidables, decisiones online
y un gráfico de diferencias con incertidumbre agrupada por instancia.

La [decisión de arquitectura](experiments/results/portfolios_60_79/DECISION.md)
recomienda continuar con la **cartera fija Tabu+D-MAB y conservar el mejor**,
sin añadir LinUCB por ahora. Con igual presupuesto, dos Tabu y el reparto
aprendido redujeron el objetivo medio en aproximadamente 0,79; la cartera
fija lo redujo en 0,66. **Ninguna ventaja general quedó demostrada**: los
intervalos agrupados incluyen cero. Dos Tabu permanece como control para
distinguir el aprendizaje de repetir la búsqueda. El respaldo protege el
Tabu de 3.030, pero no garantiza superar al de 6.060.

## Organización

| Ruta | Contenido |
|---|---|
| [`informe/`](informe/) | Informe de la primera entrega, fuentes y PDF. |
| [`src/surgery_optim/`](src/surgery_optim/) | Datos, planificador estricto, función objetivo, Tabu y D-MAB. |
| [`instances/standard/`](instances/standard/) | Doce instancias YAML sintéticas de 15 a 30 cirugías. |
| [`experiments/run_study.py`](experiments/run_study.py) | Protocolo de evaluación emparejada y generación de CSV/gráficos. |
| [`experiments/calibrate.py`](experiments/calibrate.py) | Calibración de memoria tabú, C y λ en semillas exploratorias. |
| [`experiments/results/calibration_0_5/`](experiments/results/calibration_0_5/) | Calibración (semillas 0–5). |
| [`experiments/results/validation_40_59/`](experiments/results/validation_40_59/) | Validación vigente con semillas 40–59. |
| [`experiments/results/portfolios_60_79/`](experiments/results/portfolios_60_79/) | Carteras y asignación aprendida con presupuesto equivalente. |
| [`experiments/results/validation_20_39/`](experiments/results/validation_20_39/) | Validación de la Entrega 1, archivada. |
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
[manifiesto](experiments/results/validation_40_59/manifest.json).

Las mejoras de D-MAB son una **hipótesis experimental**, no un resultado
garantizado. Ninguna corrida demuestra optimalidad global. Los resultados
deben interpretarse dentro de este catálogo sintético y presupuesto fijo.
