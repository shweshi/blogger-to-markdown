# Blogger to Markdown Converter

This script converts a Blogger XML export file into Markdown files, downloading and storing images locally.

## Features
- Converts Blogger posts to Markdown format.
- Downloads and stores images in a local `images` directory.
- Replaces image URLs with local file paths in the Markdown files.
- Preserves the structure and metadata (like title and published date) of posts.

## Requirements

### Dependencies
The script requires the following Python libraries:
- `xml.etree.ElementTree` (built-in)
- `os` (built-in)
- `requests`
- `beautifulsoup4`

### Install the external libraries using pip:
```bash
pip install requests beautifulsoup4
```

### Input File
You need a Blogger XML export file. You can download this file from your Blogger settings under "Back up content."

### Usage
#### Steps to Run
- Place the Blogger XML file (e.g., blogger.xml) in the same directory as the script.
- Create an output directory (e.g., output).
- Run the script:
```bash
python blogger_to_markdown.py ./path_to_blogger.xml
```
### Script Behavior
- The Markdown files are saved in the specified output directory.
- Images referenced in the posts are downloaded and stored in an images folder inside the output directory.
- Each Markdown file contains metadata (title and date) in YAML front matter.

### Example Markdown Output
A typical generated Markdown file looks like this:

```markdown
---
title: "Sample Blog Post"
date: 2022-01-05
---

This is a paragraph with an image:

![Image](./images/image.jpg)

Another paragraph here.
```

### Directory Structure
After running the script, your output directory will look like this:

```arduino
output/
├── 2022-01-05-sample-blog-post.md
└── images/
    └── image.jpg
```

### Troubleshooting
#### Common Issues
- Missing Dependencies: Ensure requests and beautifulsoup4 are installed.
- Invalid Blogger File: Verify the XML file is correctly downloaded from Blogger.
- Failed Image Downloads: Check your internet connection and ensure the image URLs are accessible.

#### Debugging Tips
- Add print statements in the script to inspect content or URLs if needed.
- Ensure the output directory is writable and not restricted.

### Future Enhancements
- Support for additional Blogger XML features, such as labels or draft posts.
- Improved error handling for image download failures.
- Optional arguments for running the script without manual input.

### License
This project is open-source and free to use.

### Support
<a href="https://www.buymeacoffee.com/shashi" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

### Happy coding!
