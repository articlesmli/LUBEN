import joblib
import os
from chemistry.models import MLModelMetadata
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nmr_site.settings')
django.setup()

def check_models():
    models = MLModelMetadata.objects.all()
    if not models:
        print("No models found in database.")
        return

    for m in models:
        print(f"\n--- Checking Model: {m.target_functionality} ---")
        if os.path.exists(m.joblib_path):
            model = joblib.load(m.joblib_path)
            
            # Check expected input size
            if hasattr(model, 'n_features_in_'):
                print(f"Expected Input Features: {model.n_features_in_}")
            elif hasattr(model, 'feature_names_in_'):
                print(f"Expected Input Features: {len(model.feature_names_in_)}")
            else:
                print("Could not automatically determine feature count.")
            
            # Check internal metadata
            print(f"Model Type: {type(model).__name__}")
            print(f"Stored Accuracy in DB: {m.training_accuracy}")
        else:
            print(f"FILE NOT FOUND: {m.joblib_path}")

if __name__ == "__main__":
    check_models()