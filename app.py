import os
import secrets
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import DAL

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Upload configuration
app.config["UPLOAD_FOLDER"] = Path("static/images")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB max file size
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file_storage):
    if not file_storage or file_storage.filename == "":
        raise ValueError("No file selected")
    if not allowed_file(file_storage.filename):
        raise ValueError("Invalid file type. Allowed: png, jpg, jpeg, gif, webp")
    filename = secure_filename(file_storage.filename)
    upload_folder = Path(app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)
    filepath = upload_folder / filename
    if filepath.exists():
        name, ext = filename.rsplit(".", 1)
        unique_suffix = secrets.token_hex(3)
        filename = f"{name}__{unique_suffix}.{ext}"
        filepath = upload_folder / filename
    file_storage.save(str(filepath))
    return filename

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/projects')
def projects():
    projects_list = DAL.get_projects()
    return render_template('projects.html', projects=projects_list)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'GET':
        return render_template('project_form.html')
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        image_file = request.files.get('image')
        if not title:
            flash('Title is required', 'error')
            return render_template('project_form.html'), 400
        if not description:
            flash('Description is required', 'error')
            return render_template('project_form.html'), 400
        if not image_file:
            flash('Image is required', 'error')
            return render_template('project_form.html'), 400
        stored_filename = save_image(image_file)
        DAL.insert_project(title, description, stored_filename)
        flash('Project added successfully!', 'success')
        return redirect(url_for('projects'))
    except ValueError as e:
        flash(str(e), 'error')
        return render_template('project_form.html'), 400
    except Exception as e:
        flash(f'Error adding project: {str(e)}', 'error')
        return render_template('project_form.html'), 500

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    DAL.init_db()
    projects_list = DAL.get_projects()
    if len(projects_list) == 0:
        print("Seeding database...")
        DAL.insert_project("FCRE Racing Website", "A seven-page website built with HTML, CSS, and Bootstrap for FCRE (Four Circles Racing Events).", "fcre home.png")
        DAL.insert_project("iPhone Recommender Chatbot", "A Dialogflow chatbot that recommends iPhone models based on user preferences.", "chatbot1.png")
        print("Database seeded!")
    app.run(debug=True)
