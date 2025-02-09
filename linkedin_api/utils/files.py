import subprocess
import requests
import os
import uuid

def download_file_from_url(url):
    response = requests.get(url, stream=True)
    
    # Extract filename from headers or URL
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition and "filename=" in content_disposition:
        filename = content_disposition.split("filename=")[-1].strip(' "')
    else:
        filename = os.path.basename(url.split("?")[0])  # Remove query params if present

    content_type = response.headers.get("Content-Type", "Unknown")

    file_uuid = uuid.uuid4()
    filename_with_uuid = f"{file_uuid}---{filename}"

    # Download and save the file
    total_bytes = 0
    # Ensure the directory exists
    os.makedirs("files", exist_ok=True)
    with open(os.path.join("files", filename_with_uuid), "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            total_bytes += len(chunk)

    # Log the details
    print(f"Downloaded: {filename}")
    print(f"File Size: {total_bytes} bytes" if total_bytes else "Unknown size")
    print(f"Content Type: {content_type}")

    return {
        "byteSize": total_bytes,
        "mediaType": content_type,
        "name": filename,
        "fileId": filename_with_uuid
    }
    
def get_file_properties(assetUrn: str):
    parts = assetUrn.split("---")

    if len(parts) > 1:
        assetUrnValue = parts[0]
        id = parts[1]
        filename = parts[2]

        file_path = "---".join([parts[1], parts[2]])

        mime_type = subprocess.run(["file", "--mime-type", "-b", os.path.join("files", file_path)], capture_output=True, text=True).stdout.strip()
        # Get the file size
        file_size = os.path.getsize(os.path.join("files", file_path))
        return {
            "assetUrn": assetUrnValue,
            "byteSize": file_size,
            "mediaType": mime_type,
            "name": filename,
            "url": f"blob:https://www.linkedin.com/{id}"
        }
    else:
        print("No ID found")
    
    return "Invalid asset URN" 