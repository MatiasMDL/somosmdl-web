---
title: "Google, OpenAI y Microsoft acuerdan una señal para no entrenar IA con tu web: ¿te conviene usarla?"
description: "Una línea nueva en el robots.txt va a decirle a Google, OpenAI y Microsoft si pueden entrenar su IA con tu web. Qué es, cuándo llega y qué le conviene a una pyme."
date: 2026-11-02
category: Web y SEO
service: /servicios/seo-geo/
tldr: "El 30 de octubre de 2026 Google, OpenAI y Microsoft anunciaron que van a respetar una misma señal en el robots.txt para que una web diga si acepta que la usen para entrenar inteligencia artificial. No cambia tu posición en Google. Para la mayoría de las pymes, que quieren aparecer en las respuestas de la IA, lo recomendable es no activarla sin revisar antes qué más bloquea."
portada:
  frase: "Una línea para decidir qué hace la IA con tu web"
  escena: "robots.txt de tu web"
  motivo: buscador
figuras:
  - tipo: comparacion
    titulo: "Qué cubre la nueva señal y qué no"
    columnas: ["La cubre", "No la cubre"]
    filas:
      - ["Entrenar modelos de IA con tu contenido", "Tu posición en los resultados de Google"]
      - ["En Google, también las respuestas de Gemini que citan webs", "Las vistas creadas con IA y el Modo IA de Google"]
      - ["Google, OpenAI, Microsoft y Anthropic", "Las empresas que no se sumaron"]
  - tipo: dato
    dato: "2027"
    texto: "es el año en que Google y Microsoft van a empezar a respetar la señal. OpenAI habla de los próximos meses."
    fuente: "Google Search Central y Bing, 30 de octubre de 2026"
  - tipo: pasos
    titulo: "Cómo decidirlo en tu negocio"
    pasos:
      - "Preguntate si querés que la IA te mencione cuando alguien pregunta por tu rubro"
      - "Si la respuesta es sí, no actives la señal por ahora"
      - "Si tenés contenido propio que no querés ceder, protegé solo esas carpetas"
      - "Revisá tu robots.txt con quien maneja tu web antes de tocar nada"
sources:
  - title: "Supporting a shared AI training control for websites (Google Search Central)"
    url: https://developers.google.com/search/blog/2026/10/ai-training-control
  - title: "Google common crawlers: Google-Extended (Google)"
    url: https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended
  - title: "Machine-Readable Training Preference Signal, borrador en la IETF"
    url: https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/
  - title: "Google, Microsoft, OpenAI and Anthropic back one AI training opt-out (PPC Land)"
    url: https://ppc.land/google-microsoft-openai-and-anthropic-back-one-ai-training-opt-out/
---

El 30 de octubre de 2026 Google, OpenAI y Microsoft anunciaron que van a respetar una misma señal para que cualquier web pueda decir "no quiero que entrenen inteligencia artificial con mi contenido". Se escribe una sola vez en el archivo robots.txt y vale para todas. No cambia tu posición en los resultados de Google. Pero en el caso de Google tiene un efecto que conviene conocer antes de activarla: también te puede sacar de las respuestas de Gemini.

## ¿Qué se anunció?

Hasta ahora, si no querías que una empresa de IA usara tu web para entrenar sus modelos, tenías que bloquear a cada una por su nombre: Google-Extended para Google, GPTBot para OpenAI, y así con cada empresa. Era fácil olvidarse de alguna.

La propuesta nueva sale de un grupo de trabajo de la IETF, el organismo que define muchos estándares de internet. El borrador lo presentó Kevin Kelley, de Anthropic, y el mismo día Google, OpenAI y Microsoft publicaron que lo van a adoptar. Anthropic también dijo que empezó a implementarlo.

La idea es simple: una sola instrucción en el robots.txt que todas entienden. Se ve así:

    User-Agent: __usage_ai-training
    Disallow: /

La primera línea no nombra a un robot, nombra un uso: el entrenamiento de IA. La segunda dice que no lo aceptás en ninguna página. Si querés dejar alguna carpeta disponible, se agrega una línea de Allow con esa carpeta.

## ¿Cuándo empieza a funcionar?

![Dato: la señal empieza a respetarse en 2027](/img/blog/senal-comun-entrenamiento-ia-robots-txt-2.jpg "Por ahora es un anuncio. Las empresas van a empezar a leer la señal durante 2027.")

Todavía no. Google dice en su documentación que planea soportarla a comienzos de 2027. Microsoft la va a respetar desde el 1 de febrero de 2027. OpenAI habló de "los próximos meses", sin fecha. Y el borrador de la IETF todavía no es un estándar aprobado.

Es decir, tenés tiempo para decidir con calma.

## ¿Me baja en Google si la uso?

No. La señal habla del entrenamiento de modelos, no de la búsqueda. Tu posición en los resultados de Google y de Bing no cambia. Las vistas creadas con IA y el Modo IA de Google tampoco se rigen por esta señal: dependen de las reglas de siempre para Googlebot.

![Qué cubre la nueva señal de entrenamiento de IA y qué no](/img/blog/senal-comun-entrenamiento-ia-robots-txt-1.jpg "La señal no toca tu posición en Google. En el caso de Google, sí puede afectar las respuestas de Gemini.")

El detalle está en otro lado. Google aclaró que si una web usa la señal para no permitir el entrenamiento y no dice nada específico sobre Google-Extended, lo va a tomar como si hubiera bloqueado Google-Extended. Y Google-Extended no solo controla el entrenamiento: también decide si tu web puede aparecer citada en las respuestas de Gemini. En palabras de John Mueller, de Google, las webs que permiten Google-Extended son las que pueden aparecer en esas respuestas y recibir clics desde ahí.

> Bloquear el entrenamiento de IA en Google, hoy, también es bloquear que Gemini te recomiende.

Microsoft lo separó distinto: el entrenamiento por un lado y las respuestas de su IA por otro, con una preferencia aparte.

## ¿Qué le conviene a una pyme?

Depende de qué vendés, pero para la mayoría la respuesta es no activarla. Una pyme de servicios, un comercio o una industria quiere lo contrario: que cuando alguien le pregunte a una IA "¿quién hace mantenimiento de calderas en Escobar?", la respuesta te nombre a vos. Para eso las IA tienen que conocer tu web.

| Tu caso | Qué hacer |
| --- | --- |
| Querés que la IA te mencione y te recomiende | No actives la señal |
| Vendés contenido propio (cursos, informes, fotos) | Protegé solo esas carpetas |
| Medio o editorial que vive de su contenido | Analizalo con tiempo, caso por caso |

## ¿Qué hacer ahora?

![Pasos para decidir si usar la señal de entrenamiento de IA](/img/blog/senal-comun-entrenamiento-ia-robots-txt-3.jpg "La decisión depende de si querés aparecer en las respuestas de la IA.")

1. **Revisá tu robots.txt.** Está en tudominio.com/robots.txt. Fijate si alguien ya bloqueó a GPTBot, Google-Extended u otros robots de IA sin que lo sepas.
2. **Decidí qué querés.** Si tu objetivo es que te encuentren, no hace falta hacer nada.
3. **Si tenés algo que proteger, hacelo por carpeta.** Bloqueá solo esa parte, no toda la web.
4. **Anotá 2027 en la agenda.** Cuando las empresas empiecen a leer la señal, conviene revisar que todo siga como lo dejaste.

## En resumen

Es una buena noticia para quien quiere cuidar su contenido: por fin hay una sola forma de decirlo. Para una pyme que quiere más clientes, el riesgo es copiar la línea sin entender que en Google también te saca de las respuestas de Gemini. Si querés que revisemos cómo está configurada tu web para aparecer en Google y en las respuestas de la IA, escribinos y lo vemos juntos.
