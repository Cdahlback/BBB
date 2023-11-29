from fuzzywuzzy import fuzz

# Function to determine if two business names represent the same business entity
def is_same_business(
    historical_name: str,
    new_name: str,
    threshold: int = 80,
    business_type_historical: str = None,
    business_type_new: str = None,
    is_SOS: bool = False,
) -> bool:
    """
    This function uses fuzzy string matching to compare two business names (or email domains)
    and determine if they are essentially the same, considering various factors like business type.
    """

    # Helper function to preprocess business names by removing common suffixes and converting to lowercase
    def preprocess_name(name: str) -> str:
        name = name.lower()
        # Removes common business suffixes if the name is not from SOS (Secretary of State)
        for suffix in ["inc", "llc", "ltd", "co", ".", ",", "&", "corp", "incorporation"]:
            name = name.replace(suffix, "")
        return name.strip()

    # Preprocess names if not from SOS
    if not is_SOS:
        historical_name = preprocess_name(historical_name)
        new_name = preprocess_name(new_name)

    # Return False immediately if business types are provided and they do not match
    if business_type_historical and business_type_new and business_type_historical != business_type_new:
        return False

    # Calculate fuzzy matching ratios to compare the two names
    token_ratio = fuzz.token_sort_ratio(historical_name, new_name)
    fuzzy_ratio = fuzz.ratio(historical_name, new_name)
    partial_ratio = fuzz.partial_ratio(historical_name, new_name)

    # Return True if any of the fuzzy matching ratios exceed the given threshold
    return any(ratio >= threshold for ratio in [token_ratio, fuzzy_ratio, partial_ratio])

# Function to validate an email by comparing it against historical email and business name
def validate_email(historical_email, historical_name, new_email):
    
    """
    Validates a new email by comparing it to a historical email. If they are not the same,
    it checks if their domains represent the same business entity
    """

    # Check if the new email is exactly the same as the historical email
    if new_email == historical_email:
        return True

    # Extract the domain part of both new and historical emails
    new_email_domain = new_email.split("@")[-1]
    historical_email_domain = historical_email.split("@")[-1]

    # Use the is_same_business function to compare the domains of the emails
    # to see if they are from the same business entity
    return is_same_business(historical_email_domain, new_email_domain, business_type_historical=historical_email_domain, business_type_new=new_email_domain)
