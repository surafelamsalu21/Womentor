from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from app.models import process_resume, evaluate_resume_with_openai
import os
import json

routes = Blueprint('routes', __name__)
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@routes.route('/results', methods=['POST'])
def results():
    """Handle the resume upload and evaluation."""
    if 'file' not in request.files:
        flash('No file part in the request.')
        return redirect(url_for('routes.home'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected.')
        return redirect(url_for('routes.home'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Process the resume and extract text
            resume_content = process_resume(file_path)
            if not resume_content.strip():
                flash("The uploaded file does not contain valid content. Please upload a valid resume.")
                return redirect(url_for('routes.home'))

            # Evaluate the resume using OpenAI
            openai_response = evaluate_resume_with_openai(resume_content)
            if not openai_response.strip():
                flash("OpenAI API returned an empty response. Please try again.")
                return redirect(url_for('routes.home'))

            # Parse the cleaned response
            try:
                evaluation = json.loads(openai_response)
            except json.JSONDecodeError:
                flash("Invalid response from OpenAI. Please try again later.")
                return redirect(url_for('routes.home'))

            # Calculate score and average
            try:
                score = sum(10 for key, value in evaluation.items() if value == "Yes")
                total_criteria = len([key for key in evaluation if key.endswith("_reasoning")])
                average_score = (score / (total_criteria * 10)) * 100 if total_criteria > 0 else 0
            except Exception as e:
                flash(f"An error occurred during score calculation: {str(e)}")
                return redirect(url_for('routes.home'))

            # Pass the evaluation results to the template
            return render_template(
                'results.html',
                evaluation=evaluation,
                criteria_evaluation=evaluation,  # Pass as criteria_evaluation for compatibility
                score=f"{score} / {total_criteria * 10} ({average_score:.2f}%)"
            )

        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for('routes.home'))

    flash('Invalid file type.')
    return redirect(url_for('routes.home'))
