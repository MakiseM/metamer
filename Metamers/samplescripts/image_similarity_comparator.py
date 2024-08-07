import cv2
import numpy as np
import matplotlib.pyplot as plt


def calculate_histogram(image):
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Calculate the histogram
    hist = cv2.calcHist([hsv_image], [0, 1], None, [50, 60], [0, 180, 0, 256])
    # Normalize the histogram
    cv2.normalize(hist, hist)
    return hist


def compare_images(image1, image2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    # Compute the absolute difference between the two images
    diff = cv2.absdiff(gray1, gray2)
    # Threshold the difference image to get the regions with significant differences
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    return thresh


def calculate_similarity(hist1, hist2):
    # Compare the histograms using correlation method
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity


def overlay_diff(image, diff_mask, label):
    # Create a colored overlay
    overlay = np.zeros_like(image)
    overlay[:, :, 1] = 255  # Green channel
    # Apply the overlay to the original image
    overlayed_image = image.copy()
    overlayed_image[diff_mask == 255] = cv2.addWeighted(image[diff_mask == 255], 0.5, overlay[diff_mask == 255], 0.5, 0)
    # Add text label
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(overlayed_image, label, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return overlayed_image


def main(image_paths, groundtruth_path):
    # Load the images
    images = [cv2.imread(image_path) for image_path in image_paths]
    groundtruth = cv2.imread(groundtruth_path)
    num_images = len(images)

    # Define labels for the pairs
    labels = [
        ("Image 1 and Image 2", "Image 1 and Image 3", "Image 1 and Groundtruth"),
        ("Image 2 and Image 1", "Image 2 and Image 3", "Image 2 and Groundtruth"),
        ("Image 3 and Image 1", "Image 3 and Image 2", "Image 3 and Groundtruth")
    ]

    # Calculate histograms for all images
    histograms = [calculate_histogram(image) for image in images]
    groundtruth_hist = calculate_histogram(groundtruth)

    # Calculate pairwise differences and overlay them on images
    result_images = []
    for i in range(num_images):
        for j in range(i + 1, num_images):
            diff_mask = compare_images(images[i], images[j])
            similarity = calculate_similarity(histograms[i], histograms[j])
            label = f"{labels[i][j - 1]} (Similarity: {similarity:.4f})"
            result_image = overlay_diff(images[i], diff_mask, label)
            result_images.append((result_image, label))

        # Compare with groundtruth
        diff_mask = compare_images(images[i], groundtruth)
        similarity = calculate_similarity(histograms[i], groundtruth_hist)
        label = f"{labels[i][-1]} (Similarity: {similarity:.4f})"
        result_image = overlay_diff(images[i], diff_mask, label)
        result_images.append((result_image, label))

    # Save and display the result images
    for idx, (result_image, label) in enumerate(result_images):
        output_path = f"result_{idx + 1}.png"
        cv2.imwrite(output_path, result_image)
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        plt.title(f'Difference Overlay: {label}')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    image_paths = ["./poolstatmetamer_output/1.png", "./poolstatmetamer_output/2.png", "./poolstatmetamer_output/3.png"]  # Replace with your image paths
    groundtruth_path = "./poolstatmetamer_output/groundtruth.png"
    main(image_paths,groundtruth_path)