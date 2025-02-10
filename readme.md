# NSFW Image Detection and Auto-Deletion

This project is a Python-based NSFW image detection system that scans images in a folder and automatically deletes those flagged as inappropriate. It uses **OpenCV** for skin detection, contour analysis, and edge detection to determine whether an image contains explicit content.

## 🚀 Features

- ✅ **Skin Detection:** Uses HSV color filtering and morphological transformations.
- ✅ **Edge Detection:** Canny edge detection helps detect exposed areas.
- ✅ **Contour Analysis:** Detects large and small skin regions.
- ✅ **Parallel Processing:** Uses `ThreadPoolExecutor` for fast image scanning.
- ✅ **Automatic Deletion:** Removes flagged NSFW images.
- ✅ **Configurable Thresholds:** Adjust detection sensitivity.

## 📌 How It Works

1. **Skin Detection:** The script identifies skin regions using HSV color filtering.
2. **Contour Analysis:** It finds large and small skin regions to estimate nudity.
3. **Edge Detection:** Detects exposed areas using adaptive Canny edge detection.
4. **Thresholding:** If an image exceeds defined thresholds, it's flagged as NSFW.
5. **Automatic Deletion:** Flagged images are removed from the system.

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/nsfw-image-detector.git
   cd nsfw-image-detector
   ```

2. **Install dependencies:**
   ```bash
   pip install opencv-python numpy
   ```

3. **Prepare a folder with images:**  
   Place images inside a folder (e.g., `images/`).

## 🔥 Usage

Run the script to scan all images in the specified folder:

```bash
python nsfw_detector.py
```

Modify the folder path inside the script:

```python
folder_path = "images"  # Change this to your image folder path
```

## ⚙️ Configuration

You can adjust these **detection thresholds** in `nsfw_detector.py` to fine-tune sensitivity:

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `SKIN_THRESHOLD` | Minimum total skin percentage required to be flagged | `40` |
| `UPPER_HALF_SKIN_THRESHOLD` | Minimum upper-body skin percentage required | `30` |
| `EXPOSED_AREA_THRESHOLD` | Minimum detected exposed area percentage | `5.0` |
| `LARGE_SKIN_REGION_AREA` | Minimum area size for a "large skin region" | `5000` |
| `SMALL_SKIN_REGION_AREA` | Minimum area size for a "small skin region" | `100` |

## 📝 Example Output

```
Processing image: images/sample1.jpg
Skin Percentage (Entire Image): 45.23%
Skin Percentage (Upper Half): 35.10%
Large Skin Regions: 2
Small Skin Regions: 3
Exposed Area Percentage: 7.25%
❌ NSFW content detected! Deleting image...
✅ Image deleted: images/sample1.jpg
```

## 🤖 How to Improve Accuracy

- **Fine-tune thresholds** to reduce false positives.
- **Use a deep-learning model** (e.g., **NSFW ResNet50**, **OpenNSFW2**).
- **Train on specific datasets** to improve detection for targeted content.

## 📜 License

This project is open-source under the **MIT License**.

---

🎯 **Need help?** Feel free to open an issue or contribute! 🚀