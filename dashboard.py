from flask import Flask, render_template_string, jsonify
import threading

app = Flask(__name__)

# Variável global para armazenar o último comando executado
latest_command = "[MAESTRO] Sistema Inicializado. Aguardando gestos..."

index_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maestro Virtual - HUD</title>
    <style>
        body {
            background-color: #000000;
            color: #00FF66;
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 100vh;
        }
        .container {
            border: 2px solid #00FF66;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 255, 102, 0.4);
        }
        h2 { font-size: 1.1rem; border-bottom: 1px dashed #00FF66; padding-bottom: 10px; margin-top: 0; }
        #status { font-size: 1.3rem; font-weight: bold; margin-top: 15px; word-break: break-all; }
        .blink { animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="container">
        <h2>[MAESTRO VIRTUAL - HUD] <span class="blink">● REC</span></h2>
        <p>Status: Conectado e Ativo</p>
        <div id="status">Carregando...</div>
    </div>

    <script>
        setInterval(async () => {
            try {
                let response = await fetch('/get_status');
                let data = await response.json();
                document.getElementById('status').innerText = data.command;
            } catch (e) {
                document.getElementById('status').innerText = "[ERRO] Conexão perdida.";
            }
        }, 500);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(index_html)

@app.route('/get_status')
def get_status():
    global latest_command
    return jsonify({"command": latest_command})

def run_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_dashboard():
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

def update_hud(new_msg):
    global latest_command
    latest_command = new_msg