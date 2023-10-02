import re
import logging

logging.basicConfig(filename='normalization.log', level=logging.INFO)

# Normalize Business Names (using Eli's function)
def standardizeName(name:str) -> str:
    """
    Normalize business names by converting to lowercase, replacing '&' with 'and', removing special characters,
    and removing extra whitespace. If the business name is empty after normalization, it is considered invalid
    and None is returned.

    Parameters:
    name: Business name to normalize

    Returns:
    Normalized business name or None if invalid
    """
    name = name.lower()                 
    name = re.sub('&', ' and ', name)   
    name = re.sub('[^a-z\s-]', '', name)   
    name = re.sub(' {2,}', ' ', name)     
    return name.strip()

# Normalize Addresses using regex 
def normalize_address(address:str) -> str | None:
    """
    Normalize addresses by converting to lowercase, removing whitespace, and removing special characters except
    ., -, and #. If the address does not match the pattern of a valid address, it is considered invalid and
    None is returned.

    Parameters:
    address: Address to normalize

    Returns:
    Normalized address or None if invalid
    """
    
    pattern = r'^\d+\s[A-Za-z0-9\s\.\-]+(?:\s(?:Apt|Suite|Ste)\s\d+)?$'
    
    if re.match(pattern, address):
      
        logging.info(f"Normalized Address: {address}")
        return address
    else:
       
        logging.error(f"Invalid Address: {address}")
        return None  


def normalize_url(url:str) -> str | None:
    """
    Normalize URLs by converting to lowercase, removing whitespace, and removing special characters except
    ., -, and #. If the URL does not match the pattern of a valid URL, it is considered invalid and
    None is returned.

    Parameters:
    url: URL to normalize

    Returns:
    Normalized URL or None if invalid
    """
   
    url = url.lower()
    
    url = url.replace(" ", "")
    
    
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
  
    logging.info(f"Normalized URL: {url}")
    
    return url

# Example usage
if __name__ == "__main__":
    
    business_name = "Example & Co."
    print("Normalized Business Name:", standardizeName(business_name))

    address = "123 Main St Apt 456"
    print("Normalized Address:", normalize_address(address))

    url = "www.Example.com"
    print("Normalized URL:", normalize_url(url))
