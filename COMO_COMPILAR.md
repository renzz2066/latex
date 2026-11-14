# Cómo compilar este proyecto LaTeX

Guía rápida para dejar el entorno funcionando en Windows y compilar `main.tex`.

## 1. Instalar MiKTeX (el motor de LaTeX)

1. Descargar desde https://miktex.org/download (instalador de 64-bit para Windows).
2. Instalar con las opciones por defecto.
3. Importante — activar la instalación automática de paquetes que falten:
   - Abrir PowerShell y ejecutar:
     ```
     initexmf --set-config-value [MPM]AutoInstall=1
     ```
   - Esto evita que la compilación se trabe pidiendo paquetes como `geometry.sty` uno por uno.

## 2. Instalar Perl (lo necesita `latexmk`)

La extensión de VS Code compila usando `latexmk`, que es un script en Perl. Sin Perl, el botón de compilar no hace nada (falla en silencio).

- Instalar **Strawberry Perl**: https://strawberryperl.com (o con `winget install StrawberryPerl.StrawberryPerl` desde PowerShell).
- Reiniciar VS Code después de instalarlo para que tome el PATH nuevo.

## 3. Extensión de VS Code

Instalar **LaTeX Workshop** (autor: James Yu) desde el Marketplace de VS Code.

## 4. Compilar

1. Abrir `main.tex` en VS Code.
2. Apretar el ícono ▶ verde arriba a la derecha del editor, o el atajo `Ctrl+Alt+B`.
3. El PDF se abre solo en una pestaña al lado (o `Ctrl+Alt+V` para verlo).

El proceso automático hace: `pdflatex` → `biber` (procesa `referencias.bib`) → `pdflatex` × 2 (para que citas y referencias cruzadas queden bien). Latexmk se encarga de encadenar todo esto solo.

## Problemas comunes

- **"File `xxx.sty` not found"**: falta activar el AutoInstall del paso 1, o ejecutar manualmente `miktex packages install <nombre-paquete>`.
- **El botón ▶ no hace nada / no pasa nada**: casi siempre es que falta Perl (paso 2). Revisar la pestaña "Output" → "LaTeX Compiler" en VS Code para ver el error real.
- **Citas aparecen como "?"**: correr la compilación de nuevo (a veces hace falta una pasada extra para que `biber` y las referencias cruzadas se asienten; el botón ▶ ya hace esto automáticamente).

## Archivos del proyecto

- `main.tex` — documento principal.
- `referencias.bib` — bibliografía (biblatex/biber).
- `imagenes/` — imágenes usadas en el documento.
- `main.pdf` — último PDF compilado (se regenera al compilar, no hace falta tocarlo a mano).


## comando para borrar los archivos de ejcucion si queremos exportar solo la tesis:

Remove-Item main.aux,main.bbl,main.bcf,main.blg,main.fdb_latexmk,main.fls,main.lof,main.log,main.lot,main.out,main.run.xml,main.synctex.gz,main.toc -ErrorAction SilentlyContinue

en PS desde la ruta del proyecto