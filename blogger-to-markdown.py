import os
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from dateutil import parser
from bs4 import BeautifulSoup

# Configure paths
BLOGGER_FILE = "blog-12-04-2024.xml"  # Replace with your Blogger file name
OUTPUT_DIR = "markdown_posts"  # Directory to save Markdown files
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")  # Subdirectory for images

# Create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def clean_filename(title):
    """Create a safe filename from a blog post title."""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in title)

def download_image(img_url, output_dir):
    """Download an image from the given URL and save it locally."""
    # Ensure the images directory exists
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Generate a local filename for the image
    img_name = os.path.basename(img_url.split("?")[0])  # Remove query params
    local_path = os.path.join(images_dir, img_name)

    try:
        # Download and save the image
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        with open(local_path, "wb") as img_file:
            for chunk in response.iter_content(1024):
                img_file.write(chunk)
    except Exception as e:
        print(f"Failed to download image: {img_url}\nError: {e}")
        return None

    return f"./images/{img_name}"

def clean_html(content, output_dir):
    """Clean up HTML content, download images, and convert to Markdown-friendly text."""
    soup = BeautifulSoup(content, "html.parser")

    # Replace <br> and <br/> tags with newline characters
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Replace <p> tags with double newlines for Markdown paragraphs
    for p in soup.find_all("p"):
        p.insert_after("\n\n")
        p.unwrap()

    # Process <img> tags: download and replace with local Markdown paths
    for img in soup.find_all("img"):
        img_url = img.get("src", "")
        if img_url:
            local_path = download_image(img_url, output_dir)
            if local_path:
                markdown_image = f"![Image]({local_path})"
                img.insert_after(markdown_image)
        img.decompose()  # Remove the original <img> tag

    # Remove other unwanted tags while keeping their content
    for tag in soup.find_all(["div", "a"]):
        tag.unwrap()

    # Return cleaned-up text
    return soup.get_text().strip()


def replace_images_in_content(content):
    """Replace image URLs in content and download the images."""
    def replace_match(match):
        url = match.group(1)
        local_path = download_image(url, IMAGES_DIR)
        return f'![Image]({local_path})'

    # Match <img> tags and extract their src attributes
    return re.sub(r'<img[^>]+src="([^">]+)"[^>]*>', replace_match, content)

def parse_blogger_date(published):
    """Parse Blogger's published date using dateutil."""
    try:
        return parser.parse(published).strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error parsing date: {published}. Error: {e}")
        return "unknown_date"

def convert_blogger_to_markdown(blogger_file, output_dir):
    """Convert Blogger XML export file to Markdown files with images."""
    tree = ET.parse(blogger_file)
    root = tree.getroot()

    # Namespaces in the Blogger XML
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "blogger": "http://schemas.google.com/blogger/2008",
    }

    # Iterate through entries in the Blogger XML
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text or "Untitled"
        published = entry.find("atom:published", ns).text
        content = entry.find("atom:content", ns)

        if content is not None:
            content_text = content.text or ""
        else:
            content_text = ""

        # Clean HTML and process image URLs
        content_text = clean_html(content_text, output_dir)

        # Format the published date
        date = parse_blogger_date(published)

        # Generate Markdown filename and content
        filename = f"{date}-{clean_filename(title)}.md"
        markdown_content = f"""---
title: "{title}"
date: {date}
---

{content_text}
"""

        # Save the Markdown file
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)

    print(f"Conversion completed! Markdown files with images saved in: {output_dir}")


# Run the conversion
convert_blogger_to_markdown(BLOGGER_FILE, OUTPUT_DIR)
