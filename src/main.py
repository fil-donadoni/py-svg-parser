import sys
from PIL import Image
import pytesseract
import cairosvg

correct_values = {
    1: 0.84,
    2: 35.99,
    3: 32.01,
    4: 1.65,
    5: 0.001
}

def svg_to_png(input_svg, output_png):
    try:
        cairosvg.svg2png(url=input_svg, write_to=output_png)
        # print(f"Rasterization successful. PNG file saved at: {output_png}")
    except Exception as e:
        print(f"Rasterization failed: {str(e)}")

if(len(sys.argv) >= 2):
    psm_value = sys.argv[1]
else:
    psm_value = '6'

psm = '--psm ' + psm_value
print('PSM ', psm)

def ocr_from_image(image_path):
    text = pytesseract.image_to_string(Image.open(image_path), config=psm)

    return text.strip()

def force_number(string):
    if((string[0] == '0' or string[0] == 'O') and string[1] != '.'):
        new_string = string[0] + '.' + string[1:]
    else:
        new_string = string

    # Remove non-numeric characters (excluding the decimal point)
    numeric_string = ''.join(char for char in new_string if char.isdigit() or char == '.')

    return float(numeric_string)

for file, expected_value in correct_values.items():
    print(f'{file}.svg')
    print(f'Expected value: {expected_value}')

    svg_file_path = '/code/src/' + str(file) + '.svg'
    output_png_path = '/code/src/price.png'

    svg_to_png(svg_file_path, output_png_path)
    extracted_number = force_number(ocr_from_image(output_png_path))

    print(f"#Output number: {extracted_number}")

    if(extracted_number == expected_value):
        print('BENE!')
    else:
        print('NOOOOOOOOOOOOOOOOOO')
