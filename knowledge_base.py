# knowledge_base.py

data_ml = {
    # =========================================================
    # REGRESIÓN (Predecir Valores Numéricos)
    # =========================================================
    
    "Lasso": [
        {
            "titulo": "🏠 1. Precio de Casas (Feature Selection)",
            "contexto": "Predecir el precio de una casa eliminando variables basura (como el color de la puerta).",
            "pasos": [
                "1. Importamos Lasso y Numpy.",
                "2. Creamos datos: [Metros2, Habitaciones, Color(1-10)].",
                "3. Entrenamos con un alpha (castigo) bajo.",
                "4. Lasso vuelve 0 el coeficiente del 'Color'."
            ],
            "codigo": """import numpy as np
from sklearn.linear_model import Lasso

# Datos: [Metros2, Habitaciones, Color(Ruido)]
X = np.array([
    [100, 2, 5], 
    [150, 3, 1], 
    [200, 4, 9], 
    [120, 2, 2]
])
y = np.array([200000, 300000, 400000, 240000])

# Alpha controla la severidad. 0.1 elimina ruido leve.
modelo = Lasso(alpha=0.1)
modelo.fit(X, y)

print("Predicción (180m2, 3hab, color 5):")
print(f"${modelo.predict([[180, 3, 5]])[0]:,.2f}")

print("Importancia de variables:", modelo.coef_)
# Nota cómo el último valor (Color) se acerca a 0""",
            
            "explicacion_codigo": "Definimos 'X' como nuestra matriz de características y 'y' como el precio objetivo. Al llamar a .coef_, vemos qué peso le dio el modelo a cada columna.",
            "quiz": {
                "pregunta": "¿Qué hace Lasso con las variables irrelevantes?",
                "opciones": ["Las multiplica por 10", "Reduce su peso a CERO", "Da un error"],
                "correcta": "Reduce su peso a CERO",
                "retro_acierto": "¡Exacto! Lasso limpia tus datos eliminando lo que no sirve.",
                "retro_fallo": "Incorrecto. Lasso se caracteriza por 'borrar' variables (peso cero), no por multiplicarlas ni fallar."
            },
            "versus": {
                "rival": "Ridge Regression",
                "comparacion": "Lasso ELIMINA variables (coeficiente 0). Ridge solo las hace muy pequeñas, pero las mantiene todas."
            }
        },
        {
            "titulo": "🌾 2. Rendimiento de Cultivos",
            "contexto": "Predecir toneladas de cosecha ignorando mitos (fase lunar).",
            "pasos": [
                "1. Datos: Lluvia, Fertilizante, Fase Lunar.", 
                "2. Lasso detecta que la Luna no afecta.", 
                "3. Predice cosecha basada solo en lo real."
            ],
            "codigo": """import numpy as np
from sklearn.linear_model import Lasso

# Datos: [Lluvia(mm), Fertilizante(kg), FaseLunar(0-1)]
X = np.array([
    [100, 50, 1], 
    [200, 60, 0], 
    [50, 20, 1], 
    [300, 80, 0]
])
y = np.array([10, 25, 5, 35]) # Toneladas

modelo = Lasso(alpha=0.1)
modelo.fit(X, y)

# Predecir con mucha lluvia (150mm) y abono (55kg)
pred = modelo.predict([[150, 55, 1]])
print(f"Cosecha estimada: {pred[0]:.2f} toneladas")""",
            
            "explicacion_codigo": "Aunque le pasamos el dato de la fase lunar (el 1 al final), el modelo matemático aprende a ignorarlo para calcular las toneladas.",
            "quiz": {
                "pregunta": "¿Por qué usar Lasso y no Regresión Lineal aquí?",
                "opciones": ["Para ignorar el ruido", "Es más rápido", "Es más bonito"],
                "correcta": "Para ignorar el ruido",
                "retro_acierto": "¡Correcto! La regresión normal intentaría usar la fase lunar, cometiendo errores.",
                "retro_fallo": "No es eso. La clave de este ejemplo es que tenemos datos basura (ruido) que queremos ignorar."
            },
            "versus": {
                "rival": "Linear Regression",
                "comparacion": "La regresión simple se confunde fácil con datos basura. Lasso es inmune al ruido."
            }
        },
        {
            "titulo": "🚗 3. Valor de Autos Usados",
            "contexto": "Estimar precio ignorando accesorios estéticos sin valor.",
            "pasos": ["1. Variables: Km, Año, Calcomanías.", "2. Lasso ignora las calcomanías.", "3. Predice precio."],
            "codigo": """import numpy as np
from sklearn.linear_model import Lasso

# [Km, Año, Calcomanías(1=Sí/0=No)]
X = np.array([
    [50000, 2015, 1], 
    [10000, 2020, 0], 
    [80000, 2012, 1]
])
y = np.array([15000, 25000, 8000]) # Precios

modelo = Lasso(alpha=1.0)
modelo.fit(X, y)

nuevo_auto = [[60000, 2016, 0]]
print(f"Precio estimado: ${modelo.predict(nuevo_auto)[0]:.2f}")""",
            
            "explicacion_codigo": "Usamos un alpha=1.0 para ser más estrictos. El modelo penaliza la complejidad para evitar sobreajustarse a los datos de entrenamiento.",
            "quiz": {
                "pregunta": "¿Qué parámetro controla el castigo en Lasso?",
                "opciones": ["Beta", "Alpha", "Gamma"],
                "correcta": "Alpha",
                "retro_acierto": "¡Bien! Alpha es el hiperparámetro clave.",
                "retro_fallo": "Incorrecto. Beta y Gamma se usan en otros modelos, aquí usamos Alpha."
            },
            "versus": {
                "rival": "ElasticNet",
                "comparacion": "ElasticNet mezcla Lasso y Ridge. Úsalo si Lasso borra demasiadas cosas."
            }
        }
    ],

    "SVR": [
        {
            "titulo": "📈 1. Tendencia de Acciones",
            "contexto": "Ajustar una curva a precios que suben y bajan (no lineal).",
            "pasos": ["1. Datos de días.", "2. Kernel RBF permite curvas.", "3. Predicción futura."],
            "codigo": """import numpy as np
from sklearn.svm import SVR

# Día 1, Día 2, Día 3...
X = np.array([[1], [2], [3], [4], [5]])
# Precios (suben y bajan)
y = np.array([100, 110, 105, 115, 120])

# Kernel 'rbf' permite ajustar líneas curvas
modelo = SVR(kernel='rbf', C=100, gamma=0.1)
modelo.fit(X, y)

dia_futuro = [[6]]
print(f"Precio estimado Día 6: {modelo.predict(dia_futuro)[0]:.2f}")""",
            
            "explicacion_codigo": "kernel='rbf' (Radial Basis Function) es lo que permite doblar la línea. 'C' controla cuánto queremos evitar errores (C alto = ajuste estricto).",
            "quiz": {
                "pregunta": "¿Qué permite a SVR hacer curvas?",
                "opciones": ["El Kernel", "El precio", "La memoria"],
                "correcta": "El Kernel",
                "retro_acierto": "¡Exacto! El 'Truco del Kernel' proyecta datos para hallar patrones curvos.",
                "retro_fallo": "No. El precio es el dato y la memoria es hardware. La matemática curva viene del Kernel."
            },
            "versus": {
                "rival": "Linear Regression",
                "comparacion": "La regresión lineal solo dibuja rectas. SVR dibuja curvas complejas."
            }
        },
        {
            "titulo": "🌡️ 2. Predicción de Temperatura",
            "contexto": "Relación compleja entre humedad y calor.",
            "pasos": ["1. Datos históricos.", "2. Kernel Polinomial (curva U).", "3. Predice grados."],
            "codigo": """import numpy as np
from sklearn.svm import SVR

# Humedad (%)
X = np.array([[20], [30], [40], [80], [90]])
# Grados Celsius
y = np.array([35, 32, 30, 15, 12])

# Degree=2 intenta ajustar una parábola
modelo = SVR(kernel='poly', degree=2) 
modelo.fit(X, y)

print(f"Temp estimada con 50% humedad: {modelo.predict([[50]])[0]:.1f}°C")""",
            
            "explicacion_codigo": "Degree=2 significa que buscamos una relación cuadrática (x²), útil para fenómenos físicos que aceleran o desaceleran.",
            "quiz": {
                "pregunta": "¿Qué es Epsilon en SVR?",
                "opciones": ["Margen de error tolerado", "Nombre del creador", "Velocidad"],
                "correcta": "Margen de error tolerado",
                "retro_acierto": "¡Así es! SVR crea un 'tubo' de tolerancia alrededor de la predicción.",
                "retro_fallo": "Falso. Epsilon define qué tan exigente es el modelo con la precisión exacta."
            },
            "versus": {
                "rival": "Decision Trees",
                "comparacion": "Los árboles hacen predicciones escalonadas. SVR hace curvas suaves."
            }
        },
        {
            "titulo": "🏗️ 3. Resistencia de Materiales",
            "contexto": "Peso máximo de una viga según grosor (Relación Lineal).",
            "pasos": ["1. Datos ingeniería.", "2. SVR Lineal.", "3. Carga máxima."],
            "codigo": """import numpy as np
from sklearn.svm import SVR

# Grosor en mm
X = np.array([[10], [20], [30], [40]])
# Carga soportada en kg
y = np.array([100, 200, 300, 400])

# Aquí la relación es directa, usamos linear
modelo = SVR(kernel='linear')
modelo.fit(X, y)

print(f"Carga para 25mm: {modelo.predict([[25]])[0]:.0f} kg")""",
            
            "explicacion_codigo": "Aunque SVR es famoso por curvas, con kernel='linear' funciona igual que una regresión pero más robusta ante outliers.",
            "quiz": {
                "pregunta": "Si los datos forman una recta, ¿qué Kernel usas?",
                "opciones": ["RBF", "Poly", "Linear"],
                "correcta": "Linear",
                "retro_acierto": "¡Lógico! No gastes recursos en curvas si una recta funciona.",
                "retro_fallo": "No. RBF y Poly son para curvas complejas. Si es recto, usa Linear."
            },
            "versus": {
                "rival": "Lasso",
                "comparacion": "Ambos hacen rectas, pero SVR ignora mejor los errores pequeños dentro del margen."
            }
        }
    ],

    "SGD Regressor": [
        {
            "titulo": "⚡ 1. Consumo Eléctrico Masivo",
            "contexto": "Aprender dato por dato sin llenar la memoria RAM (Streaming).",
            "pasos": ["1. Llega un lote de datos.", "2. partial_fit actualiza modelo.", "3. Olvida esos datos."],
            "codigo": """import numpy as np
from sklearn.linear_model import SGDRegressor

# Configuramos el modelo
modelo = SGDRegressor(max_iter=1000, tol=1e-3)

print("Iniciando aprendizaje por streaming...")

# Simulamos que llegan datos de 3 en 3 (mini-batches)
for i in range(3):
    # Generamos 3 datos aleatorios nuevos
    X_chunk = np.random.rand(3, 1) 
    y_chunk = 2 * X_chunk.flatten() + 1 
    
    # partial_fit NO reinicia el modelo, solo lo actualiza
    modelo.partial_fit(X_chunk, y_chunk)
    print(f"Ronda {i+1}: Pesos actualizados -> {modelo.coef_}")

print("Modelo listo para seguir recibiendo datos.")""",
            
            "explicacion_codigo": "La función clave es .partial_fit(). A diferencia de .fit() normal, esta permite entrenar el modelo poco a poco, ideal para Big Data.",
            "quiz": {
                "pregunta": "¿Por qué usar SGD en lugar de Regresión normal?",
                "opciones": ["Es más preciso", "Soporta datos infinitos", "Es más fácil"],
                "correcta": "Soporta datos infinitos",
                "retro_acierto": "¡Correcto! Nunca carga todos los datos a la vez en la RAM.",
                "retro_fallo": "No exactamente. Su gran ventaja es procesar datos que no caben en memoria."
            },
            "versus": {
                "rival": "Batch Gradient Descent",
                "comparacion": "Batch lee TODOS los datos para dar un paso. SGD da un paso con cada dato (más rápido)."
            }
        },
        {
            "titulo": "🖱️ 2. Predicción de Clics (CTR)",
            "contexto": "Predecir probabilidad de click en publicidad online en tiempo real.",
            "pasos": ["1. Info del usuario.", "2. Actualizar al instante.", "3. Predecir."],
            "codigo": """import numpy as np
from sklearn.linear_model import SGDRegressor

modelo = SGDRegressor()

# Datos simulados: [Edad, Hora del día]
X_usuario1 = np.array([[25, 10]])
y_usuario1 = np.array([1]) # Dio Click

# El modelo aprende de este usuario único
modelo.partial_fit(X_usuario1, y_usuario1)

# Llega usuario nuevo
X_nuevo = np.array([[30, 12]])
print("Predicción para nuevo usuario:", modelo.predict(X_nuevo))""",
            
            "explicacion_codigo": "En publicidad, los gustos cambian rápido. SGD permite re-entrenar el modelo cada segundo con la actividad más reciente.",
            "quiz": {
                "pregunta": "¿Qué pasa si los datos llegan muy rápido?",
                "opciones": ["SGD se bloquea", "SGD se adapta rápido", "Necesitas reiniciar"],
                "correcta": "SGD se adapta rápido",
                "retro_acierto": "¡Exacto! Es ideal para sistemas de alta velocidad.",
                "retro_fallo": "Al contrario, SGD está diseñado para no bloquearse con velocidad."
            },
            "versus": {
                "rival": "Random Forest",
                "comparacion": "Un bosque es muy lento para re-entrenar. SGD lo hace en milisegundos."
            }
        },
        {
            "titulo": "🐦 3. Tendencias Twitter",
            "contexto": "Predecir volumen de tweets. El modelo debe adaptarse si algo se vuelve viral.",
            "pasos": ["1. Flujo de tweets.", "2. Ajustar pendiente.", "3. Predecir."],
            "codigo": """import numpy as np
from sklearn.linear_model import SGDRegressor

modelo = SGDRegressor()

# Minuto 1: 100 tweets
modelo.partial_fit([[1]], [100]) 
# Minuto 2: 200 tweets (Tendencia subiendo)
modelo.partial_fit([[2]], [200]) 

# ¿Cuántos habrá en el minuto 3?
pred = modelo.predict([[3]])
print(f"Predicción Minuto 3: {pred[0]:.0f} tweets")""",
            
            "explicacion_codigo": "El modelo calcula la pendiente (crecimiento) basándose solo en los últimos puntos recibidos.",
            "quiz": {
                "pregunta": "¿Qué significa 'Estocástico'?",
                "opciones": ["Aleatorio / Al azar", "Estático", "Estadístico"],
                "correcta": "Aleatorio / Al azar",
                "retro_acierto": "¡Bien! Toma muestras al azar para decidir hacia dónde moverse (optimizar).",
                "retro_fallo": "No. Viene de 'Stochastic' que implica azar/probabilidad en el movimiento."
            },
            "versus": {
                "rival": "Standard SVR",
                "comparacion": "SVR necesita todo el historial. SGD solo necesita el último dato."
            }
        }
    ],

    # =========================================================
    # CLASIFICACIÓN (Categorías)
    # =========================================================

    "Naive Bayes": [
        {
            "titulo": "📧 1. Filtro de SPAM",
            "contexto": "Si aparece 'GRATIS', la probabilidad de SPAM sube.",
            "pasos": ["1. Contar palabras.", "2. Calcular probabilidades.", "3. Clasificar."],
            "codigo": """import numpy as np
from sklearn.naive_bayes import MultinomialNB

# 0='Hola', 1='Gratis', 2='Reunión'
# Frase: "Hola Reunion" -> [1, 0, 1]
X = np.array([
    [1, 0, 1], # Normal
    [0, 1, 0], # Spam ("Gratis")
    [1, 1, 0]  # Spam ("Hola Gratis")
])
y = np.array([0, 1, 1]) # 0=Normal, 1=Spam

modelo = MultinomialNB()
modelo.fit(X, y)

# Nueva frase solo con "Gratis"
es_spam = modelo.predict([[0, 1, 0]])
print("¿Es Spam?:", "SÍ" if es_spam[0] == 1 else "NO")""",
            
            "explicacion_codigo": "MultinomialNB funciona contando frecuencias. Si 'Gratis' aparece mucho en correos marcados como Spam, el modelo aprende esa asociación.",
            "quiz": {
                "pregunta": "¿Por qué se llama 'Naive' (Ingenuo)?",
                "opciones": ["Es tonto", "Asume independencia", "Es nuevo"],
                "correcta": "Asume independencia",
                "retro_acierto": "¡Correcto! Cree que las palabras no se relacionan entre sí.",
                "retro_fallo": "Incorrecto. Se le dice ingenuo porque simplifica el mundo asumiendo que nada está conectado."
            },
            "versus": {
                "rival": "Logistic Regression",
                "comparacion": "Logistic busca una fórmula precisa. Bayes cuenta probabilidades, siendo más rápido entrenando."
            }
        },
        {
            "titulo": "😊 2. Análisis de Sentimientos",
            "contexto": "Saber si un comentario es Positivo o Negativo.",
            "pasos": ["1. Contar buenas/malas.", "2. Probabilidades.", "3. Tono."],
            "codigo": """from sklearn.naive_bayes import MultinomialNB
import numpy as np

# [Palabras_Buenas, Palabras_Malas]
X = np.array([
    [3, 0], # "Muy muy bueno"
    [0, 3], # "Mal mal horrible"
    [2, 1]  # "Bueno pero lento"
])
y = np.array(['Positivo', 'Negativo', 'Neutro'])

modelo = MultinomialNB()
modelo.fit(X, y)

# Comentario con 1 buena y 5 malas
print("Resultado:", modelo.predict([[1, 5]])[0])""",
            
            "explicacion_codigo": "El modelo balancea la evidencia. Aunque haya 1 palabra buena, las 5 malas pesan más en la probabilidad condicional.",
            "quiz": {
                "pregunta": "¿Para qué datos es mejor Naive Bayes?",
                "opciones": ["Imágenes", "Texto y NLP", "Audio"],
                "correcta": "Texto y NLP",
                "retro_acierto": "¡Sí! Es el rey del procesamiento de texto rápido.",
                "retro_fallo": "No. Para imágenes y audio se usan redes neuronales."
            },
            "versus": {
                "rival": "LSTM (Deep Learning)",
                "comparacion": "Una red neuronal entiende sarcasmo. Naive Bayes no, es literal."
            }
        },
        {
            "titulo": "🩺 3. Diagnóstico Médico Simple",
            "contexto": "Gripe vs Alergia basado en síntomas (Sí/No).",
            "pasos": ["1. Síntomas binarios.", "2. BernoulliNB.", "3. Diagnóstico."],
            "codigo": """from sklearn.naive_bayes import BernoulliNB
import numpy as np

# [Fiebre, Estornudos] -> 1=Sí, 0=No
X = np.array([
    [1, 0], # Solo fiebre -> Gripe
    [0, 1], # Solo estornudo -> Alergia
    [1, 1]  # Ambos -> Gripe
])
y = np.array(['Gripe', 'Alergia', 'Gripe'])

modelo = BernoulliNB()
modelo.fit(X, y)

paciente = [[1, 1]] # Tiene ambas
print("Diagnóstico:", modelo.predict(paciente)[0])""",
            
            "explicacion_codigo": "Usamos BernoulliNB porque los datos son binarios (True/False). Multinomial es para conteos (1, 2, 3...).",
            "quiz": {
                "pregunta": "Si tiene fiebre, ¿qué hace el modelo?",
                "opciones": ["Llama al doctor", "Calcula Prob(Gripe | Fiebre)", "Nada"],
                "correcta": "Calcula Prob(Gripe | Fiebre)",
                "retro_acierto": "¡Exacto! Aplica el Teorema de Bayes puro.",
                "retro_fallo": "No. El modelo matemático solo calcula la probabilidad condicional."
            },
            "versus": {
                "rival": "Decision Tree",
                "comparacion": "Un árbol sigue reglas fijas. Bayes maneja incertidumbre y probabilidades."
            }
        }
    ],

    "Linear SVC": [
        {
            "titulo": "🛑 1. Clasificación Lineal Estricta",
            "contexto": "Separar dos grupos con una línea recta perfecta.",
            "pasos": ["1. Puntos 2D.", "2. Buscar mejor línea (margen).", "3. Clasificar."],
            "codigo": """from sklearn.svm import LinearSVC
import numpy as np

# Coordenadas [X, Y]
X = np.array([[1, 1], [2, 2], [8, 8], [9, 9]])
y = np.array([0, 0, 1, 1]) # Clase 0 (Abajo), Clase 1 (Arriba)

modelo = LinearSVC()
modelo.fit(X, y)

# Punto intermedio
punto = [[1.5, 1.5]]
print("Clase predicha:", modelo.predict(punto)[0])""",
            
            "explicacion_codigo": "LinearSVC busca trazar una línea que maximice la distancia (margen) entre los puntos más cercanos de ambos grupos.",
            "quiz": {
                "pregunta": "¿Qué es el 'Margen'?",
                "opciones": ["El error", "Espacio vacío entre la línea y datos", "El borde"],
                "correcta": "Espacio vacío entre la línea y datos",
                "retro_acierto": "¡Bien! SVM busca la 'carretera' más ancha posible.",
                "retro_fallo": "Incorrecto. El margen es la separación segura entre los dos grupos."
            },
            "versus": {
                "rival": "KNN",
                "comparacion": "KNN mira vecindad. SVM mira fronteras y geometría."
            }
        },
        {
            "titulo": "💻 2. Detección de Malware",
            "contexto": "Separar archivos seguros de virus usando firmas binarias.",
            "pasos": ["1. Características binarias.", "2. Hiperplano separador.", "3. Clasificar."],
            "codigo": """from sklearn.svm import LinearSVC
import numpy as np

# [Usa red?, Modifica sistema?, Es oculto?]
X = np.array([
    [0,0,0], # Seguro
    [1,1,1], # Virus
    [0,1,0], # Seguro
    [1,0,1]  # Virus
])
y = np.array(['Seguro', 'Virus', 'Seguro', 'Virus'])

modelo = LinearSVC()
modelo.fit(X, y)

archivo = [[1, 0, 1]] # Red + Oculto
print("El archivo es:", modelo.predict(archivo)[0])""",
            
            "explicacion_codigo": "En muchas dimensiones, la 'línea' separadora se llama Hiperplano. SVM es excelente encontrando este plano óptimo.",
            "quiz": {
                "pregunta": "¿Si los datos no se pueden separar con recta?",
                "opciones": ["Falla", "Hace curvas", "Borra datos"],
                "correcta": "Falla",
                "retro_acierto": "¡Correcto! Para curvas necesitas SVM con Kernel o Random Forest.",
                "retro_fallo": "No. Este modelo es estrictamente lineal. Para curvas necesitas Kernels."
            },
            "versus": {
                "rival": "RBF SVM",
                "comparacion": "LinearSVC es rígido (rectas). RBF SVM es flexible (curvas) pero lento."
            }
        },
        {
            "titulo": "🍎 3. Clasificación de Frutas",
            "contexto": "Manzanas vs Naranjas usando color y peso.",
            "pasos": ["1. Peso/Color.", "2. Ajuste lineal.", "3. Predicción."],
            "codigo": """from sklearn.svm import LinearSVC
import numpy as np

# [Peso(gr), Color(1=Rojo, 5=Naranja)]
X = np.array([
    [150, 1], [160, 1], # Manzanas
    [140, 5], [155, 5]  # Naranjas
]) 
y = np.array(['Manzana', 'Manzana', 'Naranja', 'Naranja'])

modelo = LinearSVC()
modelo.fit(X, y)

fruta = [[145, 5]]
print("Es una:", modelo.predict(fruta)[0])""",
            
            "explicacion_codigo": "El modelo aprende que el eje 'Color' es determinante. Si color es alto (5), cae del lado del hiperplano de Naranjas.",
            "quiz": {
                "pregunta": "¿Sirve para texto?",
                "opciones": ["No", "Sí, excelente", "Solo imágenes"],
                "correcta": "Sí, excelente",
                "retro_acierto": "¡Así es! Funciona genial en espacios de alta dimensión como texto.",
                "retro_fallo": "Te sorprenderá, pero sí. Es uno de los mejores para clasificar textos."
            },
            "versus": {
                "rival": "Random Forest",
                "comparacion": "Forest usa reglas 'Si... entonces'. SVM usa geometría matemática."
            }
        }
    ],

    "KNN": [
        {
            "titulo": "🎥 1. Recomendador de Películas",
            "contexto": "Si a tus vecinos les gusta, a ti también. (Vecinos Cercanos).",
            "pasos": ["1. Mapa de gustos.", "2. Buscar 3 vecinos.", "3. Votación."],
            "codigo": """from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# [Nivel Acción, Nivel Romance] (Escala 1-10)
X = np.array([
    [1, 9], [2, 8], # Aman Romance
    [9, 1], [8, 2]  # Aman Acción
])
y = np.array(['Romance', 'Romance', 'Acción', 'Acción'])

# Mira a los 3 más cercanos
modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X, y)

usuario = [[5, 5]] # Gustos neutros
print("Recomendación:", modelo.predict(usuario)[0])""",
            
            "explicacion_codigo": "n_neighbors=3 indica que el algoritmo buscará los 3 puntos más cercanos geométricamente y tomará la decisión por mayoría de votos.",
            "quiz": {
                "pregunta": "¿Qué es la 'K' en KNN?",
                "opciones": ["Kilómetros", "Número de vecinos", "Constante"],
                "correcta": "Número de vecinos",
                "retro_acierto": "¡Exacto! K=1 copia al más cercano. K=100 hace votación masiva.",
                "retro_fallo": "No. K se refiere a la cantidad de puntos cercanos que consultaremos."
            },
            "versus": {
                "rival": "Matrix Factorization",
                "comparacion": "KNN busca usuarios similares. Netflix usa Factorización para hallar patrones ocultos."
            }
        },
        {
            "titulo": "🔢 2. Reconocimiento de Dígitos",
            "contexto": "Comparar imagen nueva con base de datos píxel a píxel.",
            "pasos": ["1. Píxeles.", "2. Distancia.", "3. Clasificar."],
            "codigo": """from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Píxeles simples [Blanco, Negro, Blanco...]
X = np.array([
    [0,1,0], # Patrón 1
    [1,1,1], # Patrón 2
    [1,0,1]  # Patrón 3
])
y = np.array(['Uno', 'Tachado', 'U'])

modelo = KNeighborsClassifier(n_neighbors=1)
modelo.fit(X, y)

print("Predicción [0,1,0]:", modelo.predict([[0, 1, 0]])[0])""",
            
            "explicacion_codigo": "KNN no 'aprende' una forma. Simplemente guarda todas las imágenes y compara la nueva con todas las guardadas.",
            "quiz": {
                "pregunta": "¿Desventaja de KNN con muchos datos?",
                "opciones": ["Es lento", "Es poco preciso", "Se ve borroso"],
                "correcta": "Es lento",
                "retro_acierto": "¡Correcto! Tiene que comparar contra TODO cada vez.",
                "retro_fallo": "Incorrecto. El problema es la velocidad, porque tiene que medir distancia con todos."
            },
            "versus": {
                "rival": "CNN (Redes Neuronales)",
                "comparacion": "CNN aprende formas (líneas, curvas). KNN solo compara píxeles brutos."
            }
        },
        {
            "titulo": "🍷 3. Calidad de Vinos",
            "contexto": "Clasificar vino comparándolo con botellas similares químicas.",
            "pasos": ["1. Datos químicos.", "2. Buscar gemelos.", "3. Calidad."],
            "codigo": """from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# [Acidez, Azúcar]
X = np.array([[7, 2], [6, 1.5], [8, 5], [9, 6]]) 
y = np.array(['Bueno', 'Bueno', 'Malo', 'Malo'])

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X, y)

vino_nuevo = [[6.5, 2]]
print("Calidad:", modelo.predict(vino_nuevo)[0])""",
            
            "explicacion_codigo": "Se llama 'Lazy Learning' (Aprendizaje Vago) porque no genera una fórmula, solo consulta la base de datos en el momento.",
            "quiz": {
                "pregunta": "¿KNN crea una fórmula matemática?",
                "opciones": ["Sí", "No (Lazy)", "A veces"],
                "correcta": "No (Lazy)",
                "retro_acierto": "¡Muy bien! Solo guarda datos en memoria.",
                "retro_fallo": "Falso. KNN no genera una ecuación matemática, solo almacena los puntos."
            },
            "versus": {
                "rival": "SVM",
                "comparacion": "SVM busca una fórmula general. KNN carga con todos los datos."
            }
        }
    ],

    "Random Forest": [
        {
            "titulo": "🏥 1. Diagnóstico Médico",
            "contexto": "Votación de múltiples 'doctores' (árboles).",
            "pasos": ["1. Muchos árboles.", "2. Votación.", "3. Mayoría gana."],
            "codigo": """from sklearn.ensemble import RandomForestClassifier
import numpy as np

# [Edad, Colesterol, Presión]
X = np.array([
    [25, 180, 120], 
    [30, 240, 140], 
    [50, 200, 130], 
    [60, 260, 150]
])
y = np.array(['Sano', 'Enfermo', 'Sano', 'Enfermo'])

# 10 árboles votando
modelo = RandomForestClassifier(n_estimators=10, random_state=42)
modelo.fit(X, y)

paciente = [[40, 250, 135]]
print("Diagnóstico:", modelo.predict(paciente)[0])""",
            
            "explicacion_codigo": "n_estimators=10 crea 10 árboles distintos. Cada uno ve una parte diferente de los datos para evitar sesgos.",
            "quiz": {
                "pregunta": "¿Ventaja frente a un solo árbol?",
                "opciones": ["Más bonito", "Evita errores (Overfitting)", "Más rápido"],
                "correcta": "Evita errores (Overfitting)",
                "retro_acierto": "¡Exacto! El bosque promedia errores individuales.",
                "retro_fallo": "No. Un solo árbol suele ser más rápido, pero el bosque se equivoca menos."
            },
            "versus": {
                "rival": "Decision Tree",
                "comparacion": "Un árbol es inestable. El bosque es robusto y fiable."
            }
        },
        {
            "titulo": "🦁 2. Clasificación de Animales",
            "contexto": "Reglas complejas: Pelo, huevos, vuela.",
            "pasos": ["1. Características.", "2. Bosque decide.", "3. Especie."],
            "codigo": """from sklearn.ensemble import RandomForestClassifier
import numpy as np

# [Pelo?, Huevos?, Vuela?]
X = np.array([
    [1,0,0], # Perro
    [0,1,1], # Pájaro
    [0,1,0]  # Serpiente
])
y = np.array(['Mamífero', 'Ave', 'Reptil'])

modelo = RandomForestClassifier(n_estimators=10)
modelo.fit(X, y)

print("Animal:", modelo.predict([[1, 0, 0]])[0])""",
            
            "explicacion_codigo": "Cada árbol hace preguntas tipo '¿Tiene pelo?'. Al final, si 8 árboles dicen 'Mamífero', esa es la respuesta.",
            "quiz": {
                "pregunta": "¿Cómo se llama combinar modelos?",
                "opciones": ["Ensemble Learning", "Deep Learning", "Cluster"],
                "correcta": "Ensemble Learning",
                "retro_acierto": "¡Bien! Ensemble significa conjunto. La unión hace la fuerza.",
                "retro_fallo": "Incorrecto. Se llama Aprendizaje en Conjunto (Ensemble)."
            },
            "versus": {
                "rival": "Redes Neuronales",
                "comparacion": "Las redes son cajas negras. Random Forest te dice qué variables importaron."
            }
        },
        {
            "titulo": "💳 3. Fraude Bancario",
            "contexto": "Detectar transacciones raras con muchas variables.",
            "pasos": ["1. Historial.", "2. Votación masiva.", "3. Alerta."],
            "codigo": """from sklearn.ensemble import RandomForestClassifier
import numpy as np

# [Monto, Hora, Distancia]
X = np.array([
    [10, 12, 1], 
    [10000, 3, 500], # Fraude obvio
    [20, 14, 2]
])
y = np.array(['Ok', 'Fraude', 'Ok'])

modelo = RandomForestClassifier(n_estimators=100)
modelo.fit(X, y)

transaccion = [[5000, 4, 200]]
print("Estado:", modelo.predict(transaccion)[0])""",
            
            "explicacion_codigo": "Usamos 100 árboles porque el fraude es sutil. Necesitamos muchas 'opiniones' para estar seguros.",
            "quiz": {
                "pregunta": "¿Si un árbol se equivoca?",
                "opciones": ["Falla todo", "Los otros 99 corrigen", "Se borra"],
                "correcta": "Los otros 99 corrigen",
                "retro_acierto": "¡Esa es la clave! La sabiduría de la mayoría gana.",
                "retro_fallo": "No. Si uno falla, los otros 99 ganan la votación."
            },
            "versus": {
                "rival": "Gradient Boosting",
                "comparacion": "RF entrena árboles en paralelo. Boosting los entrena en serie corrigiendo errores previos."
            }
        }
    ],

    # =========================================================
    # CLUSTERING (Agrupar)
    # =========================================================

    "K-Means": [
        {
            "titulo": "👕 1. Tallas de Camisetas",
            "contexto": "Definir tallas S, M, L en datos de medidas.",
            "pasos": ["1. Definir K=3.", "2. Mover centros.", "3. Asignar grupos."],
            "codigo": """from sklearn.cluster import KMeans
import numpy as np

# [Altura, Peso]
X = np.array([
    [160, 55], [165, 60], # Pequeños
    [180, 80], [185, 85], # Grandes
    [175, 70]             # Medios
])

# K=3 (Queremos 3 tallas)
modelo = KMeans(n_clusters=3, n_init=10)
modelo.fit(X)

print("Centros (Tallas ideales):", modelo.cluster_centers_)
print("Grupo cliente nuevo:", modelo.predict([[170, 72]])[0])""",
            
            "explicacion_codigo": "n_clusters=3 es obligatorio. El algoritmo mueve 3 puntos centrales hasta que quedan en medio de los grupos de datos.",
            "quiz": {
                "pregunta": "¿Qué debes decirle a K-Means obligatoriamente?",
                "opciones": ["Nombres", "Número de grupos (K)", "Colores"],
                "correcta": "Número de grupos (K)",
                "retro_acierto": "¡Correcto! K-Means no sabe adivinar cuántos grupos hay.",
                "retro_fallo": "Falso. El algoritmo necesita saber cuántos grupos (K) buscar antes de empezar."
            },
            "versus": {
                "rival": "DBSCAN",
                "comparacion": "K-Means te obliga a elegir K. DBSCAN encuentra el número solo."
            }
        },
        {
            "titulo": "🎨 2. Compresión de Imágenes",
            "contexto": "Reducir colores de una foto a solo 2.",
            "pasos": ["1. Píxeles RGB.", "2. K=2.", "3. Reducir."],
            "codigo": """from sklearn.cluster import KMeans
import numpy as np

# Píxeles [R, G, B]
X = np.array([
    [255, 0, 0], [250, 10, 10], # Rojos
    [0, 0, 255], [10, 10, 250]  # Azules
])

modelo = KMeans(n_clusters=2, n_init=10)
modelo.fit(X)

print("Etiquetas (0 o 1):", modelo.labels_)""",
            
            "explicacion_codigo": "Agrupa miles de colores en solo 2 promedios. Así se comprimen las imágenes (GIF, PNG).",
            "quiz": {
                "pregunta": "¿Cómo se llama el centro del grupo?",
                "opciones": ["Centroide", "Núcleo", "Líder"],
                "correcta": "Centroide",
                "retro_acierto": "¡Bien! Es el promedio matemático.",
                "retro_fallo": "No. En K-Means se le llama Centroide."
            },
            "versus": {
                "rival": "Hierarchical Clustering",
                "comparacion": "K-Means es rápido. Hierarchical permite ver subgrupos dentro de grupos."
            }
        },
        {
            "titulo": "👥 3. Segmentación de Clientes",
            "contexto": "Agrupar por comportamiento de compra.",
            "pasos": ["1. Datos sin etiqueta.", "2. Agrupar.", "3. Analizar."],
            "codigo": """from sklearn.cluster import KMeans
import numpy as np

# [Gasto Anual, Frecuencia]
X = np.array([[1000, 50], [200, 2], [1200, 60], [150, 5]])

modelo = KMeans(n_clusters=2, n_init=10)
modelo.fit(X)

cliente = [[500, 20]]
print("Grupo asignado:", modelo.predict(cliente)[0])""",
            
            "explicacion_codigo": "El modelo detecta patrones: 'Gente que gasta mucho' vs 'Gente que gasta poco', sin que tú se lo digas.",
            "quiz": {
                "pregunta": "¿Tipo de aprendizaje?",
                "opciones": ["Supervisado", "No Supervisado", "Reforzado"],
                "correcta": "No Supervisado",
                "retro_acierto": "¡Exacto! No usamos etiquetas.",
                "retro_fallo": "Incorrecto. Como no le damos las respuestas correctas, es No Supervisado."
            },
            "versus": {
                "rival": "Clasificación",
                "comparacion": "En Clasificación tú enseñas las clases. En Clustering el modelo las inventa."
            }
        }
    ],

    "DBSCAN": [
        {
            "titulo": "🗺️ 1. Zonas de Calor (GPS)",
            "contexto": "Encontrar grupos densos e ignorar ruido.",
            "pasos": ["1. GPS.", "2. Densidad.", "3. Ruido."],
            "codigo": """from sklearn.cluster import DBSCAN
import numpy as np

# Coordenadas
X = np.array([
    [1, 1], [1, 2], [2, 1], # Grupo denso
    [100, 100]              # Ruido (Lejos)
])

# eps=3 (distancia máxima), min_samples=2 (vecinos mínimos)
modelo = DBSCAN(eps=3, min_samples=2)
labels = modelo.fit_predict(X)

print("Etiquetas:", labels) 
# 0 = Grupo, -1 = Ruido""",
            
            "explicacion_codigo": "DBSCAN es único porque etiqueta como '-1' los datos que están solos y lejos. K-Means los forzaría a entrar en un grupo.",
            "quiz": {
                "pregunta": "¿Qué hace con los puntos aislados?",
                "opciones": ["Los fuerza", "Marca Ruido (-1)", "Borra"],
                "correcta": "Marca Ruido (-1)",
                "retro_acierto": "¡Correcto! Limpia datos sucios.",
                "retro_fallo": "No. No los borra ni los fuerza, los etiqueta diferente (-1)."
            },
            "versus": {
                "rival": "K-Means",
                "comparacion": "K-Means asume esferas. DBSCAN encuentra formas raras (serpientes, lunas)."
            }
        },
        {
            "titulo": "💳 2. Detección de Anomalías",
            "contexto": "Transacción solitaria = Fraude.",
            "pasos": ["1. Transacciones.", "2. DBSCAN.", "3. Alerta."],
            "codigo": """from sklearn.cluster import DBSCAN
import numpy as np

X = np.array([[10, 10], [11, 11], [10, 12], [500, 500]])

modelo = DBSCAN(eps=5, min_samples=2)
labels = modelo.fit_predict(X)

es_anomalia = labels[-1] == -1
print("¿El último es anomalía?:", es_anomalia)""",
            
            "explicacion_codigo": "Si no tiene suficientes vecinos cerca (definido por eps y min_samples), se considera una anomalía.",
            "quiz": {
                "pregunta": "¿Necesitas decirle cuántos grupos (K) buscar?",
                "opciones": ["Sí", "No", "A veces"],
                "correcta": "No",
                "retro_acierto": "¡Exacto! Él te dirá cuántos encontró.",
                "retro_fallo": "Falso. DBSCAN descubre el número de grupos automáticamente."
            },
            "versus": {
                "rival": "Isolation Forest",
                "comparacion": "Isolation Forest es solo para anomalías. DBSCAN agrupa Y detecta anomalías."
            }
        },
        {
            "titulo": "✨ 3. Astronomía (Galaxias)",
            "contexto": "Agrupar estrellas.",
            "pasos": ["1. Estrellas.", "2. Densidad.", "3. Grupos."],
            "codigo": """from sklearn.cluster import DBSCAN
import numpy as np

X = np.array([[10,10], [12,12], [80,80], [82,82], [50,50]])

modelo = DBSCAN(eps=10, min_samples=2)
labels = modelo.fit_predict(X)

print("Grupos encontrados:", set(labels))""",
            
            "explicacion_codigo": "Conecta estrellas cercanas 'saltando' de una a otra. Así puede dibujar la forma de una galaxia irregular.",
            "quiz": {
                "pregunta": "¿Qué es Epsilon (eps)?",
                "opciones": ["Radio búsqueda", "Estrellas", "Velocidad"],
                "correcta": "Radio búsqueda",
                "retro_acierto": "¡Bien! Define la vecindad.",
                "retro_fallo": "Incorrecto. Epsilon es la distancia máxima para considerar dos puntos como vecinos."
            },
            "versus": {
                "rival": "Gaussian Mixture",
                "comparacion": "GMM usa probabilidad. DBSCAN usa densidad pura."
            }
        }
    ]
}