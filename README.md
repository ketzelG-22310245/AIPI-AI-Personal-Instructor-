# AIPI-AI-Personal-Instructor-

Markdown

# 🧠 AIPI: AI Personal Instructor
> **Sistema Experto Educativo para la Selección de Algoritmos de Machine Learning**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=flat&logo=flask)
![Status](https://img.shields.io/badge/Estado-Terminado-success)

## 📖 Descripción del Proyecto

**AIPI** es un Sistema Experto basado en reglas (Forward Chaining) diseñado para ayudar a estudiantes y desarrolladores a seleccionar el algoritmo de Machine Learning más adecuado para sus problemas.

A diferencia de un simple árbol de decisiones, AIPI funciona como un **tutor inteligente**: no solo te da la respuesta, sino que te enseña mediante ejemplos de código ejecutables, explicaciones detalladas línea por línea, comparativas técnicas y quizzes interactivos.

Este proyecto fue desarrollado como parte de la materia de **Sistemas Expertos** en **CETI**.

---

## ✨ Características Principales

### 🎓 Módulo Educativo
* **Diagnóstico Guiado:** Interfaz de chat intuitiva que realiza preguntas estratégicas para filtrar opciones.
* **Base de Conocimientos:** Cubre 9 algoritmos clave (Regresión, Clasificación y Clustering).
* **Lupa de Código:** Explicaciones detalladas de qué hace cada línea del código generado.
* **Modo Versus:** Comparativas técnicas entre el algoritmo recomendado y sus rivales directos.
* **Quizzes Interactivos:** Retos rápidos con retroalimentación inmediata para validar el aprendizaje.

### 🎮 Gamificación y UX
* **Niveles de Usuario:** Sube de rango ("Novato" ➔ "Estudiante" ➔ "Científico de Datos") conforme interactúas con el sistema.
* **Gestión de Chats:** Crea, cambia y borra conversaciones múltiples sin perder el contexto.
* **Persistencia Local:** Sistema de guardado de progreso automático y función de "Hard Reset".

### 📊 Panel de Administración
* **Feedback Loop:** Los usuarios pueden votar (Like/Dislike) sobre las recomendaciones.
* **Dashboard Oculto:** Visualización de métricas de satisfacción en tiempo real en la ruta `/admin`.

---

## 📸 Capturas de Pantalla

*(Puedes agregar aquí tus capturas de pantalla guardándolas en una carpeta `screenshots`)*

| Chat Interactivo | Resultado y Código |
|:---:|:---:|
| ![Chat](screenshots/chat_preview.png) | ![Code](screenshots/code_preview.png) |

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para correr el proyecto en tu computadora local:

### 1. Clonar el repositorio
git clone [https://github.com/TU_USUARIO/AIPI-System.git](https://github.com/TU_USUARIO/AIPI-System.git)
cd AIPI-System

##2. Crear un entorno virtual (Recomendado)
# En Windows:
python -m venv venv
venv\Scripts\activate

# En Mac/Linux:
python3 -m venv venv
source venv/bin/activate

##3. Instalar dependencias
pip install -r requirements.txt
4. Ejecutar la aplicación
Bash
python app.py

##5. Abrir en el navegador
Ve a la siguiente dirección en tu navegador web: http://127.0.0.1:5000

Para ver el panel de administración, ve a: http://127.0.0.1:5000/admin

📂 Estructura del Proyecto
Plaintext

/AIPI-System
│
├── app.py                 # Lógica del Motor de Inferencia y Servidor Flask
├── knowledge_base.py      # Base de Conocimientos (Reglas, Quizzes, Ejemplos)
├── requirements.txt       # Lista de librerías necesarias
├── feedback_log.txt       # Base de datos simple (Logs de votos y actividad)
│
├── static/                # Archivos estáticos
│   ├── style.css          # Hoja de estilos (Diseño System Figma)
│   └── image/             # Logos y recursos gráficos
│       ├── logo.png
│       └── ceti.png
│
├── templates/             # Plantillas HTML
│   ├── index.html         # Interfaz principal (Chat)
│   └── admin.html         # Dashboard de estadísticas
│
└── README.md              # Documentación del proyecto

🧠 Base de Conocimientos
El sistema cubre los siguientes algoritmos:

Regresión: Lasso, SVR, SGD Regressor.

Clasificación: Naive Bayes, Linear SVC, KNN, Random Forest.

Clustering: K-Means, DBSCAN.

👨‍💻 Autor
Ketzel Gibran Carrillo Ibarra

Institución: CETI (Centro de Enseñanza Técnica Industrial)

Carrera: Ingeniería en Desarrollo de Software

Materia: Sistemas Expertos
