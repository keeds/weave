import argparse
from PIL import Image, ImageFilter, ImageDraw

def weave_grid(path1, path2, output_path, dpi=96, x_ratio=1, y_ratio=1, border_softness=2):
    img1 = Image.open(path1).convert("RGB")
    img2 = Image.open(path2).convert("RGB")

    # Ensure images match size
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)

    width, height = img1.size
    
    # Calculate base strip size in pixels (1cm)
    base_strip = int(dpi / 2.54)
    
    # Calculate strip sizes based on ratio
    strip_x = base_strip * x_ratio
    strip_y = base_strip * y_ratio
    
    # Create output canvas
    result = Image.new("RGB", (width, height))

    # Process by grid blocks
    for y in range(0, height, strip_y):
        for x in range(0, width, strip_x):
            # Define the bounding box for the current rectangle
            box = (x, y, min(x + strip_x, width), min(y + strip_y, height))
            box_width = box[2] - box[0]
            box_height = box[3] - box[1]
            
            # Logic: If (row_index + col_index) is even, use Image A. 
            # Otherwise, use Image B. This creates the "checkered" weave.
            if ((y // strip_y) + (x // strip_x)) % 2 == 0:
                region = img1.crop(box)
            else:
                region = img2.crop(box)
            
            # Create a soft-edged mask for the region
            mask = Image.new("L", (box_width, box_height), 0)  # Black mask
            draw = ImageDraw.Draw(mask)
            # Draw a white rectangle inset by border_softness
            inset = border_softness
            if box_width > 2 * inset and box_height > 2 * inset:
                draw.rectangle([inset, inset, box_width - inset, box_height - inset], fill=255)
            else:
                draw.rectangle([0, 0, box_width, box_height], fill=255)
            # Blur the mask to soften edges
            mask = mask.filter(ImageFilter.GaussianBlur(radius=border_softness))
                
            result.paste(region, (x, y), mask)

    result.save(output_path)
    print(f"Grid weave complete! Strip size: {strip_x}x{strip_y}px (ratio {x_ratio}:{y_ratio})")


def main():
    parser = argparse.ArgumentParser(description="Create a woven grid image from two input images.")
    parser.add_argument("input1", help="Path to the first input image.")
    parser.add_argument("input2", help="Path to the second input image.")
    parser.add_argument("output", help="Output image path.")
    parser.add_argument("--dpi", type=int, default=96, help="Dots per inch used to calculate strip size (default: 96).")
    parser.add_argument("--x-ratio", type=int, default=1, help="X-axis ratio multiplier (default: 1).")
    parser.add_argument("--y-ratio", type=int, default=1, help="Y-axis ratio multiplier (default: 1).")
    parser.add_argument("--border-softness", type=int, default=2, help="Softness of cell borders (default: 2).")

    args = parser.parse_args()
    weave_grid(args.input1, args.input2, args.output, dpi=args.dpi, x_ratio=args.x_ratio, y_ratio=args.y_ratio, border_softness=args.border_softness)


if __name__ == "__main__":
    main()
