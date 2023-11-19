from fuzzywuzzy import fuzz


def is_same_business(
    historical_name: str,
    new_name: str,
    threshold: int = 80,
    business_type_historical: str = None,
    business_type_new: str = None,
    is_SOS: bool = False,
) -> bool:
    """
    Check if the new business name is essentially the same as the historical one.
    Uses fuzzy string matching to make this determination. If the names are not from SOS,
    removes common business suffixes before comparing.
    """

    def preprocess_name(name: str) -> str:
        # Convert to lowercase
        name = name.lower()
        # If not from SOS, remove common business suffixes
        for suffix in ["inc", "llc", "ltd", "co", ".", ",", "&", "corp", "incorporation"]:
            name = name.replace(suffix, "")
        return name.strip()

    if not is_SOS:
        historical_name = preprocess_name(historical_name)
        new_name = preprocess_name(new_name)

    # Check business types
    if business_type_historical and business_type_new and business_type_historical != business_type_new:
        return False

    # Fuzzy matching ratios
    token_ratio = fuzz.token_sort_ratio(historical_name, new_name)
    fuzzy_ratio = fuzz.ratio(historical_name, new_name)
    partial_ratio = fuzz.partial_ratio(historical_name, new_name)

    # Check if any ratio exceeds the threshold
    return any(ratio >= threshold for ratio in [token_ratio, fuzzy_ratio, partial_ratio])

def validate_email(historical_email: str, historical_name: str, new_email: str) -> bool:
    """
    Validate the new email by comparing it against the historical email and name.
    """
    # Check if emails are exactly the same
    if new_email == historical_email:
        return True
    
    # Extract domain from new email
    new_email_domain = new_email.split("@")[-1]
    historical_email_domain = historical_email.split("@")[-1]

    # Use the is_same_business function to compare domains
    return is_same_business(historical_name, new_email_domain, business_type_historical=historical_email_domain, business_type_new=new_email_domain)

