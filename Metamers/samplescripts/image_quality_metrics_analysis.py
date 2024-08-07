import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
import os

# Function to calculate PSNR and return the difference map
def calculate_psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:  # MSE is zero means no difference
        return float('inf'), np.zeros_like(original)
    max_pixel = 255.0
    psnr_value = 20 * np.log10(max_pixel / np.sqrt(mse))
    diff = (original - compressed) ** 2
    diff = (diff / diff.max()) * 255
    return psnr_value, diff.astype(np.uint8)

# Function to read images
def read_image(image_path):
    return cv2.imread(image_path, cv2.IMREAD_COLOR)

# Function to calculate SSIM and return the difference map
def calculate_ssim(original, compressed):
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    compressed_gray = cv2.cvtColor(compressed, cv2.COLOR_BGR2GRAY)
    ssim_value, diff = ssim(original_gray, compressed_gray, full=True)
    diff = (diff * 255).astype("uint8")
    return ssim_value, diff

# Custom function to calculate VIF and return the difference map
def calculate_vif(reference, distorted):
    sigma_nsq = 2.0
    eps = 1e-10

    reference = reference.astype(np.float64)
    distorted = distorted.astype(np.float64)

    mu1 = cv2.GaussianBlur(reference, (9, 9), 1.5)
    mu2 = cv2.GaussianBlur(distorted, (9, 9), 1.5)

    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = cv2.GaussianBlur(reference * reference, (9, 9), 1.5) - mu1_sq
    sigma2_sq = cv2.GaussianBlur(distorted * distorted, (9, 9), 1.5) - mu2_sq
    sigma12 = cv2.GaussianBlur(reference * distorted, (9, 9), 1.5) - mu1_mu2

    g = sigma12 / (sigma1_sq + eps)
    sv_sq = sigma2_sq - g * sigma12

    g[sigma1_sq < eps] = 0
    sv_sq[sigma1_sq < eps] = sigma2_sq[sigma1_sq < eps]
    sigma1_sq[sigma1_sq < eps] = 0

    g[sigma2_sq < eps] = 0
    sv_sq[sigma2_sq < eps] = 0

    num = np.sum(np.log10(1 + g * g * sigma1_sq / (sv_sq + sigma_nsq)))
    den = np.sum(np.log10(1 + sigma1_sq / sigma_nsq))

    vifp = num / den

    diff = np.abs(reference - distorted)
    diff = (diff / diff.max()) * 255
    return vifp, diff.astype(np.uint8)

# Image paths
image_pairs = [
    ('../sampleimages/bigben.jpg', './result/bigben_metamer.png'),
    ('../sampleimages/buffon.png', './result/buffon_metamer.png'),
    ('../sampleimages/Einstein.jpg', './result/Einstein_metamer.png'),
    ('../sampleimages/Shakespeare.jpg', './result/Shakespeare_metamer.png')
]

# Create directory to save result images
output_dir = 'F:/msc/results'
os.makedirs(output_dir, exist_ok=True)

# Store results
results = []

# Process each image pair
for i, (original_path, compressed_path) in enumerate(image_pairs):
    original_image = read_image(original_path)
    compressed_image = read_image(compressed_path)

    psnr_value, psnr_diff = calculate_psnr(original_image, compressed_image)
    ssim_value, ssim_diff = calculate_ssim(original_image, compressed_image)
    vif_value, vif_diff = calculate_vif(cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY), cv2.cvtColor(compressed_image, cv2.COLOR_BGR2GRAY))

    results.append({
        'Original Image': original_path,
        'Compressed Image': compressed_path,
        'PSNR': psnr_value,
        'SSIM': ssim_value,
        'VIF': vif_value
    })

    # Save original image
    cv2.imwrite(f'{output_dir}/original_image_{i+1}.png', original_image)
    # Save compressed image
    cv2.imwrite(f'{output_dir}/compressed_image_{i+1}.png', compressed_image)

    # Convert difference map to pseudo-color map
    psnr_diff_colored = cv2.applyColorMap(psnr_diff, cv2.COLORMAP_JET)
    ssim_diff_colored = cv2.applyColorMap(ssim_diff, cv2.COLORMAP_JET)
    vif_diff_colored = cv2.applyColorMap(vif_diff, cv2.COLORMAP_JET)

    # Save pseudo-color difference images
    cv2.imwrite(f'{output_dir}/psnr_diff_{i+1}.png', psnr_diff_colored)
    cv2.imwrite(f'{output_dir}/ssim_diff_{i+1}.png', ssim_diff_colored)
    cv2.imwrite(f'{output_dir}/vif_diff_{i+1}.png', vif_diff_colored)

    # Visualize and save images with PSNR, SSIM, VIF, and difference maps
    fig, ax = plt.subplots(2, 3, figsize=(18, 12))

    # Original image
    ax[0, 0].imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    ax[0, 0].set_title('Original Image')
    ax[0, 0].axis('off')

    # Compressed image
    ax[0, 1].imshow(cv2.cvtColor(compressed_image, cv2.COLOR_BGR2RGB))
    ax[0, 1].set_title(f'Compressed Image\nPSNR: {psnr_value:.2f}, SSIM: {ssim_value:.2f}, VIF: {vif_value:.2f}')
    ax[0, 1].axis('off')

    # SSIM difference map
    ax[0, 2].imshow(ssim_diff_colored)
    ax[0, 2].set_title('SSIM Difference Heatmap')
    ax[0, 2].axis('off')

    # PSNR difference map
    ax[1, 0].imshow(psnr_diff_colored)
    ax[1, 0].set_title('PSNR Difference Heatmap')
    ax[1, 0].axis('off')

    # VIF difference map
    ax[1, 1].imshow(vif_diff_colored)
    ax[1, 1].set_title('VIF Difference Heatmap')
    ax[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/comparison_{i+1}.png')
    plt.close()

# Convert results to DataFrame
df = pd.DataFrame(results)

# Print the table
print(df)

# Save the table to a CSV file
df.to_csv(f'{output_dir}/image_quality_metrics.csv', index=False)