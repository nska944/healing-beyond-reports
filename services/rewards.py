def calculate_badge(steps):
    if steps >= 10000:
        return "Champion"
    elif steps >= 5000:
        return "Active"
    elif steps >= 3000:
        return "Starter"
    return None
