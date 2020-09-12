---
layout: index
title:  SETM
---
A principios de 2020 finalmente me decidí a escribir código en [Python](https://www.python.org). No tenía
nada especial para hacer hasta que el *SARS-CoV-2* logró alcanzar todos los rincones del planeta. Así que
me propuse programar un par de modelos sencillos para simular no sólo la evolución de una epidemia en una
población sino también los efectos de distintas medidas de contingencia que las autoridades sanitarias de
un país pueden tomar.  
El proyecto se llama **SETM** (**S**imple **E**pidemic **T**ransmission **M**odels). Hablé de un par de
modelos porque me propuse diseñar dos. Uno para simular epidemias de enfermedades que se transmiten entre
personas (inspirado especialmente en la epidemia de *COVID-19*) y otro para simular enfermedades que
se transmiten a través de un vector (inspirado en el *Dengue*).  
Para correr tus propias simulaciones necesitás *Python3* y las librerías *Pandas* y *Matplotlib*. Podés
contactarme por [mail](mailto:rodrigovalla@protonmail.ch) o encontrarme en [telegram](https://t.me/rvalla)
y <a rel="me" href="https://fosstodon.org/@rvalla">mastodon</a>. Si querés saber quién soy podés leer
[acá](https://rvalla.github.io/es/aboutme_es/). 

<p></p>
<hr class="red" />
<hr class="green" />
<hr class="blue" />

### Modelo Humano > Humano

El modelo es sencillo. Existe una población de *humanos* dividida en dos *ciudades*. Los *humanos infectados*
cada *día* entran en contacto con otros *humanos*. Una serie de cálculos decide si se contagian o no. El *virus*
tiene sus propias características y define entre otras cosas un *tiempo de incubación* y un *tiempo total de
duración*. También cuán frecuente es que los *humanos* presenten *síntomas* y cuánto depende de éstos la
probabilidad de que un *humano* contagie a otro. También existen variables que representan por ejemplo *cuán
cuidadosos* son los *humanos* o el *distanciamiento social*.  
El *gobierno* puede tomar distintas medidas para intentar frenar el brote. Estas medidas se disparan a partir
del *número de casos conocido* y no del *número real de casos*. Estos dos números pueden parecerse más o menos
según cuán efectivo sea el *testeo*. El *gobierno* puede aislar *casos confirmados*, buscar *contactos
estrechos*, puede reducir la circulación o detener el intercambio de *humanos* entre las *ciudades*.  
Después de cada *simulación* todos los datos tanto de la *configuración* como de la *población*, las *infecciones*
y la *evolución del brote* son guardados en la carpeta
[/SimulationData](https://github.com/rvalla/SETM/tree/master/HumanToHumanModel/SimulationData). También se
guardan automáticamente una serie de gráficos en la carpeta
[/SimulationPlots](https://github.com/rvalla/SETM/tree/master/HumanToHumanModel/SimulationPlots) para
visualizar los resultados rápidamente.  

#### Para seguir leyendo (en preparación):

Por supuesto fui cambiando cosas del modelo con el tiempo. Mejorando mucho los gráficos automáticos
e introduciendo varios cambios en el algoritmo (algunas veces para corregir errores o para guardar datos a los
que no les estaba prestando atención). Aprendí mucho mientras lo diseñaba y también con sus resultados. Si
bien se trata de un modelo sencillo creo que puede ayudar a pensar en el *problema* siempre y cuando se
interpreten con cuidado sus resultados.  
Compartiré los resultados que me sorprendan y algunas ideas sobre su implementación en el
[blog](https://rvalla.github.io/SETM/es/blog_es), aunque no me comprometo a publicar contenido con frecuencia.
Si te da curiosidad saber qué pasa con una *epidemia simulada* cuando se aplican cuarentenas o aislamientos
podés leer [Respuestas desde el futuro](https://rvalla.github.io/blog/2020/Respuestas_desde_el_futuro/).  
Pronto podrás conocer más detalles sobre el modelo y cómo funciona (siempre podés ir directo al
[código](https://github.com/rvalla/SETM)):

- ¿Cómo correr simulaciones?
- ¿Cómo leer los resultados?
- Sobre la estructura del programa
- Sobre el algoritmo
- Sobre el peligro de extrapolar

<p></p>
<hr class="red" />
<hr class="green" />
<hr class="blue" />

### Modelo Humano > Vector > Humano

Sucesivas mejores en el modelo *Humano>Humano* han hecho que todavía no haya avanzado con el modelo inspirado
en el *Dengue*. Seguramente lo haga el en futuro. El *mosquito* tiene características distintas al *humano* y
en el caso del género *Aedes* no suelen viajar mucho por la ciudad. Así que el problema a resolver es distinto.  
Mientras que modelar las poblaciones de *humanos* de manera estática (sin natalidad ni mortalidad ajena a la
enfermedad simulada) es aceptable los *mosquitos* tienen ciclos completamente distintos.  