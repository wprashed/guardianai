import os
import shutil
import opennsfw2 as n2


# Move images based on classification
def move_images(input_folder, output_folder, threshold=0.5):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

                # Move the image to the output folder
                shutil.move(file_path, os.path.join(output_folder, filename))
                print(f"Moved: {filename} to {output_folder}")
            else:
                print(f"Safe image: {filename} (Probability: {nsfw_probability:.2f})")


if __name__ == "__main__":
    # Define input and output folders
    input_folder = "input_images"  # Folder containing the images to check
    output_folder = "nude_images"  # Folder to move detected nude/semi-nude images

    # Set the threshold for detecting nude/semi-nude images
    threshold = 0.6  # Adjust this value between 0 and 1 for sensitivity

    # Run the detection and moving process
    move_images(input_folder, output_folder, threshold)