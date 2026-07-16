def calculate_bmi(
    weight_kg: float | None,
    height_cm: float | None,
) -> float | None:
    
    if weight_kg is None or height_cm is None:
        return None
    
    if height_cm <+ 0:
        return None
    
    height_m = height_cm / 100
    
    bmi = weight_kg / (height_m ** 2)
    
    return round(bmi, 2)