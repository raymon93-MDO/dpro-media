# Playbook de redes · DPRO · Proyectos & Obras

Guía para gestionar las publicaciones semanales de DPRO en Instagram y Facebook.

## Cuentas (conector Windsor.ai for Social Media)

| Red | Cuenta | ID en Windsor |
|---|---|---|
| Instagram | @dpro_proyectos_obras | 17841477275519628 |
| Facebook | Página "DPRO · Proyectos & Obras" | 1358249884048379 |

- Instagram: `create_carousel_post` (2–10 JPEG, 4:5) o `create_image_post`.
- Facebook (Página "DPRO · Proyectos & Obras", 1358249884048379): **sí publicar siempre por Windsor** con `create_photo_post` (portada + texto completo), además de Instagram. El compartido automático que configuró Chapa va desde Instagram a la cuenta de Facebook vinculada (perfil "Dpro Proyectos Obras"), no a esta Página.
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

- **Estilo vigente (desde 10/11/2026): render fotorrealista + láminas técnicas.** Portada con render generado en Gemini (cuenta de Chapa, vía Claude in Chrome, prompts en `renders/prompts_gemini.md`), luego planta, vista 3D (si existe en `generador/iso.py`) y ficha. Se arma con `python3 generador/slides4.py <modelo> renders/<modelo>_render.jpg <salida>`.
- Revisar cada render antes de usarlo: mismo número de plantas y mismos materiales que el modelo. Si Gemini se equivoca, pedirle que regenere con la corrección.
- La portada dice "Render ilustrativo". Los renders no son fotos de obras construidas.
- Plantilla minimalista para láminas sin render: `generador/slides3.py` (fondo claro, tipografía fina, acento naranja #F07A1D).
- Modelos de vivienda en `generador/models.py` (verificar que los m² sumen con `python3 models.py`).
- Texto en "vos", corto, con datos concretos y cierre **"Escribí PLANO por WhatsApp"**.
- No publicar precios salvo que Chapa los valide con el listado CAPACO vigente.
- Solo diseños originales de DPRO; nunca imágenes de terceros.

## Calendario

- Lunes, miércoles y viernes a las 19:00 (America/Asuncion).
- Planilla de calendario: https://claude.ai/artifact/M7NHuQ9XjtEJyfKtXFiSG3 (hoja "Calendario", actualizada al 16/11 con lo publicado, lo programado, el Reel del martes 24/11 como "Pendiente Gemini" y el banco de ideas). Mantenerla al día en cada cambio de estado.
- Ritmo: carruseles lun/mié/vie + Reel los martes, todo a las 19:00.
- Semana 16–20/11 (aprobada y programada). Semana 23–27/11: lunes "Cómo leer un plano" y viernes "Casa por etapas" aprobados y programados como prueba (Chapa decide después si sigue el formato educativo); el miércoles 25 va con novedades frescas. Antes: Quinta Lapacho (`posts/2026-11-16-quinta-lapacho/`), Novedades BCP (`posts/2026-11-18-novedades-construccion/`), Tormentas (`posts/2026-11-20-casa-tormentas/`). `posts/proximos/` quedó vacío: los 4 modelos ya tienen carrusel. Láminas informativas: `python3 generador/info.py <sector|tormentas> <salida>`.
- Textos de los modelos: `posts/textos_publicaciones.md`.

## Reels (1 por semana, desde 16/11/2026)

- Decisión de Chapa (16/11): mantener el ritmo de carruseles (lun/mié/vie) y sumar **un Reel por semana**, en un día sin carrusel (martes, 19:00).
- **Decisión de Chapa (16/11): el Reel lo genera Gemini, bien profesional (video animado), no el montaje de la nube.** Los montajes `posts/2026-11-17-reel-lapacho/` y `posts/2026-11-24-reel-nanduti/` quedan como borrador y **no se publican**. Se necesita la compu de Chapa conectada con Claude in Chrome. Pedirle a Gemini un video 9:16 de 15–20 s a partir del render del modelo: recorrido de cámara suave, mismas plantas y materiales, sin personas ni texto. Revisarlo, sumar la leyenda "Render ilustrativo" y el cierre "Escribí PLANO", mostrárselo a Chapa y publicarlo solo con su OK.
- **Reel Quinta Lapacho (Gemini) aprobado por Chapa el 16/11:** `posts/2026-11-17-reel-lapacho-gemini/` (2 clips de Gemini unidos con `python3 generador/reel_gemini.py <clip1.mp4> <clip2.mp4> "<KICKER>" "<título>" "<bajada>" <salida.mp4>`: 18,8 s, leyenda "Render ilustrativo", cierre "Escribí PLANO", audio ambiente de Gemini). Programado para el martes 17/11 a las 19:00.
- Borrador alternativo (solo si Chapa lo pide): `python3 generador/reel.py <render.jpg> <lamina_planta.jpg> <lamina_ficha.jpg> "<KICKER>" "<título 1>" "<título 2>" "<bajada>" <salida.mp4>`: 9:16, 1080x1920, unos 19 s, paneo sobre el render de Gemini + planta + ficha + cierre "Escribí PLANO". Sin música (sin riesgo de derechos). Portada: el frame de 0,5 s exportado como JPEG.
- Renders nuevos de Gemini (o un video animado de Gemini) solo se pueden pedir cuando la compu de Chapa está conectada con Claude in Chrome (prompts en `renders/prompts_gemini.md`).
- Publicación: Instagram `create_video_post` con `cover_url`. **raw.githubusercontent.com sirve el MP4 como application/octet-stream**, así que el video se publica desde jsDelivr fijado al commit: `https://cdn.jsdelivr.net/gh/raymon93-MDO/dpro-media@<commit>/posts/<carpeta>/<video>.mp4` (verificado: 200 y video/mp4). En la Página de Facebook: `create_photo_post` con la portada y el texto (Windsor no publica videos en la Página).
- Motivo: en el informe del 06–12/11 los carruseles solo llegaron a seguidores (alcance 15 y 12). El Reel es el formato que Instagram muestra a quienes no te siguen.

## Registro de publicaciones

| Fecha | Post | Instagram | Facebook |
|---|---|---|---|
| 2026-11-10 | Casa Brisa 58 (carrusel moderno) | https://www.instagram.com/p/DfkdgstDfpu/ | Post 1358249884048379_122093166489555754 |
| 2026-11-11 | Casa Ñandutí 92 (carrusel con render) | https://www.instagram.com/p/DfngZj0EU8Y/ | Post 1358249884048379_122093891493555754 |
| 2026-11-13 | Dúplex Dúo 70 (carrusel con render) | https://www.instagram.com/p/Dfsp9pakVkn/ | Post 1358249884048379_122095073577555754 |
| 2026-11-16 | Quinta Lapacho (carrusel con render) | https://www.instagram.com/p/Df0YXbGEYNl/ | Post 1358249884048379_122097244545555754 |
| 2026-11-17 | Reel Quinta Lapacho (video Gemini) | https://www.instagram.com/reel/Df29H0-DOJ-/ | Post 1358249884048379_122097893775555754 (portada + texto) |
| 2026-11-18 | La construcción vuelve a empujar (novedades BCP, carrusel) | https://www.instagram.com/p/Df5iAsyDfVA/ | Post 1358249884048379_122098620291555754 |
| 2026-11-20 | Tu casa, lista para el temporal (educativo, carrusel con checklist) | https://www.instagram.com/p/Df-rkANDQ9r/ | Post 1358249884048379_122100236979555754 |
| 2026-11-23 | Cómo leer el plano de tu casa (educativo, carrusel) | https://www.instagram.com/p/DgGZ8rFiOni/ | Post 1358249884048379_122103078933555754 |
