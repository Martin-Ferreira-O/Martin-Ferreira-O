# Widgets del perfil

Las tarjetas se generan con datos reales de la API de GitHub. Los SVG y su
snapshot JSON viven en `assets/widgets/`, de modo que el perfil conserva su
última versión aunque una consulta posterior falle. No dependen de un servidor
de estadísticas externo.

- **Resumen:** cantidad de repositorios públicos propios, estrellas recibidas en
  ellos y lenguajes detectados en su código. Se excluyen los forks.
- **Lenguajes:** proporción de bytes de código agregados, no nivel de dominio ni
  porcentaje de tiempo de trabajo. Los lenguajes restantes se agrupan en Otros.
- **Privacidad:** el generador consulta exclusivamente endpoints públicos. No
  accede a Psycode ni a ningún otro repositorio privado.

El workflow `Refresh profile widgets` los actualiza a diario y permite una
ejecución manual desde Actions. Comenzará a funcionar cuando estos archivos
estén en `main` en GitHub y Actions esté habilitado. Usa el `GITHUB_TOKEN`
automático del repositorio; no requiere un token personal ni secretos nuevos.
Si hay reglas que impidan los commits automáticos a `main`, habrá que adaptar el
paso de publicación a esas reglas.

Para actualizar localmente, con Python 3.12 o posterior:

```sh
python3 -m unittest discover -s tests
python3 scripts/profile_widgets.py
```

Si la instalación local de Python no encuentra los certificados raíz del sistema,
configura su almacén de certificados; no desactives la verificación TLS.

GitHub puede retrasar ejecuciones programadas y deshabilitarlas tras 60 días sin
actividad en un repositorio público. Ver [eventos programados](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).

La tira de iconos identifica tecnologías utilizadas en los proyectos y procede
de [Skill Icons](https://github.com/tandpfun/skill-icons). No representa certificaciones.
