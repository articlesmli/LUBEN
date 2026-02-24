from django.db import models

class MLModelMetadata(models.Model):  # <--- Make sure this name matches
    target_functionality = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    joblib_path = models.CharField(max_length=500)
    scaler_path = models.CharField(max_length=500, null=True, blank=True)
    training_accuracy = models.FloatField(default=0.0)
    training_f1_score = models.FloatField(default=0.0)

    def __str__(self):
        # Corrected: Use target_functionality instead of name
        return f"{self.target_functionality}"

class NMRTest(models.Model):
    """Stores the actual compound data you want to test"""
    compound_name = models.CharField(max_length=230)
    # TextField allows for the very long 0000... string
    peak_string = models.TextField(help_text="Paste your 000... string here")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.compound_name
    
class PredictionHistory(models.Model):
    compound_name = models.CharField(max_length=255)
    peak_string = models.TextField()
    prediction_results = models.TextField() # Or JSONField
    created_at = models.DateTimeField(auto_now_add=True)

