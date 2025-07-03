from flask import Flask, render_template, request, jsonify
import io, contextlib, base64, os, uuid, pandas as pd, matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get("code", "")
    stdout = io.StringIO()
    img_data = ""

    try:
        with contextlib.redirect_stdout(stdout):
            globals_dict = {
                '__builtins__': __builtins__,
                'pd': pd,
                'plt': plt
            }
            exec(code, globals_dict)
            if plt.get_fignums():
                img_path = f'static/{uuid.uuid4().hex}.png'
                plt.savefig(img_path)
                with open(img_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode()
                plt.close('all')
    except Exception as e:
        return jsonify({"output": str(e), "plot": ""})

    return jsonify({"output": stdout.getvalue(), "plot": img_data})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    ext = os.path.splitext(file.filename)[1]
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)
    return jsonify({"message": f"Uploaded: {file.filename}", "path": save_path, "ext": ext})

if __name__ == '__main__':
    app.run(debug=True)
