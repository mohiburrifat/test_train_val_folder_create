import os
import shutil
import random
from tqdm import tqdm

def split_dataset(source_folder, output_folder):
    # Percentages
    train_split = 0.75
    val_split = 0.15
    test_split = 0.10

    # Output directories
    output_dirs = ["train", "validation", "test"]

    # Create main output folder
    os.makedirs(output_folder, exist_ok=True)

    # Create train/validation/test folders
    for d in output_dirs:
        os.makedirs(os.path.join(output_folder, d), exist_ok=True)

    # Loop through each subfolder inside source folder
    for subfolder in os.listdir(source_folder):
        subfolder_path = os.path.join(source_folder, subfolder)

        if not os.path.isdir(subfolder_path):
            continue

        images = [f for f in os.listdir(subfolder_path)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

        random.shuffle(images)
        total = len(images)

        # Compute split indexes
        train_end = int(total * train_split)
        val_end = train_end + int(total * val_split)

        train_imgs = images[:train_end]
        val_imgs = images[train_end:val_end]
        test_imgs = images[val_end:]

        # Create corresponding subfolders in the output directory
        for d in output_dirs:
            os.makedirs(os.path.join(output_folder, d, subfolder), exist_ok=True)

        # Copy files to split folders
        def copy_files(files, target_dir):
            for img in tqdm(files, desc=f"Copying to {target_dir}/{subfolder}"):
                src = os.path.join(subfolder_path, img)
                dst = os.path.join(output_folder, target_dir, subfolder, img)
                shutil.copy2(src, dst)

        copy_files(train_imgs, "train")
        copy_files(val_imgs, "validation")
        copy_files(test_imgs, "test")

    print("✔ Dataset successfully split into train, validation, and test folders!")


# ---------------------------
# User Input Section
# ---------------------------
source = input("Enter the input folder path: ")
destination = input("Enter the output folder path: ")

split_dataset(source, destination)
