from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import NMRTest, MLModelMetadata, PredictionHistory
import joblib
import numpy as np
import os
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def get_predictions(peak_string):
    # Create a mapping of Model Name -> Definition
    DEFINITIONS = {
        'model_D1': 'D1 Dopamine Receptor Antagonism: Measures the blocking effect on D1 signaling.',
        'model_CHOP': 'CHOP Inhibition: Evaluation of ER-stress induced apoptosis pathways.',
    }
    
    results = []
    
    # 1. Strip whitespace and newlines
    peak_string = peak_string.strip()

    if ',' in peak_string:
        # Handle comma-separated floats
        raw_data = [float(x.strip()) for x in peak_string.split(',') if x.strip()]
    else:
        # Handle bitstrings (ignores \r, \n)
        raw_data = [float(char) for char in peak_string if char.isdigit()]
    
    if not raw_data:
        return []

    input_data = np.array(raw_data).reshape(1, -1)
    all_models = MLModelMetadata.objects.all()

    for m in all_models:
        if os.path.exists(m.joblib_path):
            model = joblib.load(m.joblib_path)
            
            # Scaling logic
            if m.scaler_path and os.path.exists(m.scaler_path):
                scaler = joblib.load(m.scaler_path)
                processed_data = scaler.transform(input_data)
            else:
                processed_data = input_data
            
            prediction = model.predict(processed_data)[0]
            results.append({
                'functionality': m.target_functionality,
                'definition': DEFINITIONS.get(m.target_functionality, "No description available."),
                'prediction': "Positive" if prediction == 1 else "Negative",
                'accuracy': f"{m.training_accuracy * 100:.1f}%",
                'f1': m.training_f1_score
            })
    return results

def predict_compound(request):
    models = MLModelMetadata.objects.all()

    results = []
    compound_name = ""
    peak_string = ""
    test_id = None  # Initialize to prevent UnboundLocalError

    if request.method == "POST":
        compound_name = request.POST.get('compound_name')
        peak_string = request.POST.get('peak_string')

        try:
            # 1. Save to DB first to get an ID
            new_test = NMRTest.objects.create(
                compound_name=compound_name,
                peak_string=peak_string
            )
            test_id = new_test.id
            
            # 2. Get ML Results
            results = get_predictions(peak_string)

            PredictionHistory.objects.create(
                compound_name=compound_name,
                peak_string=peak_string,
                prediction_results=str(results)
            )

        except Exception as e:
            messages.error(request, f"Error processing data: {e}")

    return render(request, 'chemistry/predict.html', {
        'models': models,
        'results': results,
        'compound_name': compound_name,
        'peak_string': peak_string,
        'test_id': test_id, # Passed to fix NoReverseMatch
    })

def export_pdf(request, test_id):
    test = get_object_or_404(NMRTest, id=test_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{test.compound_name}_report.pdf"'
    
    styles = getSampleStyleSheet()
    elements = []
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Header
    elements.append(Paragraph(f"Chemical Analysis Report: {test.compound_name}", styles['Title']))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Generate fresh predictions for the report
    results = get_predictions(test.peak_string)

    data = [['Target Functionality', 'Result', 'Model Accuracy']]
    for res in results:
        data.append([res['functionality'], res['prediction'], res['accuracy']])

    report_table = Table(data, colWidths=[200, 100, 100])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(report_table)
    doc.build(elements)
    return response

def history_list(request):
    tests = NMRTest.objects.all().order_by('-created_at')
    return render(request, 'chemistry/history.html', {'tests': tests})

def model_list_view(request):
    # Fetch EVERY model found by your scan command
    all_models = MLModelMetadata.objects.all() 
    return render(request, 'your_template.html', {'models': all_models})

