# GuardianAI: Detect, Blur, and Organize Nude/Semi-Nude Images

This Python project detects nude and semi-nude images using the **OpenNSFW2** library, blurs them, and organizes them into separate folders. It is designed to help automate the process of identifying and handling sensitive content in image datasets.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Folder Structure](#folder-structure)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features
- **Detect Nude/Semi-Nude Images**: Uses the OpenNSFW2 model to classify images based on their NSFW probability.
- **Blur Unsafe Images**: Applies a Gaussian blur to detected nude/semi-nude images to anonymize sensitive content.
- **Organize Images**:
  - Moves original unsafe images to a dedicated folder (`nude_images`).
  - Moves blurred versions of unsafe images to another folder (`blurred_images`).
- **Threshold-Based Filtering**: Allows you to adjust the sensitivity of detection using a configurable threshold.

---

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.7 or higher
- `opennsfw2` (for NSFW detection)
- `Pillow` (for image processing)
- `shutil` (for file operations)

You can install the required dependencies using the following command:

```bash
pip install opennsfw2 pillow
```

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/wprashed/guardianai
   cd guardianai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the necessary folders:
   ```
   mkdir input_images nude_images blurred_images
   ```

4. Place your images in the `input_images` folder.

---

## Usage
1. Run the script:
   ```bash
   python app.py
   ```

2. The script will:
   - Process all images in the `input_images` folder.
   - Move detected nude/semi-nude images to the `nude_images` folder.
   - Blur the detected images and move the blurred versions to the `blurred_images` folder.

3. Adjust the sensitivity of detection by modifying the `threshold` variable in the script:
   ```python
   threshold = 0.6  # Default value; adjust between 0 and 1
   ```

---

## Folder Structure
The project uses the following folder structure:
```
project/
├── input_images/       # Place your images here
├── nude_images/        # Original nude/semi-nude images will be moved here
├── blurred_images/     # Blurred nude/semi-nude images will be moved here
├── temp_blurred/       # Temporary folder for blurred images (auto-cleaned)
├── app.py              # The Python script
├── README.md           # Project documentation
└── requirements.txt    # List of dependencies
```

---

## Customization
1. **Adjust Blur Intensity**:
   Modify the `radius` parameter in the `blur_image()` function to control the strength of the blur:
   ```python
   blurred_img = img.filter(ImageFilter.GaussianBlur(radius=20))  # Default radius
   ```

2. **Change Detection Threshold**:
   Adjust the `threshold` variable in the `process_images()` function to make the detection stricter or more lenient:
   ```python
   threshold = 0.6  # Higher values make detection stricter
   ```

3. **Output Folder Names**:
   Change the folder names in the `process_images()` function if you want to use different folder names:
   ```python
   nude_folder = "nude_images"
   blurred_folder = "blurred_images"
   ```

---

## Troubleshooting
1. **Error: Pillow Not Installed**:
   If you encounter an error related to `Pillow`, install it using:
   ```bash
   pip install pillow
   ```

2. **Error: File Overwrite Issues**:
   Ensure filenames are unique or modify the script to append a suffix to filenames when saving blurred images.

3. **Temporary Folder Cleanup**:
   The `temp_blurred` folder is automatically deleted if empty. If issues persist, manually delete it after running the script.

---

## Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

---

## License
This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the terms of the license.

---

## Acknowledgments
- Thanks to the creators of the [OpenNSFW2](https://github.com/mdietrichstein/opennsfw2) library for making it publicly available.
- Special thanks to the `Pillow` library for providing robust image processing capabilities.
