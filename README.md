# weave.py

A small Python script that creates a woven grid-style composite image from two input images.

The script divides the output into rectangular cells and alternates between the two source images in a checkerboard pattern. Each cell is pasted with a softly blurred edge to produce a seamless, woven appearance.

## Requirements

- Python 3.x
- Pillow

Install the dependency with:

```bash
pip install Pillow
```

## Usage

```bash
python weave.py <input1> <input2> <output> [--dpi DPI] [--x-ratio X_RATIO] [--y-ratio Y_RATIO] [--border-softness SOFTNESS]
```

### Arguments

- `input1` - Path to the first input image.
- `input2` - Path to the second input image.
- `output` - Path for the generated output image.

### Options

- `--dpi` - Dots per inch used to calculate the base strip size. Default is `96`.
- `--x-ratio` - Multiplier for the horizontal strip width. Default is `1`.
- `--y-ratio` - Multiplier for the vertical strip height. Default is `1`.
- `--border-softness` - Softness of the cell edges. Default is `2`.

## Example

```bash
python weave.py a1.jpg a2.jpg output.jpg --dpi 96 --x-ratio 1 --y-ratio 1 --border-softness 2
```

This will create a woven composite with square cells based on a 1cm strip size at 96 DPI.

## Notes

- If the two input images have different sizes, the second image is resized to match the first.
- The script uses a checkerboard strategy: cells are taken alternately from `input1` and `input2`.
- The resulting image is saved as the specified output file.
