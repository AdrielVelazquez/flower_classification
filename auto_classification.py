from PIL import Image
from collections import defaultdict

def create_graphed_image(picture):
	width, height = picture.size
	new_image = Image.new("RGB", (width, height))
	# Get the size of the image
	Primary_colors = defaultdict(int)
	# Process every pixel
	for x in range(width):
		previous_RGB_average = 0
		for y in range(height):
			current_color = picture.getpixel( (x,y) )
			current_color_average = sum(current_color)/3
			if abs(previous_RGB_average - current_color_average) > 15:
				new_image.putpixel((x, y), (255, 255, 255))
				Primary_colors["R"] += current_color[0]
				Primary_colors["G"] += current_color[1]
				Primary_colors["B"] += current_color[2]
				Primary_colors["C"] += 1
			previous_RGB_average = current_color_average
	new_image.save("trial_2.jpg")
	return Primary_colors
           
def calculate_primary_color(primary_dict):
	len_c = primary_dict["C"]
	R = primary_dict.get("R", 0)/len_c
	G = primary_dict.get("G", 0)/len_c
	B = primary_dict.get("B", 0)/len_c
	print R, G, B
	return R, G, B

if __name__ == "__main__":
	picture = Image.open("Yellow.jpg")
	color_dict = create_graphed_image(picture)
	R, G, B = calculate_primary_color(color_dict)
