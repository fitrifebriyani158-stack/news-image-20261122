import os
import shutil
# Set destination folder from environment variable or default to /output
dest_folder = os.getenv("MAKEFUN_OUTPUT_DIR", "/output")
# Create destination folder if it doesn’t exist
if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)
# Copy entry.png into destination folder
shutil.copy2("entry.png", dest_folder + "/entry.png")
print(f"Poster copied to {dest_folder}/entry.png")
