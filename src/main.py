import os
from shutil import rmtree

from dotenv import load_dotenv
import supervisely as sly
from supervisely.io.fs import get_file_name


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

workspace_id = sly.env.workspace_id()

original_dir = "src/images/original"
result_dir = "src/images/result"

# Remove results directory if it exists.
if os.path.exists(result_dir):
    rmtree(result_dir)
os.mkdir(result_dir)


# Create new Supervisely project.
project = api.project.create(workspace_id, "Fruits", change_name_if_conflict=True)
print(f"Project ID: {project.id}")

# Create new Supervisely dataset.
dataset = api.dataset.create(project.id, "Fruits ds1")
print(f"Dataset ID: {dataset.id}")


# Upload image from local directory to Supervisely platform.
path = os.path.join(original_dir, "lemons.jpg")
meta = {"my-field-1": "my-value-1", "my-field-2": "my-value-2"}

image = api.image.upload_path(dataset.id, name="Lemons", path=path, meta=meta)
print(f'Image "{image.name}" uploaded to Supervisely with ID:{image.id}')


# Upload list of images from local directory to Supervisely platform.
names = [
    "grapes-1.jpg",
    "grapes-2.jpg",
    "oranges-2.jpg",
    "oranges-1.jpg",
]
paths = [os.path.join(original_dir, name) for name in names]

# This method uses fewer requests to database and allows to upload more images efficiently.
upload_info = api.image.upload_paths(dataset.id, names, paths)
print(f"{len(upload_info)} images successfully uploaded to Supervisely platform")


# Upload image from local directory to Supervisely platform as NumPy matrix
img_np = sly.image.read(path)
np_image_info = api.image.upload_np(dataset.id, name="Lemons-np.jpeg", img=img_np)
print(f"Image successfully uploaded as NumPy matrix to Supervisely (ID: {np_image_info.id})")

# Upload list of images from local directory to Supervisely platform
names_np = [f"np-{name}" for name in names]
imgs_np = [sly.image.read(img_path) for img_path in paths]
np_images_info = api.image.upload_nps(dataset.id, names_np, imgs_np)
print(f"{len(imgs_np)} images successfully uploaded to platform as NumPy matrix")


# Get information about image from Supervisely by id.
image_info = api.image.get_info_by_id(image.id)
print(image_info)

# Get information about image from Supervisely by name and dataset ID.
image_name = get_file_name(image.name)
image_info_by_name = api.image.get_info_by_name(dataset.id, image_name)
print(f"image name - {image_info_by_name.name}")

# Get list of all images from Supervisely dataset.
image_info_list = api.image.get_list(dataset.id)
print(f"{len(image_info_list)} images information received.")


# Download image from Supervisely platform to local directory by id.
save_path = os.path.join(result_dir, image_info.name)
api.image.download_path(image_info.id, save_path)
print(f"Image has been successfully downloaded to '{save_path}'")


# Download list of images from Supervisely platform to local directory by ids.
image_ids = [img.id for img in image_info_list]
image_names = [img.name for img in image_info_list]
save_paths = [os.path.join(result_dir, img_name) for img_name in image_names]

api.image.download_paths(dataset.id, image_ids, save_paths)
print(f"{len(image_info_list)} images has been successfully downloaded")


# You can also download image frame as RGB NumPy matrix.
image_np = api.image.download_np(image_info.id)
print(f"image downloaded as RGB NumPy matrix. Image shape: {image_np.shape}")

# Download multiple images as RGB NumPy matrix from Supervisely platform.
image_np = api.image.download_nps(dataset.id, image_ids)
print(f"{len(image_np)} images downloaded in RGB NumPy matrix.")


# Get image metadata from server
img = api.image.get_info_by_id(image.id)
meta = img.meta
print(image.meta)


# Update image metadata at server
new_meta = {"Camera Make": "Canon", "Color Space": "sRGB"}

api.image.update_meta
new_image_info = api.image.update_meta(id=image.id, meta=new_meta)

print(new_image_info["meta"])


# Remove image from Supervisely platform by id
api.image.remove(image.id)
print(f"Video (ID: {image.id}) successfully removed")


# Remove list of images from Supervisely platform by ids
images_to_remove = api.image.get_list(dataset.id)
remove_ids = [img.id for img in images_to_remove]
api.image.remove_batch(remove_ids)
print(f"{len(remove_ids)} images successfully removed.")
