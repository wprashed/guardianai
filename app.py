import os
from nsfw_detector import predict

# Path to the folder containing images
IMAGE_FOLDER = 'images'

# Load the NSFW model
model = predict.load_model('nsfw_model.h5')  # You need to download a pre-trained model

def is_nude(image_path, threshold=0.8):
    predictions = predict.classify(model, image_path)
    nsfw_score = predictions[image_path].get('porn', 0) + predictions[image_path].get('hentai', 0)
    return nsfw_score > threshold

def remove_nude_images(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                image_path = os.path.join(root, file)
                if is_nude(image_path):
                    print(f"Removing NSFW image: {image_path}")
                    os.remove(image_path)

# Run the nude photo remover
remove_nude_images(IMAGE_FOLDER)