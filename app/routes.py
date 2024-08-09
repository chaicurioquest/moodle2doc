from flask import Blueprint, render_template, request, send_file, abort
import os
from app.document_generator import generate_document

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        xml_file = request.files['file']
        user_choices = request.form.getlist('choices')

        # Define the base directory (current script directory)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Ensure the 'uploaded_files' directory exists within the project directory
        upload_folder = os.path.join(base_dir, '..', 'uploaded_files')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        xml_path = os.path.join(upload_folder, xml_file.filename)
        xml_file.save(xml_path)

        # Ensure the 'output_doc' directory exists within the project directory
        output_folder = os.path.join(base_dir, '..', 'output_doc')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file = os.path.join(output_folder, 'output.docx')

        # Generate the document
        print(f"Generating document at: {output_file}")
        generate_document(xml_path, output_file, user_choices)

        # Check if the document was created
        if not os.path.exists(output_file):
            print(f"File not found after generation: {output_file}")
            abort(404, description="Document not found or failed to generate")

        print(f"Sending file: {output_file}")
        return send_file(output_file, as_attachment=True)

    return render_template('upload.html')
