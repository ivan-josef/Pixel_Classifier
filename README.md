# Pixel Class Annotator for Color Segmentation

A specialized computer vision tool designed to manually annotate pixels in images. The primary goal of this tool is to generate a robust dataset (CSV) containing HSV color values associated with specific classes. 

This dataset is intended to train a Neural Network (or Machine Learning classifiers) that will subsequently generate semantic segmentation masks automatically for training images.

## Purpose & Workflow

1.  **Annotation:** Use this tool to select regions of interest (ROI) using polygons.
2.  **Extraction:** The tool extracts the HSV (Hue, Saturation, Value) data of every pixel inside the polygon.
3.  **Dataset Creation:** Exports a structured `.csv` file where each row is a pixel and columns are `H`, `S`, `V`, and `class`.
4.  **Training (Next Step):** You use this CSV to train a lightweight classifier (e.g., MLP, SVM, Random Forest).
5.  **Inference:** The trained model is applied to full images to classify every pixel, generating a binary or multi-class mask for semantic segmentation tasks. 

## Features

* **Polygon Selection:** Precise annotation using mouse clicks (Left click to add points, Right click to close polygon).
* **Multi-Class Support:** Define as many classes as needed (e.g., *grass, road, sky*) at runtime.
* **Visual Feedback:** Real-time drawing with transparency (visualized via redraw) or solid colors to track progress.
* **Undo Functionality:** Remove the last annotated polygon and its corresponding data from the specific class.
* **HSV Color Space:** Automatically converts BGR images to HSV for better color segmentation performance.
* **Pandas Export:** Saves the final dataset in a clean CSV format ready for Data Science libraries.

## 🛠️ Prerequisites

Ensure you have Python installed along with the following libraries:

```bash
pip install opencv-python numpy pandas
```

## Controls 

* L-Click	Add a vertex point to the polygon
* R-Click	Close the polygon and save pixel data
* A	Previous Image
* D	Next Image
* Q	Previous Class
* E	Next Class
* Z	Undo (Delete last polygon/data of current class)
* W	Save Dataset to CSV and Exit

## How to use

1. **Setup Path:** Open the script and update the path variable to point to your image folder:

```bash
path = '/path/to/your/images'
```

2. **Run the script:**

```bash
python3 pixel_classifier.py
```

3. **Define classes:** The terminal will ask how many classes you want. Enter the number and name them 

4. **Anotate:**

* Navigate to an image.
* Select the class using **Q** and **E**.
* Draw polygons around the object of interest

5. **Export:** When finished, press **W**. Enter a name for your file 