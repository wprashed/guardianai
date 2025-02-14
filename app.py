import os
import shutil
import opennsfw2 as n2
from PIL import Image, ImageFilter


# Blur an image and save it to a temporary folder
def blur_image(image_path, temp_folder):
    # Open the image
    img = Image.open(image_path)

    # Apply a Gaussian blur (you can adjust the radius for stronger/weaker blur)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=20))

    # Save the blurred image to the temporary folder
    temp_path = os.path.join(temp_folder, os.path.basename(image_path))
    blurred_img.save(temp_path)
    print(f"Blurred and saved temporarily: {temp_path}")
    return temp_path


# Process images based on classification
def process_images(input_folder, nude_folder, blurred_folder, threshold=0.5):
    # Create folders if they don't exist
    if not os.path.exists(nude_folder):
        os.makedirs(nude_folder)
    if not os.path.exists(blurred_folder):
        os.makedirs(blurred_folder)

    # Create a temporary folder for blurred images
    temp_folder = "temp_blurred"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Check if the file is an image
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"Processing: {filename}")

            # Predict NSFW probability
            nsfw_probability = n2.predict_image(file_path)

            # Check if the image is classified as NSFW above the threshold
            if nsfw_probability > threshold:
                print(f"Detected nude/semi-nude: {filename} (Probability: {nsfw_probability:.2f})")

                # Move the original image to the "nude" folder
                shutil.move(file_path, os.path.join(nude_folder, filename))
                print(f"Moved original image: {filename} to {nude_folder}")

                # Blur the image and save it to the temporary folder
                temp_path = blur_image(os.path.join(nude_folder, filename), temp_folder)

                # Move the blurred image to the "blurred" folder
                shutil.move(temp_path, os.path.join(blurred_folder, filename))
                print(f"Moved blurred image: {filename} to {blurred_folder}")
            else:
                print(f"Safe image: {filename} (Probability: {nsfw_probability:.2f})")

    # Clean up the temporary folder if it's empty
    if os.path.exists(temp_folder) and not os.listdir(temp_folder):
        os.rmdir(temp_folder)


if __name__ == "__main__":
    # Define input and output folders
    input_folder = "input_images"  # Folder containing the images to check
    nude_folder = "nude_images"  # Folder to move original nude/semi-nude images
    blurred_folder = "blurred_images"  # Folder to move blurred nude/semi-nude images

    # Set the threshold for detecting nude/semi-nude images
    threshold = 0.6  # Adjust this value between 0 and 1 for sensitivity

    # Run the detection, moving, and blurring process
    process_images(input_folder, nude_folder, blurred_folder, threshold)