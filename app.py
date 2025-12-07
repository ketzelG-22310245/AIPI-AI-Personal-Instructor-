from flask import Flask, render_template, request, session, redirect, url_for
import random
# Asegúrate de que knowledge_base.py esté en la misma carpeta y tenga los datos completos
from knowledge_base import data_ml  

app = Flask(__name__)
app.secret_key = "clave_secreta_aipi_master_vfinal"  # Necesaria para las sesiones

# ==========================================
# 1. LÓGICA DEL ÁRBOL DE DECISIÓN
# ==========================================
logic_tree = {
    "inicio": {
        "pregunta": "Hola, soy tu instructor AIPI. ¿Cuál es tu objetivo principal?",
        "opciones": [
            {"texto": "Predecir Números (Regresión)", "next": "regresion"},
            {"texto": "Clasificar Categorías", "next": "clasificacion"},
            {"texto": "Agrupar Datos (Clustering)", "next": "clustering"}
        ]
    },
    "regresion": {
        "pregunta": "¿Cuántos datos tienes disponibles?",
        "opciones": [
            {"texto": "Pocos (< 100k filas)", "next": "reg_small"},
            {"texto": "Masivos / Streaming (> 100k)", "next": "res_SGD Regressor"}
        ]
    },
    "reg_small": {
        "pregunta": "¿Qué priorizas en el resultado?",
        "opciones": [
            {"texto": "Eliminar ruido (Feature Selection)", "next": "res_Lasso"},
            {"texto": "Precisión en curvas complejas", "next": "res_SVR"}
        ]
    },
    "clasificacion": {
        "pregunta": "¿Qué tipo de datos analizas?",
        "opciones": [
            {"texto": "Texto / Lenguaje Natural", "next": "class_text"},
            {"texto": "Tablas Estructuradas (Excel)", "next": "class_table"}
        ]
    },
    "class_text": {
        "pregunta": "¿Qué enfoque prefieres?",
        "opciones": [
            {"texto": "Probabilístico (rápido)", "next": "res_Naive Bayes"},
            {"texto": "Geométrico (preciso)", "next": "res_Linear SVC"}
        ]
    },
    "class_table": {
        "pregunta": "¿Complejidad del modelo?",
        "opciones": [
            {"texto": "Simple e Interpretable", "next": "res_KNN"},
            {"texto": "Robusto y Potente", "next": "res_Random Forest"}
        ]
    },
    "clustering": {
        "pregunta": "¿Conoces el número de grupos (K)?",
        "opciones": [
            {"texto": "Sí, sé cuántos grupos busco", "next": "res_K-Means"},
            {"texto": "No, quiero descubrirlos", "next": "res_DBSCAN"}
        ]
    }
}

# Función auxiliar para iniciar un chat limpio
def create_new_chat_history():
    return [{
        "role": "bot", 
        "type": "question", 
        "content": logic_tree["inicio"]["pregunta"], 
        "options": logic_tree["inicio"]["opciones"]
    }]

# ==========================================
# 2. RUTA PRINCIPAL (CHAT)
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def index():
    # --- INICIALIZACIÓN DE SESIÓN ---
    if 'chats' not in session:
        session['chats'] = {'Chat 1': create_new_chat_history()}
        session['active_chat'] = 'Chat 1'

    # Seguridad: Si el chat activo no existe (por algún error), reiniciamos o asignamos uno
    if session.get('active_chat') not in session['chats']:
        if len(session['chats']) > 0:
            session['active_chat'] = list(session['chats'].keys())[0]
        else:
            session['chats'] = {'Chat 1': create_new_chat_history()}
            session['active_chat'] = 'Chat 1'
    
    current_id = session['active_chat']

    # --- GAMIFICACIÓN: CÁLCULO DE NIVEL ---
    # Contamos mensajes totales para determinar el nivel
    total_msgs = sum(len(c) for c in session['chats'].values())
    
    if total_msgs < 10:
        user_level = "Novato 🐣"
        progress = (total_msgs / 10) * 100
    elif total_msgs < 30:
        user_level = "Estudiante 🎓"
        progress = ((total_msgs - 10) / 20) * 100
    else:
        user_level = "Científico de Datos 🚀"
        progress = 100

    if request.method == 'POST':
        action = request.form.get('action')
        
        # Obtenemos historial actual (si existe), si no, creamos uno temporal para evitar crash
        if current_id in session['chats']:
            active_history = session['chats'][current_id]
        else:
            active_history = [] 

        # -------------------------------------------------
        # GESTIÓN DE CHATS (Sidebar)
        # -------------------------------------------------
        
        # A. NUEVO CHAT (Lógica corregida con max + 1)
        if action == 'new_chat':
            existing_nums = []
            for key in session['chats'].keys():
                try:
                    # Extraer el número del nombre "Chat X"
                    num = int(key.split(' ')[1])
                    existing_nums.append(num)
                except: pass
            
            # Si no hay chats, el siguiente es 1. Si hay, es el máximo + 1
            next_num = max(existing_nums) + 1 if existing_nums else 1
            new_id = f"Chat {next_num}"
            
            session['chats'][new_id] = create_new_chat_history()
            session['active_chat'] = new_id
            session.modified = True
            return redirect(url_for('index'))

        # B. CAMBIAR DE CHAT
        elif action == 'switch_chat':
            chat_to_switch = request.form.get('chat_id')
            if chat_to_switch in session['chats']:
                session['active_chat'] = chat_to_switch
            return redirect(url_for('index'))

        # C. ELIMINAR UN CHAT
        elif action == 'delete_chat':
            chat_to_delete = request.form.get('chat_id')
            if chat_to_delete in session['chats']:
                del session['chats'][chat_to_delete]
            
            # Lógica post-borrado: ¿Qué mostramos ahora?
            if len(session['chats']) == 0:
                session['chats'] = {'Chat 1': create_new_chat_history()}
                session['active_chat'] = 'Chat 1'
            elif chat_to_delete == current_id:
                session['active_chat'] = list(session['chats'].keys())[0]
            
            session.modified = True
            return redirect(url_for('index'))

        # D. BORRAR TODO EL PROGRESO (HARD RESET)
        elif action == 'delete_all_data':
            session['chats'] = {'Chat 1': create_new_chat_history()}
            session['active_chat'] = 'Chat 1'
            session.modified = True
            return redirect(url_for('index'))

        # -------------------------------------------------
        # INTERACCIÓN DENTRO DEL CHAT
        # -------------------------------------------------
        
        # E. FEEDBACK (Like/Dislike) + Respuesta
        elif action == 'feedback':
            score = request.form.get('score')
            algo = request.form.get('algo')
            
            # Guardar log en archivo de texto
            try:
                with open('feedback_log.txt', 'a', encoding='utf-8') as f:
                    f.write(f"Voto: {score.upper()} | Algoritmo: {algo} | Nivel: {user_level}\n")
            except: pass

            msg_bot = "¡Gracias por tu opinión! He registrado tu voto para mejorar el sistema. ¿Qué deseas hacer ahora?"
            active_history.append({"role": "bot", "type": "post_feedback", "content": msg_bot})
            session.modified = True
            return redirect(url_for('index'))

        # F. QUIZ (Reto Rápido con lógica Acierto/Fallo)
        elif action == 'answer_quiz':
            user_ans = request.form.get('answer')
            correct = request.form.get('correct')
            
            # Textos personalizados de retroalimentación
            retro_acierto = request.form.get('retro_acierto')
            retro_fallo = request.form.get('retro_fallo')
            
            is_correct = (user_ans == correct)
            
            if is_correct:
                feedback_text = f"✅ {retro_acierto}"
            else:
                feedback_text = f"❌ {retro_fallo}"
            
            active_history.append({"role": "user", "content": f"Respuesta Quiz: {user_ans}"})
            active_history.append({"role": "bot", "type": "quiz_result", "content": feedback_text})
            session.modified = True
            return redirect(url_for('index'))

        # G. VERSUS (Comparativa)
        elif action == 'show_versus':
            rival = request.form.get('rival')
            comp_text = request.form.get('comparacion')
            
            active_history.append({"role": "user", "content": f"Comparar con {rival}"})
            active_history.append({"role": "bot", "type": "simple", "content": f" **Comparativa:** {comp_text}"})
            session.modified = True
            return redirect(url_for('index'))

        # H. REINICIAR CHAT ACTUAL
        elif request.form.get('next_step') == 'reset':
            session['chats'][current_id] = create_new_chat_history()
            session.modified = True
            return redirect(url_for('index'))

        # I. FLUJO NORMAL DEL ÁRBOL
        else:
            next_step = request.form.get('next_step')
            user_text = request.form.get('user_text')
            
            # Opción "Ver otro ejemplo aleatorio"
            if next_step == 'reload_example':
                 last_msg = active_history[-1]
                 if last_msg['type'] == 'result':
                     algo_name = last_msg['algo']
                     if data_ml.get(algo_name):
                        new_example = random.choice(data_ml[algo_name])
                        active_history[-1]['example'] = new_example
                        session.modified = True
                 return redirect(url_for('index'))

            # 1. Guardar mensaje del usuario
            if user_text:
                active_history.append({"role": "user", "content": user_text})

            # 2. Generar respuesta del Bot
            if next_step in logic_tree:
                step_data = logic_tree[next_step]
                active_history.append({
                    "role": "bot",
                    "type": "question",
                    "content": step_data["pregunta"],
                    "options": step_data["opciones"]
                })
            
            elif next_step and next_step.startswith('res_'):
                algo_name = next_step.replace('res_', '')
                # Verificar que existe en la base de conocimientos
                if algo_name in data_ml and data_ml[algo_name]:
                    ejemplo = random.choice(data_ml[algo_name])
                    active_history.append({
                        "role": "bot",
                        "type": "result",
                        "algo": algo_name,
                        "example": ejemplo
                    })

            session.modified = True
            return redirect(url_for('index'))

    # Renderizar plantilla pasando variables necesarias
    return render_template('index.html', 
                           history=session['chats'][session['active_chat']], 
                           chats=session['chats'], 
                           active_chat=session['active_chat'],
                           user_level=user_level,
                           progress=progress)

# ==========================================
# 3. RUTA ADMIN (Dashboard)
# ==========================================
@app.route('/admin')
def admin_panel():
    stats = {}
    total_votes = 0
    try:
        with open('feedback_log.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(' | ')
                if len(parts) >= 2:
                    vote = parts[0].split(': ')[1]
                    algo = parts[1].split(': ')[1]
                    
                    if algo not in stats: stats[algo] = {'likes': 0, 'dislikes': 0}
                    if vote == 'LIKE': stats[algo]['likes'] += 1
                    elif vote == 'DISLIKE': stats[algo]['dislikes'] += 1
                    total_votes += 1
    except: pass

    # Calcular porcentajes
    for algo in stats:
        total = stats[algo]['likes'] + stats[algo]['dislikes']
        stats[algo]['percent'] = int((stats[algo]['likes'] / total * 100)) if total > 0 else 0

    return render_template('admin.html', stats=stats, total=total_votes)

if __name__ == '__main__':
    app.run(debug=True)