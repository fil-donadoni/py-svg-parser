import base64
from io import BytesIO
from PIL import Image
import pytesseract
import cairosvg

correct_values = {
    1: 0.84,
    2: 35.99,
    3: 32.01,
    4: 1.65,
    5: 0.001,
    6: 28.01,
}

def svg_to_png(input_svg, output_png = None):
    if output_png:
        try:
            cairosvg.svg2png(bytestring=input_svg, write_to=output_png)
            # print(f"Rasterization successful. PNG file saved at: {output_png}")
        except Exception as e:
            print(f"Rasterization failed: {str(e)}")
    else:
        try:
            png_bytes = cairosvg.svg2png(bytestring=input_svg)

            png_base64 = base64.b64encode(png_bytes).decode('utf-8')

            # print(f"Rasterization successful. PNG file saved at: {output_png}")

            return png_base64
        except Exception as e:
            print(f"Rasterization failed: {str(e)}")

def svg_file_to_png(input_svg_file, output_png = None):
    if output_png:
        try:
            cairosvg.svg2png(url=input_svg_file, write_to=output_png)
            # print(f"Rasterization successful. PNG file saved at: {output_png}")
        except Exception as e:
            print(f"Rasterization failed: {str(e)}")
    else:
        try:
            png_bytes = cairosvg.svg2png(url=input_svg_file)

            png_base64 = base64.b64encode(png_bytes).decode('utf-8')

            # print(f"Rasterization successful. PNG file saved at: {output_png}")

            return png_base64
        except Exception as e:
            print(f"Rasterization failed: {str(e)}")

def ocr_from_image(image_path = None, base64 = None):
    if image_path:
        text = pytesseract.image_to_string(Image.open(image_path), config='--psm 6')
    else:
        # print(base64)
        image = base64_to_image(base64)
        text = pytesseract.image_to_string(image, config='--psm 6')
        
    return text.strip()
        

def force_number(string):
    if(len(string) and (string[0] == '0' or string[0] == 'O') and string[1] != '.'):
        new_string = string[0] + '.' + string[1:]
    else:
        new_string = string

    # Remove non-numeric characters (excluding the decimal point)
    numeric_string = ''.join(char for char in new_string if char.isdigit() or char == '.')

    if numeric_string:
        return float(numeric_string)
    else:
        return None

def base64_to_image(base64_string):   
    image_data = base64.b64decode(base64_string)
    image_stream = BytesIO(image_data)
    image_stream.seek(0)  # Move to the beginning of the stream
    image = Image.open(image_stream)

    return image

for file, expected_value in correct_values.items():
    print(f'{file}.svg')
    print(f'Expected value: {expected_value}')

    svg_file_path = '/code/src/' + str(file) + '.svg'
    output_png_path = '/code/src/price.png'

    png_base64 = svg_file_to_png(svg_file_path)
    extracted_number = force_number(ocr_from_image(base64=png_base64))

    print(f"#Output number: {extracted_number}")

    if(extracted_number == expected_value):
        print('BENE!')
    else:
        print('NOOOOOOOOOOOOOOOOOO')
