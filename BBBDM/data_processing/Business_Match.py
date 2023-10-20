from fuzzywuzzy import fuzz

def is_same_business(historical_name: str, new_name: str, threshold: int = 80) -> bool:
    """
    Check if the new business name is essentially the same as the historical one.
    Uses fuzzy string matching to make this determination.
    """
    
    # Ensuring our inputs are strings, just in case!
    historical_name = str(historical_name).lower()
    new_name = str(new_name).lower()

    # Casting threshold to integer to make sure our comparisons are consistent.
    threshold = int(threshold)

    # Token match ratio
    token_ratio = fuzz.token_sort_ratio(historical_name, new_name)

    # Regular fuzzy match ratio
    fuzzy_ratio = fuzz.ratio(historical_name, new_name)
    
    # Partial match ratio
    partial_ratio = fuzz.partial_ratio(historical_name, new_name)

    # Return True if any of the above ratios exceed the threshold
    return any(ratio >= threshold for ratio in [token_ratio, fuzzy_ratio, partial_ratio])
