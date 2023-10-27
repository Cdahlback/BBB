from fuzzywuzzy import fuzz

def is_same_business(historical_name: str, new_name: str, threshold: int = 80, 
                     business_type_historical: str = None, business_type_new: str = None, 
                     is_SOS: bool = False) -> bool:
    """
    Check if the new business name is essentially the same as the historical one.
    Uses fuzzy string matching to make this determination. If the names are not from SOS, 
    removes common business suffixes before comparing.
    """
    
    # Helper function to preprocess names
    def preprocess_name(name: str) -> str:
        # Convert to lowercase
        name = name.lower()
        
        # If not from SOS, remove common business suffixes
        for suffix in ["inc", "llc", "ltd", "co", ".", ",", "&", "corp", "incorporation"]:
            name = name.replace(suffix, "")
        
        return name.strip()

    # If not from SOS, preprocess the business names" 
    if not is_SOS:
        historical_name = preprocess_name(historical_name)
        new_name = preprocess_name(new_name)
    
    # If business types are provided and they don't match, return False immediately
    if business_type_historical and business_type_new and business_type_historical != business_type_new:
        return False

    # Token match ratio
    token_ratio = fuzz.token_sort_ratio(historical_name, new_name)

    # Regular fuzzy match ratio
    fuzzy_ratio = fuzz.ratio(historical_name, new_name)
    
    # Partial match ratio
    partial_ratio = fuzz.partial_ratio(historical_name, new_name)

    # Return True if any of the above ratios exceed the threshold
    return any(ratio >= threshold for ratio in [token_ratio, fuzzy_ratio, partial_ratio])
