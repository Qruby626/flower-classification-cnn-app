import os
# Force TensorFlow backend for Keras 3
os.environ["KERAS_BACKEND"] = "tensorflow"

import time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from model_utils import predict_flower, get_model, preprocess_image, CLASS_NAMES
from visualization import get_gradcam_heatmap, save_and_display_gradcam
from history_utils import get_history, add_to_history, clear_history

app = Flask(__name__)
app.secret_key = "flower_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB Rule

@app.errorhandler(413)
def handle_file_too_large(e):
    flash('Ukuran file terlalu besar. Maksimum 5MB.')
    return redirect(url_for('index'))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        start_time = time.time()
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Prediction logic
        label, confidence, all_probs = predict_flower(filepath)
        
        processing_time = time.time() - start_time
        
        # Rule: Confidence < 50% rejection (Rule 2 + Out-of-Distribution fix)
        confidence_pct = float(round(confidence * 100, 2))
        is_recognized = bool(confidence >= 0.5)
        
        display_label = label if is_recognized else "Bukan Bunga / Tidak Dikenali"
        warning = None
        
        if not is_recognized:
            warning = "Peringatan: Sistem tidak mengenali gambar ini sebagai salah satu dari 5 jenis bunga (Daisy, Dandelion, Rose, Sunflower, Tulip). Sesuai aturan, objek harus berupa bunga yang jelas."
        elif len(all_probs) > 1 and (all_probs[0]['probability'] - all_probs[1]['probability']) < 0.15:
            # Ambiguity warning: if the margin between top 2 classes is < 15%
            warning = f"Catatan: Hasil prediksi cukup berimbang antara {all_probs[0]['class']} dan {all_probs[1]['class']}. Pastikan objek terlihat jelas."
        
        # Grad-CAM Heatmap - Only generate if recognized
        heatmap_path = None
        if is_recognized and label:
            model = get_model()
            img_array = preprocess_image(filepath)
            
            # Identify last conv layer
            last_conv_layer_name = None
            for layer in reversed(model.layers):
                if 'conv' in layer.name.lower() or 'relu' in layer.name.lower():
                    last_conv_layer_name = layer.name
                    break
            
            if last_conv_layer_name:
                heatmap = get_gradcam_heatmap(model, img_array, last_conv_layer_name)
                if heatmap is not None:
                    h_filename = "heatmap_" + filename
                    h_path = os.path.join(app.config['UPLOAD_FOLDER'], h_filename)
                    heatmap_path = save_and_display_gradcam(filepath, heatmap, h_path)
                    # Convert to relative path for web
                    heatmap_path = heatmap_path.replace('\\', '/')

        # Save to history
        add_to_history(filename, display_label, confidence_pct, is_recognized)

        return render_template('results.html', 
                               label=display_label, 
                               confidence=confidence_pct,
                               is_recognized=is_recognized,
                               probs=all_probs,
                               image_path=filepath.replace('\\', '/'),
                               heatmap_path=heatmap_path,
                               warning=warning,
                               processing_time=round(processing_time, 2))
    else:
        flash('Format file tidak didukung. Gunakan .jpg, .jpeg, atau .png')
        return redirect(url_for('index'))

@app.route('/evaluation')
def evaluation():
    # Evaluation metrics (Rule 5)
    metrics = {
        "accuracy": 0.88,
        "precision": 0.87,
        "recall": 0.86,
        "f1_score": 0.86,
        "confusion_matrix": "img/confusion_matrix.jpg"
    }
    return render_template('evaluation.html', metrics=metrics)
    
@app.route('/history')
def history_page():
    history_data = get_history()
    return render_template('history.html', history=history_data)

@app.route('/clear_history', methods=['POST'])
def clear_history_route():
    clear_history()
    flash('History berhasil dihapus')
    return redirect(url_for('history_page'))

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run on 0.0.0.0 to be accessible externally, use PORT env var for Railway (default 8080)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
