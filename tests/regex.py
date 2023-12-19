import re

# pattern = r'\b(IMG_\d{4}|DSC\d{5}|P\d{7}|DSC_\d{4})\b'
# pattern = r'(\w{3}_\d{4}|\w{3}\d{5})'
def find_image_names(text):
    pattern = r'\b(IMG_\d{4}|DSC\d{5}|P\d{7}|DSC_\d{4})\b'
    matches = re.findall(pattern, text)
    return matches

# Example usage:
text = "I found these images: IMG_1234.JPG, DSC01234.JPG, DSC01664_copy.JPG, P1234567.JPG, and some_random_image.JPG."
print(find_image_names(text))  # Output: ['IMG_1234', 'DSC01234', 'P1234567']


"""
DSC_xxxx - Sony, Nikon
DSCNxxxx - Nikon
DSCFxxxx - Fuji
DSCxxxxx - Sony mirrorless and point and shoot / action models, Nikon depending on color space used
Pxxxxxxx - Panasonic Lumix, Olymupus Tough
_DSCxxxx - Sony a6000
_MG_xxxx - Canon EOS
IMG_xxxx - Canon EOS
DJI_xxxx - DJI Mavic 2 Pro
_AAA1111 - configurable canon format
"""