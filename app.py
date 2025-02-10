import os
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Define NSFW detection thresholds
SKIN_THRESHOLD = 40  # Adjusted threshold for total skin percentage
UPPER_HALF_SKIN_THRESHOLD = 30  # Threshold for upper half of the image
EXPOSED_AREA_THRESHOLD = 5.0  # Edge detection threshold for exposed areas
LARGE_SKIN_REGION_AREA = 5000  # Minimum area for a large skin region
SMALL_SKIN_REGION_AREA = 100  # Minimum area for a small skin region

def detect_skin_percentage(image):
    """Detects skin percentage and returns total and upper-half skin coverage."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define skin color range in HSV
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create a skin mask
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply morphological operations to reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)

    # Calculate skin percentage
    total_pixels = image.shape[0] * image.shape[1]
    skin_pixels = cv2.countNonZero(skin_mask)
    skin_percentage = (skin_pixels / total_pixels) * 100

    # Calculate upper-half skin percentage
    height, width = image.shape[:2]
    upper_half_mask = skin_mask[:height // 2, :]
    upper_half_skin_pixels = cv2.countNonZero(upper_half_mask)
    upper_half_skin_percentage = (upper_half_skin_pixels / (total_pixels / 2)) * 100

    return skin_percentage, upper_half_skin_percentage, skin_mask

def detect_skin_regions(skin_mask):
    """Finds large and small skin regions using contour detection."""
    contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large_regions = [cnt for cnt in contours if cv2.contourArea(cnt) > LARGE_SKIN_REGION_AREA]
    small_regions = [cnt for cnt in contours if SMALL_SKIN_REGION_AREA < cv2.contourArea(cnt) <= LARGE_SKIN_REGION_AREA]
    return len(large_regions), len(small_regions)

def detect_exposed_areas(image, skin_mask):
    """Detects exposed skin areas using edge detection combined with skin mask."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive edge detection
    edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
    
    # Combine edges with skin mask
    exposed_areas = cv2.bitwise_and(edges, skin_mask)
    exposed_area_pixels = cv2.countNonZero(exposed_areas)
    total_pixels = image.shape[0] * image.shape[1]
    
    return (exposed_area_pixels / total_pixels) * 100

def is_nsfw_and_delete(image_path):
    """Detects NSFW content and deletes the image if flagged."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image '{image_path}'. Skipping...")
        return

    # Process image for skin detection
    skin_percentage, upper_half_skin_percentage, skin_mask = detect_skin_percentage(image)
    
    # Detect skin regions
    large_skin_regions, small_skin_regions = detect_skin_regions(skin_mask)
    
    # Detect exposed areas
    exposed_area_percentage = detect_exposed_areas(image, skin_mask)

    # Print analysis results
    print(f"\nProcessing image: {image_path}")
    print(f"Skin Percentage (Entire Image): {skin_percentage:.2f}%")
    print(f"Skin Percentage (Upper Half): {upper_half_skin_percentage:.2f}%")
    print(f"Large Skin Regions: {large_skin_regions}")
    print(f"Small Skin Regions: {small_skin_regions}")
    print(f"Exposed Area Percentage: {exposed_area_percentage:.2f}%")

    # NSFW classification based on thresholds
    if (
        skin_percentage > SKIN_THRESHOLD and
        upper_half_skin_percentage > UPPER_HALF_SKIN_THRESHOLD and
        large_skin_regions >= 1 and
        small_skin_regions >= 1 and
        exposed_area_percentage > EXPOSED_AREA_THRESHOLD
    ):
        print("❌ NSFW content detected! Deleting image...")
        try:
            os.remove(image_path)
            print(f"✅ Image deleted: {image_path}")
        except Exception as e:
            print(f"⚠️ Error deleting the image: {e}")
    else:
        print("✅ Image is safe. No action taken.")

def process_images_in_folder(folder_path):
    """Processes all images in a folder using parallel processing."""
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Supported image formats
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    # Get all image files in the folder
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(supported_extensions)]

    # Use ThreadPoolExecutor for faster processing
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(is_nsfw_and_delete, image_files)

# Example usage
folder_path = "images"  # Update this path to your folder containing images
process_images_in_folder(folder_path)