import os
import glob
from django.core.management.base import BaseCommand
from chemistry.models import MLModelMetadata

class Command(BaseCommand):
    help = 'Scans OneDrive for .joblib models and their scalers'

    def handle(self, *args, **options):
        # 1. Define the absolute path to your OneDrive
        model_folder = r"C:\Users\ivano\OneDrive\Self-appeared\Documents"
        
        # 2. Search for all .joblib files in all subfolders
        search_pattern = os.path.join(model_folder, "**", "*.joblib")
        file_list = glob.glob(search_pattern, recursive=True)

        self.stdout.write(f"Found {len(file_list)} potential files. Syncing...")

        for file_path in file_list:
            # Skip files that are actually scalers so we don't register them as models
            if "scaler" in file_path.lower():
                continue

            # --- FIXING THE ORANGE UNDERLINE ---
            # We use 'model_name' consistently here
            model_name = os.path.basename(file_path).replace('.joblib', '')
            
            # --- SCALER DISCOVERY ---
            # Look for 'scaler.joblib' in the same folder as this specific model
            folder_path = os.path.dirname(file_path)
            potential_scaler = os.path.join(folder_path, "scaler.joblib")
            found_scaler = potential_scaler if os.path.exists(potential_scaler) else None

            # --- DATABASE UPDATE ---
            # Using 'model_name' here fixes the error
            obj, created = MLModelMetadata.objects.update_or_create(
                joblib_path=file_path,
                defaults={
                    'target_functionality': model_name, # Change 'name' to 'target_functionality'
                    'training_accuracy': 0.0,
                    'training_f1_score': 0.0,
                         }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {model_name}"))
            else:
                self.stdout.write(f"🔄 Updated: {model_name} (Scaler: {found_scaler is not None})")

        self.stdout.write(self.style.SUCCESS("Sync complete! Check Django Admin."))