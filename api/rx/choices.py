from django.db.models import TextChoices


class MeasurementUnit(TextChoices):
    UNKNOWN = "?", "?"

    UNIT = "unit", "unit"

    PERCENT_WV = "wv", "% w/v"
    PERCENT_WW = "ww", "% w/w"

    MCG = "mcg", "μg"
    MG = "mg", "mg"
    G = "g", "g"

    ML = "ml", "ml"
    L = "l", "l"
