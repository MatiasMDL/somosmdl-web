---
title: "Meta cambió cómo cuenta los resultados de tus anuncios: por qué pueden subir los números sin que vendas más"
description: "Desde el 12 de noviembre el píxel de Meta mide compras en el dispositivo del cliente y ThruPlay ya puede contar desde 6 segundos. Qué revisar en tu cuenta."
date: 2026-11-18
category: Publicidad digital
service: /servicios/meta-ads/
tldr: "Desde el 12 de noviembre de 2026 el píxel de Meta tiene activada por defecto una función que mide algunas compras en el celular o la computadora del cliente, y en noviembre apareció la opción de contar un ThruPlay desde los 6 segundos de video en lugar de 15. Las dos cosas pueden hacer que tus reportes muestren más resultados sin que cambien tus ventas, así que conviene comparar siempre con lo que entra de verdad a la caja."
portada:
  frase: "Más resultados en el reporte no es más ventas"
  escena: "Compras en el sitio web: subieron esta semana"
  motivo: anuncio
figuras:
  - tipo: comparacion
    titulo: "Lo que cambió en noviembre en Meta"
    columnas: ["Qué cambió", "Qué significa para tu reporte"]
    filas:
      - ["El píxel mide compras también en el dispositivo del cliente", "Pueden aparecer compras que antes Meta no veía"]
      - ["Viene activado por defecto desde el 12 de noviembre", "Si no hiciste nada, ya está prendido"]
      - ["ThruPlay se puede contar desde 6 segundos", "Más reproducciones contadas con el mismo video"]
      - ["La ventana y el modelo de atribución no cambian", "Lo que cambia es cuánto ve Meta, no cómo reparte el crédito"]
  - tipo: dato
    dato: "6 vs 15"
    texto: "segundos: el nuevo mínimo para contar un ThruPlay en Meta, contra el estándar de siempre, que sigue siendo la opción por defecto."
    fuente: "Administrador de anuncios de Meta, vía PPC Land, 16 de noviembre de 2026"
  - tipo: pasos
    titulo: "Cómo revisar la configuración de tu píxel"
    pasos:
      - "Entrá al Administrador de eventos de Meta"
      - "Abrí Orígenes de datos y elegí tu píxel"
      - "En Configuración, buscá Medir conversiones en los dispositivos de los clientes"
      - "Anotá si está prendido y desde qué fecha"
      - "Compará cada semana las compras de Meta con tus ventas reales"
sources:
  - title: "Meta Pixel will count more conversions from Nov 12 unless advertisers opt out (PPC Land)"
    url: https://ppc.land/meta-pixel-will-count-more-conversions-from-nov-12-unless-advertisers-opt-out/
  - title: "Meta Measure Conversions on Customer Devices: What to Check (MetricMaven)"
    url: https://www.metricmaven.io/blog/meta-measure-conversions-on-customer-devices
  - title: "What changes in the Meta Pixel on November 12? (Clakta)"
    url: https://www.clakta.com/blog/meta-pixel-on-device-conversions-november-12
  - title: "Six seconds can now count as a watched video ad on Meta (PPC Land)"
    url: https://ppc.land/six-seconds-can-now-count-as-a-watched-video-ad-on-meta/
---

Sí, en noviembre Meta cambió dos cosas en la forma de contar los resultados de tus anuncios. Desde el 12 de noviembre de 2026, el píxel tiene activada por defecto una función que mide algunas compras en el celular o la computadora del cliente, además de en los servidores de Meta. Y en el Administrador de anuncios apareció la opción de contar un ThruPlay desde los 6 segundos de video, en lugar de 15. Las dos pueden hacer que tus reportes muestren más resultados aunque tus ventas sean las mismas. Por eso, justo antes de fin de año, conviene revisar la configuración y medir contra tus ventas reales.

## ¿Qué cambió en el píxel de Meta?

El píxel es el código que Meta pone en tu web para saber qué hace la gente después de ver un anuncio: si entró, si agregó algo al carrito, si compró. Una parte de esas compras nunca le llega a Meta, por bloqueos del navegador, por privacidad o porque la persona cambió de dispositivo.

La nueva función se llama "Medir conversiones en los dispositivos de los clientes". Según el texto que muestra Meta en el panel del píxel, con la función activada "la medición ocurre en el dispositivo de tu cliente en lugar de exclusivamente en los servidores de Meta". Según la ayuda de Meta que citan MetricMaven y Clakta, la coincidencia se hace con datos que el cliente ya le dio al negocio, como el mail, más datos temporales del dispositivo que no lo identifican. Meta recibe solo la confirmación de que hubo una compra y qué campaña se lleva el crédito.

![Comparación: lo que cambió en noviembre en Meta y qué significa para tu reporte](/img/blog/meta-cambia-como-cuenta-resultados-1.jpg "Los dos cambios suman resultados al reporte. Ninguno suma ventas por sí solo.")

Tres datos importantes:

- **Viene prendida por defecto** en los píxeles que ya envían eventos. Si no tocaste nada, está activada.
- **No se aplica en la Unión Europea ni en el Reino Unido**, así que en Argentina sí corre.
- **La ventana y el modelo de atribución no cambian**, según Meta. Lo que cambia es cuántas compras puede ver, no cómo reparte el crédito entre anuncios.

## ¿Le pasa a cualquier web?

No. Según la ayuda de Meta citada por MetricMaven y Clakta, la función solo trabaja si se cumplen dos condiciones técnicas:

| Condición | Qué significa en la práctica |
| --- | --- |
| El píxel está instalado directo en la página | No sirve si está dentro de un iframe o como píxel de imagen |
| La web pide iniciar sesión con mail o celular | Las tiendas donde se compra sin cuenta pueden quedar afuera |

Muchas tiendas de pymes dejan comprar sin crear una cuenta. En esos casos, Meta no aclaró qué pasa, y el efecto puede ser chico o nulo. Si tu web pide registrarse para comprar, es más probable que notes el cambio.

## ¿Qué cambió con los videos?

ThruPlay es la forma en que Meta cuenta que alguien miró tu video: hasta ahora, 15 segundos o el video completo si dura menos. Según una captura del Administrador de anuncios que publicó PPC Land el 16 de noviembre, las campañas de reconocimiento e interacción que optimizan por ThruPlay ahora tienen un campo nuevo para elegir el mínimo: 6 o 15 segundos. Meta lo presenta como ideal para videos cortos, como reels e historias.

![Dato: 6 segundos contra 15 para contar un ThruPlay](/img/blog/meta-cambia-como-cuenta-resultados-2.jpg "Quince segundos sigue siendo la opción por defecto.")

El detalle es matemático. Toda persona que mira 15 segundos ya pasó los 6. Entonces, con la opción de 6 segundos, el número de ThruPlays siempre va a ser igual o mayor, y el costo por ThruPlay igual o menor. No es que el video funcione mejor: es que la vara está más baja. Comparar una campaña de 6 segundos con una de 15 es comparar dos cosas distintas.

> Si el reporte cambia la forma de contar, el número sube aunque el negocio venda lo mismo.

## ¿Es bueno o malo para tu negocio?

Ninguna de las dos cosas, por sí sola. Que Meta vea compras que antes se le escapaban puede ayudar a que el sistema entienda mejor qué anuncios funcionan. Y un video de 6 segundos bien hecho puede ser justo lo que necesita una marca para que la recuerden.

El riesgo está en leer mal los números. Si en noviembre ves más compras en Meta y pensás que la campaña mejoró, podés subir el presupuesto de algo que en realidad rinde igual que antes. Y eso pasa en el peor momento, cuando se arman las campañas de fin de año. Meta tampoco informó si estas compras nuevas se usan para optimizar las campañas o solo aparecen en los reportes.

## ¿Qué conviene hacer ahora?

![Pasos para revisar la configuración del píxel de Meta](/img/blog/meta-cambia-como-cuenta-resultados-3.jpg "Una revisión de diez minutos para leer bien los reportes de diciembre.")

1. **Revisá el píxel.** En el Administrador de eventos, entrá a Orígenes de datos, elegí tu píxel y abrí la configuración. Ahí está el interruptor de la nueva función. Anotá si está prendido.
2. **Marcá la fecha.** Escribí en tu planilla de resultados que desde el 12 de noviembre Meta mide distinto. Así, cuando compares diciembre con octubre, sabés que no es la misma regla.
3. **Compará con tus ventas reales.** Cada semana, poné lado a lado las compras que muestra Meta y los pedidos que entraron de verdad, en tu tienda, tu sistema o tu WhatsApp. Si la proporción cambia de golpe, es la medición, no el negocio.
4. **Elegí bien la duración del video.** Si tu campaña busca que la gente vea un mensaje completo, dejá 15 segundos. Si usás videos cortos para que te conozcan, probá con 6, pero no lo compares con campañas viejas.
5. **No cambies todo junto.** Si tocás el píxel, el presupuesto y los anuncios la misma semana, después no vas a saber qué funcionó.

Si vendés por WhatsApp, esta parte te afecta menos: lo que cuenta es la conversación y cuántas terminan en venta. Ese número lo tenés vos, no Meta.

## En resumen

Desde noviembre Meta mide más compras y puede contar más reproducciones de video. Eso puede hacer que tus reportes se vean mejor sin que vendas más. Revisá la configuración del píxel, anotá la fecha del cambio y medí siempre contra tus ventas reales. Si querés que revisemos juntos tus campañas de fin de año y cómo se están midiendo, escribinos.
