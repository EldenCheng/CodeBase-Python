from PIL import Image
from PIL.ExifTags import TAGS

if __name__ == '__main__':
    image_path = r"D:\PhotoAlbum\PhotoAlbum51\深圳出差\IMG_20250904_080603.jpg"  # Replace with your image file path
    try:
        img = Image.open(image_path)
    except IOError:
        print(f"Error: Could not open image file at {image_path}")
        exit()
    exif_data = img.getexif()
    print(exif_data)
    print(TAGS)
    print("The Exif of this image is: ")
    if exif_data:
        metadata = {}
        for tag_id, value in exif_data.items():
            print(f"{TAGS.get(tag_id, tag_id)}:{value}")  # Get human-readable tag name
    else:
        print("No EXIF metadata found in the image.")