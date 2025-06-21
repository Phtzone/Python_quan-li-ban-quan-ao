import os

# Dùng đường dẫn tương đối
folder_path = "image"

file_list = sorted(os.listdir(folder_path))

for i, filename in enumerate(file_list):
    old_path = os.path.join(folder_path, filename)

    if not os.path.isfile(old_path):
        continue

    new_filename = f"{i+1}.jpg"
    new_path = os.path.join(folder_path, new_filename)

    os.rename(old_path, new_path)

print("Đổi tên xong!")
