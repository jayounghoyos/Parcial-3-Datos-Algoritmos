# Parcial-3-Datos-Algoritmos

## Integrantes
- Juan Andrés Young Hoyos
- Joseph Saldarriaga
- Sofia Flores Suárez

## Scheme
[Propuesta de Solución](PropuestaDesolucion2D.pdf)

## Preguntas asociadas al problema

Responda a las siguientes preguntas y adjunte a la propuesta de solución:

1. **Lectura del dataset**
    - Lectura por medio de pandas 'read_csv'

2. **Para cada clase, presente los métodos más importantes.**
    - Clase `Linked List`: `append`, `prepend`, `to_list`.
    - Clase `Nodo`.

3. **Creación del grafo**
    - Cada nodo en el grafo representa a un actor o director
    - Un enlace(arista) entre dos nodos existe si los dos individuos han trabajado juntos en al menos una
película.
    - Otra idea es crear una pila de los que están los más próximos a vencer.

4. **Almacenamiento de Datos**
    - Utilice listas enlazadas para almacenar los actores y directores que han trabajado en cada película. Esto
incluye almacenar, para cada película, una lista enlazada de actores y el director asociado.

5. **Búsqueda en el Grafo**
    - Implemente una función de búsqueda en amplitud (BFS) para encontrar el camino más corto de colaboración entre dos actores, mostrando todos los intermediarios y películas que los conectan.
    - Implemente una función de búsqueda en profundidad (DFS) para explorar todas las colaboraciones posibles de un actor o director dado, mostrando los caminos posibles de colaboración extendida.