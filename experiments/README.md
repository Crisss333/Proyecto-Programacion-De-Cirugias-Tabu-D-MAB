# Experimentos reproducibles

## Validación principal (versión 2)

```bash
python -m experiments.calibrate --workers 2        # opcional: semillas 0–5
python -m experiments.run_study --seed-start 40 --seed-count 20
python -m experiments.verify_results
python -m experiments.analyze_ablation
python -m experiments.finalize_analysis
python -m experiments.plot_paired_differences
python -m experiments.plot_convergence --seed 40
python -m experiments.audit_replay --seed 40
```

El primer comando ejecuta `uniform`, `dmab` y `ucb` en las 12 instancias
estándar con las mismas veinte semillas nuevas (40–59), presupuesto de 3.030
evaluaciones y objetivo sin balance. Calcula asimismo FIFO, SPT y LPT.
Guarda inmediatamente cada fila de `runs.csv`; con los mismos argumentos el
proceso se reanuda si se interrumpe. El segundo comando audita el manifiesto,
los hashes, la matriz completa de instancia × semilla × política, el mismo
valor inicial y las 3.030 evaluaciones factibles por corrida.

`experiments.calibrate` fija C y λ de D-MAB usando solo las semillas
exploratorias 0–5; su resultado está en
[`results/calibration_0_5/CALIBRATION.md`](results/calibration_0_5/CALIBRATION.md).

El directorio [`results/validation_40_59/`](results/validation_40_59/) contiene:

- `manifest.json`: protocolo, entorno, parámetros y hashes de datos/código.
- `baselines.csv`: calidad de FIFO, SPT y LPT por instancia.
- `runs.csv`: métricas y selección de operadores en cada corrida.
- `summary.csv`: medianas, mínimo y máximo por instancia y política.
- `paired.csv`: diferencias por instancia entre alternativas y Tabu mixto.
- `statistics.csv`: pruebas de Wilcoxon emparejadas y p-valores con Holm
  (familia global y familia por instancia).
- `comparison.png`/`.pdf`: medianas por tamaño y réplica.
- `ANALYSIS.md`: tabla y lectura descriptiva, sin afirmar optimalidad.
- `ABLATION.md` y `ablation_dmab_vs_ucb.csv`: comparación directa entre
  D-MAB y UCB1 sin Page–Hinkley.
- `paired_differences.png`: las 20 diferencias emparejadas por instancia
  respecto de Tabu mixto, con mediana y rango intercuartílico.
- `convergence.png` y `convergence_trace.csv`: ejemplo descriptivo de las
  curvas para semilla 40 y réplica 01 de cada tamaño. Las conclusiones usan
  todas las instancias y semillas, no solamente estas cuatro curvas.
- `replay_seed_40.csv`: 36 soluciones recalculadas; verifica valores contra
  `runs.csv` y reconstruye el calendario estricto para comprobar `max_wait`.

La validación de la Entrega 1 (semillas 20–39, C = 1, λ = 0,35) queda
archivada en [`results/validation_20_39/`](results/validation_20_39/README.md).

El [archivo exploratorio de semillas 0–19](results/exploratory_0_19/README.md)
documenta las pruebas previas que motivaron esta arquitectura. Esos datos no
se incluyen en la validación nueva. La formulación completa de métricas,
restricciones y ablation está en
[`docs/metodologia-experimental.md`](../docs/metodologia-experimental.md).
