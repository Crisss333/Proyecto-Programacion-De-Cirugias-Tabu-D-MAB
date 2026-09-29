# Metodología y protocolo experimental

## Pregunta e hipótesis

Se estudia si la selección adaptativa de movimientos **dentro de Tabu Search**
mejora la programación de cirugías frente a elegir movimientos de manera
uniforme, bajo la misma representación, decodificador, función objetivo,
inicialización y presupuesto. La hipótesis de mejora es falsable: si el
controlador no reduce consistentemente el objetivo con las semillas nuevas,
el estudio no sostendrá esa ventaja. D-MAB es aprendizaje **en línea**, sin
entrenamiento previo ni metacaracterísticas contextuales.

## Datos y alcance

El conjunto de validación contiene 12 instancias **completamente sintéticas**
`HOSP-STD-{15,20,25,30}-{01,02,03}.yaml`, de 15 a 30 cirugías. Cada
instancia declara salas, personal elegible, duración, preparación, transición,
limpieza y espera máxima para dos etapas: anestesia y cirugía. Se preserva el
`digest` del documento y se calcula SHA-256 del archivo en el manifiesto. Las
instancias YAML proceden de la copia local del catálogo del caso docente; no
se afirma que sean los cuatro JSON originales mencionados en la presentación.
Son **las mismas doce instancias** del estudio exploratorio anterior; lo nuevo
son las semillas 20–39. Esto prueba sensibilidad a la aleatoriedad de la
búsqueda dentro del catálogo ya observado, no generalización a instancias
hospitalarias no vistas.

El repositorio oficial del caso se utilizó como **fuente de contexto**:
<https://github.com/Saicooh/OII464_Hospitales>. Se trabajó sobre una copia
local independiente. Este proyecto no escribe en el repositorio oficial.
El commit `ecd30e3dbc1962d856c09b3470d1870c3b139a9a` fue el HEAD oficial
comprobado durante el piloto anterior; el manifiesto guarda además los hashes
de los archivos concretos usados aquí.

## Representación, factibilidad y objetivo

Una solución es una permutación de cirugías y dos asignaciones de sala por
cirugía. Se permiten salas distintas para anestesia y cirugía. No se fuerza el
equilibrio de uso de salas. Una codificación de tres claves reales por cirugía
sirve para generar y reparar soluciones, pero el algoritmo Tabu opera sobre
la solución discreta decodificada.

El planificador estricto asigna personal elegible, respeta disponibilidad de
salas y personal y **rechaza cualquier espera entre anestesia y cirugía que
supere `max_wait`** de la operación. Mientras una cirugía espera transferirse,
la sala de anestesia queda ocupada; si ambas etapas usan la misma sala, ésta
permanece ocupada durante cirugía y limpieza. Una propuesta no factible recibe
infinito y no puede ser la mejor solución. Los resultados guardados vuelven a
validarse con el planificador estricto.

Se minimiza

\[
f(S)=C_{\max}+10^{-6}\sum_{o\in S} t_o^{\mathrm{inicio}}
     +0{,}5\sum_j w_j+1{,}4\max_j w_j,
\]

donde `w_j` es el intervalo entre el fin de anestesia (incluida limpieza) y
el inicio de cirugía (después de preparación o transición). `Cmax`, la suma
de esperas y la espera máxima se reportan por separado. El pequeño término de
inicios usa `ScheduleEntry.start`, es decir, el inicio de preparación o reserva
del recurso para cada operación, y desempata soluciones cercanas. **No hay
penalización por desequilibrio
entre salas.** El objetivo combinado es la métrica primaria fijada antes de la
validación. El makespan y el bloqueo son métricas secundarias; no se interpreta
un descenso del objetivo como descenso automático de cada componente.

## Tres políticas comparadas

Todas comparten el mismo Tabu Search y cinco movimientos discretos:

1. `swap`: intercambiar dos pacientes en la secuencia.
2. `insert`: sacar un paciente e insertarlo en otra posición.
3. `room_1`: cambiar su sala de anestesia.
4. `room_2`: cambiar su sala de cirugía.
5. `room_pair`: cambiar ambas salas.

La selección del paciente prioriza, con probabilidad 0,65, a uno de los tres
con mayor espera actual, cuando los hay. El resto se elige del conjunto de
pacientes. Se generan 15 candidatos distintos por lote. La lista tabú guarda
las últimas 7 soluciones; una solución tabú se acepta si mejora el mejor valor
global. Se conservan el mejor resultado y las 30 soluciones iniciales. La
inicialización coloca FIFO, SPT y LPT en las primeras tres posiciones y genera
otras 27 por claves aleatorias; comienza Tabu desde la mejor de las 30.

| Política | Selección de cada propuesta |
|---|---|
| Tabu mixto (`uniform`) | Muestra cada uno de los cinco movimientos con probabilidad uniforme. |
| Tabu + D-MAB (`dmab`) | Usa UCB1 para seleccionar movimiento y Page–Hinkley para reiniciar estimaciones tras caída de recompensa. |
| Tabu + UCB1 (`ucb`) | Usa el mismo UCB1 sin reinicio Page–Hinkley: ablación del componente dinámico. |

La recompensa para un candidato es la mejora positiva respecto del valor local
antes del lote, dividida por `max(1, 0,02 × objetivo inicial)` y truncada en
`[0,1]`. Un candidato duplicado entrega recompensa cero. La recompensa se
actualiza después de cada propuesta evaluada. D-MAB es un bandido no
contextual: no recibe el tamaño de la instancia, el historial de estancamiento
ni una etiqueta de óptimo local. Page–Hinkley reinicia **sus estadísticas**,
no la solución ni la búsqueda Tabu.

## Comparación justa y criterio de parada

Las tres políticas usan 3.030 evaluaciones por corrida, **incluidas las 30
iniciales**. Se ejecutan con las mismas instancias y semillas enteras 20–39.
Las semillas 0–19 del estudio exploratorio anterior se mantienen separadas y
no se mezclan en la tabla de validación. Para una pareja instancia-semilla se
comprueba que las tres políticas tienen el mismo objetivo inicial. También se
verifica que se usen exactamente 3.030 evaluaciones factibles.

Los candidatos duplicados se descartan dentro de cada lote y no consumen una
evaluación del planificador, aunque sí cuestan trabajo de generación y pueden
actualizar el bandido con recompensa cero. Por eso el presupuesto iguala
evaluaciones estrictas, no necesariamente intentos de propuesta ni segundos
de CPU. `runs.csv` conserva intentos por movimiento **solo para D-MAB y
UCB1**. La política uniforme histórica no registraba el nombre del
movimiento en cada intento, de modo que sus columnas `attempted_*` y
`evaluated_*` aparecen en cero y no deben interpretarse como ausencia de
movimientos. Los duplicados de D-MAB/UCB1 actualizan el bandido con cero;
en Tabu uniforme no hay modelo que actualizar. Esta asimetría es parte de la
definición operativa de los controladores, no una evaluación adicional.

FIFO, SPT y LPT se calculan una vez por instancia como reglas clásicas de
referencia. Para cada algoritmo y cada instancia se reportan la mediana entre
20 semillas, mínimo y máximo del objetivo, mediana de makespan, bloqueo y
tiempo. La comparación principal utiliza diferencias **emparejadas** por
instancia y semilla (`alternativa − Tabu mixto`); valor negativo favorece al
controlador. Se muestran victorias, empates y derrotas con tolerancia `1e−9`.
La comparación con UCB1 ayuda a atribuir el efecto del reinicio dinámico.

Se evita agregar todas las corridas como si fueran instancias independientes:
las tres réplicas de cada tamaño son distintas, pero las veinte semillas de
una réplica comparten datos. Cualquier conclusión general debe considerar
este agrupamiento, el tamaño reducido del catálogo y que las instancias ya
influyeron en la elección de la arquitectura antes de esta validación.

## Reproducibilidad y procedencia del código

El código independiente del repositorio reutiliza y adapta las ideas y partes
de implementación de la copia de trabajo exploratoria de este proyecto:

| Módulo nuevo | Procedencia local |
|---|---|
| `model.py`, `instances.py` | `data/instance_model.py`, `data/instance_loader.py` |
| `scheduler.py` | Núcleo estricto de `simulation/scheduler.py` |
| `baselines.py` | `algorithms/constructive_baselines.py` |
| `encoding.py` | Decodificación de `algorithms/mh.py` y `algorithms/gwo_eyeing_comparison.py`; codificación de `algorithms/gwo_tabu_comparison.py` |
| `objective.py` | Agregación de `algorithms/mh.py`, sin término de equilibrio |
| `bandit.py` | D-MAB de `algorithms/gwo_eyeing_comparison.py` |
| `tabu.py` | Movimientos y búsqueda de `algorithms/gwo_tabu_comparison.py` y `algorithms/tabu_candidate_selection.py` |

La copia exploratoria está separada del repositorio oficial del profesor. Se
comprobaron 24 corridas antiguas (4 tamaños × 3 semillas × 2 políticas): el
valor inicial, objetivo final, makespan y esperas total/máxima coincidieron
numéricamente con los CSV anteriores. El estudio nuevo se ejecuta con semillas
20–39 y contiene hashes del código para identificar la versión exacta.

Para reproducir desde la raíz del repositorio:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[test]'
.venv/bin/python -m pytest -q
.venv/bin/python -m experiments.run_study --seed-start 20 --seed-count 20
```

El script guarda `runs.csv` tras cada corrida y se puede reanudar con el
mismo comando. `manifest.json` rechaza cambios en semillas, configuración,
instancias o código al reanudar; tras completar genera resumen, diferencias
emparejadas, gráficos y análisis.

`runs.csv` conserva métricas, no el calendario final de cada corrida. Por
ello `experiments.verify_results` audita cobertura, presupuesto, hashes y
resúmenes, pero **no puede reconstruir `max_wait` desde el CSV**. La
factibilidad procede del planificador estricto en cada evaluación, de la
revalidación de la mejor solución antes de devolverla y de las pruebas que
comprueban una violación artificial y la reproducibilidad de una corrida.
Además, `experiments.audit_replay` vuelve a ejecutar la semilla 20 en las
doce instancias y tres políticas, compara objetivo, makespan y bloqueo con
`runs.csv`, y reconstruye los 36 calendarios para verificar elegibilidad y
holgura no negativa frente a `max_wait`.
