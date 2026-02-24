import os
import joblib
from django.core.management.base import BaseCommand
from chemistry.models import MLModelMetadata

class Command(BaseCommand):
    help = 'Scans subfolders for models and scalers and updates the database'

    def handle(self, *args, **options):
        # Set your particular base folder here
        base_path = '/path/to/your/main/folder' 
        
        for root, dirs, files in os.walk(base_path):
            # 1. Identify all .joblib files that aren't scalers
            models = [f for f in files if f.endswith('.joblib') and 'scaler' not in f.lower()]
            
            for model_file in models:
                model_path = os.path.join(root, model_file)
                
                # 2. Look for a scaler in the same subfolder
                scaler_path = None
                if 'scaler.joblib' in files:
                    scaler_path = os.path.join(root, 'scaler.joblib')
                
                # 3. Create a clean name from the filename
                clean_name = model_file.replace('.joblib', '').replace('_', ' ').title()

                # 4. Update the Database
                MLModelMetadata.objects.update_or_create(
                    joblib_path=model_path,
                    defaults={
                        'target_functionality': clean_name,
                        'scaler_path': scaler_path,
                        'training_accuracy': 0.85, # Replace with logic to load real metrics if available
                        'training_f1_score': 0.84
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Synced: {clean_name} (Scaler: {scaler_path is not None})'))