# Playbook de redes · DPRO · Proyectos & Obras

Guía para gestionar las publicaciones semanales de DPRO en Instagram y Facebook.

## Cuentas (conector Windsor.ai for Social Media)

| Red | Cuenta | ID en Windsor |
|---|---|---|
| Instagram | @dpro_proyectos_obras | 17841477275519628 |
| Facebook | Página "DPRO · Proyectos & Obras" | 1358249884048379 |

- Instagram: `create_carousel_post` (2–10 JPEG, 4:5) o `create_image_post`.
- Facebook: **no publicar por Windsor**. Desde el 10/11/2026 Instagram comparte automáticamente cada publicación en la Página de Facebook vinculada (configurado por Chapa). Publicar también por `create_photo_post` duplicaría el post. Solo usar Facebook directo si Chapa lo pide para un contenido exclusivo de Facebook.
- TikTok: descartado por decisión de Chapa.

## Actualizaciones de obras (siempre)

Cada semana, antes de proponer contenido, buscar novedades del sector en Paraguay: obras y proyectos destacados (Revista Mandu'a: mandua.com.py/notas), noticias de construcción e inmobiliario (InfoNegocios InfoConstrucción / InfoMiCasa), tendencias de diseño contemporáneo y variaciones de precios (CAPACO: capaco.org.py/ceec). Usar esas novedades como tema de al menos un post o historia por semana, siempre en palabras propias y citando la fuente en el texto. Nunca reproducir fotos ni textos de terceros.

## Regla de oro

**Nada se publica sin el OK explícito de Chapa en la misma conversación.** Puede aprobar varios posts juntos ("ok" a la propuesta de la semana). Sin respuesta, no se publica.

## Alojamiento de imágenes

Instagram exige URLs públicas. Cada post va en `posts/AAAA-MM-<slug>/` como JPEG 1080x1350 y se publica desde:

`https://raw.githubusercontent.com/raymon93-MDO/dpro-media/main/posts/<carpeta>/<archivo>.jpg`

Verificar con `curl` que devuelva 200 e `image/jpeg` antes de publicar.

## Estilo

- Plantilla minimalista: `generador/slides3.py` (fondo claro, tipografía fina, acento naranja #F07A1D).
- Modelos de vivienda en `generador/models.py` (verificar que los m² sumen con `python3 models.py`).
- Texto en "vos", corto, con datos concretos y cierre **"Escribí PLANO por WhatsApp"**.
- No publicar precios salvo que Chapa los valide con el listado CAPACO vigente.
- Solo diseños originales de DPRO; nunca imágenes de terceros.

## Calendario

- Lunes, miércoles y viernes a las 19:00 (America/Asuncion).
- Planilla de calendario: https://claude.ai/artifact/M7NHuQ9XjtEJyfKtXFiSG3
- Listos para publicar (estilo minimalista): `posts/proximos/` → Ñandutí 92, Dúo 70, Quinta Lapacho.
- Textos de los modelos: `posts/textos_publicaciones.md`.

## Registro de publicaciones

| Fecha | Post | Instagram | Facebook |
|---|---|---|---|
| 2026-11-10 | Casa Brisa 58 (carrusel moderno) | https://www.instagram.com/p/DfkdgstDfpu/ | Post 1358249884048379_122093166489555754 |
