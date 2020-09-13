---
layout: post_es
title:  Simular para aprender
category: general
tags: spanish simulation "computational model"
---
No hay nada que me guste más que aprender cosas nuevas. Me mantiene activo y despierto. Y cuando digo cosas
nuevas hablo de cosas realmente nuevas. Nunca le había prestado demasiada atención a la dinámica de las
epidemias y este año tuve razones para hacerlo. En Argentina ya venía siguiendo de cerca lo que pasaba con
el brote de *Dengue* cuando los primeros casos de *COVID-19* se confirmaron.  


En seguida los diarios empezaron a llenarse de noticias y cientos de expertos hablaban de qué había que hacer.
Lo hacían como si todo estuviera desconectado. Los economistas hablaban de cuidar la economía y los infectólogos
hablaban como si fuera posible tener a la gente encerrada en la casa 60 días. Por supuesto rápidamente cambié
los diarios por otras fuentes de información. Hoy es posible tener acceso a las personas casi directamente así
que empecé a seguir en *twitter* a algunas personas que me ayudaron a enterarme más rápido de algunas cosas.  
Pero el futuro todavía no existe. Y cuando las cosas son dinámicas y las reacciones de la gente, las
sociedades y los gobiernos interactúan con un virus permanentemente vaya uno a saber cómo será.  


Por eso complementé mis lecturas sobre *SARS-CoV-2*, *COVID-19* y actualidad con un modelo de simulación que
me permitió hacerme preguntas y estudiar cómo podía cambiar el curso de una epidemia virtual según qué medidas
tomaran los gobiernos y los individuos de una población. Aprendí un montón de cosas sobre el problema y me 
sorprendí un montón de veces.  


<img class="red" src="/SETM/assets/img/2020-09-12-Simular-para-aprender.png" />
> Para poder leer rápido los resultados trabajé mucho en los gráficos automáticos que se crean después
de cada simulación.

Dije que me gusta aprender cosas nuevas así que escribí el modelo en [Python](https://www.python.org). Un
lenguaje de programación en el que no había escrito más que unas pocas líneas de código. El objetivo siempre
fue que el modelo sirviera para estudiar un problema dinámico así que lo diseñé de una manera que me permitió
ir introduciendo muchos cambios. Mientras que para las primeras simulaciones podía únicamente reducir la 
circulación de la población durante cierto período hoy es posible simular cosas como un aumento del cuidado
de la población en respuesta al brote o el rastreo y aislamiento de *contactos estrechos* de *casos confirmados*.  


En las próximas semanas intentaré ir desarrollando una documentación completa para que las personas curiosas
como yo puedan correr simulaciones o interpretar los resultados sin necesidad de estudiar todo el código. Y
quizás descubrir algo que hasta ahora a mí se me escapó.