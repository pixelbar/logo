import glob
import pathlib
import argparse
import defusedxml.ElementTree

import cairosvg

def convert_svg_to_pdf(svg_file, pdf_file, background_color):
    cairosvg.svg2pdf(url=svg_file, write_to=pdf_file, background_color=background_color)

def convert_svg_to_png(svg_file, png_file, output_width, background_color):
    cairosvg.svg2png(url=svg_file, write_to=png_file, output_width=output_width, background_color=background_color)

def get_page_color(svg_file):
    tree = defusedxml.ElementTree.parse(svg_file)
    named_view = tree.getroot().find("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview[@pagecolor]")
    return named_view.get("pagecolor")

def find_svg_files(directory):
   return glob.iglob(directory + "/**/*.svg", recursive=True)

def create_folder(directory):
    try:
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process svg files in a folder and convert into PNG variants.")
    parser.add_argument("dir", type=str, help="The directory to process.")
    args = parser.parse_args()

    for file in find_svg_files(args.dir):
        print(file)

        svg_path = pathlib.Path(file)
        page_color = get_page_color(svg_path)

        parent_path = svg_path.parent.parent
        pdf_folder = parent_path / "PDF" 
        pdf_path = pdf_folder / svg_path.with_suffix(".pdf").name
        create_folder(pdf_folder)

        convert_svg_to_pdf(str(svg_path), str(pdf_path), background_color=page_color)
        flat_png_folder = parent_path / "PNG"
        create_folder(flat_png_folder)
        png_folder = parent_path / "PNG transparent background"
        create_folder(png_folder)

        for width in [512, 1024, 2048, 4096, 8192]:
            png_path = flat_png_folder / svg_path.with_suffix(f".{width}.png").name
            convert_svg_to_png(str(svg_path), str(png_path), width, background_color=page_color)

            png_path = png_folder / svg_path.with_suffix(f".{width}.png").name
            convert_svg_to_png(str(svg_path), str(png_path), width, background_color=None)
