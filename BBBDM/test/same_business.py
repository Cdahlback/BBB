import sys

# Add the project path to the system path for imports to work seamlessly
sys.path.append(r'C:\Users\tebib\OneDrive\Desktop\Project 1\BBB')

# Import the is_same_business function
from BBBDM.data_processing.Business_Match import is_same_business

def test_is_same_business():
    # Test cases for our function
    test_cases = [
        ("Bob's burgers", "Bob's burger and fries", True),          # Direct similarity
        ("coffee shop", "tea shop", False),                          # Clearly different
        ("MCDONALDS", "McDonald's", True),                           # Different case but same name
        ("Wendys", "Wendy's Hamburgers", True),                      # One name is substring of the other
        ("Dell Technologies", "Dell", True),                         # Partial match
        ("Apple Store", "Apple Orchard", False),                     # Different despite common word "Apple"
        ("Bobs Burgers and Fries", "Fries Bobs Burgers", True),      # Reordered tokens
        ("Burger Palace", "Burger Place", False),                    # One word different
        ("Best PC Ltd.", "Best PC", True),                           # Business suffix removed
        ("Baker & Sons, Inc.", "Baker and Sons", True),              # Suffix and symbols removed, and expanded
        ("Bob's Burgers", "Joe's Burgers", False),                   # Different business names
        ("World Electronics Corp.", "World Electrics", False),       # Small but significant word change
        ("Tech Gurus LLC", "Tech Guru", False),                      # Plurality difference
        ("Sunshine Bakery", "Moonlight Bakery", False),              # Opposite prefixes
        ("Shoe Factory", "Shoe Store", False)                        # Different business type despite same category
    ]

    # Iterating through each test case
    for hist_name, new_name, expected in test_cases:
        result = is_same_business(hist_name, new_name)
        
        # Asserting that our function's result matches the expected result
        assert result == expected, f"Expected {expected} but got {result} for historical '{hist_name}' and new '{new_name}'"
