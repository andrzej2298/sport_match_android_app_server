from django.core.validators import MinValueValidator, MaxValueValidator

PROFICIENCY_VALIDATORS = [MinValueValidator(0), MaxValueValidator(2)]
AGE_VALIDATORS = [MinValueValidator(0), MaxValueValidator(120)]
MAX_PEOPLE_VALIDATORS = [MinValueValidator(2)]
