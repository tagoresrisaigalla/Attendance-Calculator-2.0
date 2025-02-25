import numpy as np

def calculate_current_percentage(classes_attended, total_classes):
    """Calculate current attendance percentage"""
    if total_classes == 0:
        return 0
    return (classes_attended / total_classes) * 100

def calculate_future_percentage(current_attended, current_total, future_attend, future_total):
    """Calculate future attendance percentage"""
    total_attended = current_attended + future_attend
    total_classes = current_total + future_total
    return calculate_current_percentage(total_attended, total_classes)

def calculate_classes_needed(current_attended, current_total, target_percentage):
    """Calculate classes needed to reach target percentage"""
    if target_percentage <= calculate_current_percentage(current_attended, current_total):
        return 0
    
    target_decimal = target_percentage / 100
    classes_needed = np.ceil((target_decimal * current_total - current_attended) / (1 - target_decimal))
    return int(max(0, classes_needed))

def calculate_classes_can_bunk(current_attended, current_total, target_percentage):
    """Calculate how many future classes can be bunked while maintaining target percentage"""
    current_percentage = calculate_current_percentage(current_attended, current_total)
    
    if target_percentage >= current_percentage:
        return 0
    
    target_decimal = target_percentage / 100
    # Calculate maximum classes that can be missed while staying above target
    bunkable_classes = int((current_attended - (target_decimal * current_total)) / target_decimal)
    return max(0, bunkable_classes)

def generate_scenarios(current_attended, current_total, future_classes):
    """Generate different attendance scenarios"""
    scenarios = []
    for attend in range(future_classes + 1):
        percentage = calculate_future_percentage(current_attended, current_total, attend, future_classes)
        scenarios.append({
            'classes_attended': attend,
            'total_classes': future_classes,
            'percentage': round(percentage, 2)
        })
    return scenarios