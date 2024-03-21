import re

raw_text = '<div><span class="actionBar__text"> Showing 18 of 101 products.</span></div>'
pattern = r'\b(\d+)\s+products\b'

matches = re.search(pattern, raw_text)
if matches:
    total_products = matches.group(1)
    print("Total number of products:", total_products)
else:
    print("No match found.")
