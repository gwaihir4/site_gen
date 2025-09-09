import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from: {from_path} -> {dest_path} | Using: {template_path}")
    with open(from_path, "r") as markdown_file:
        markdown_file_content = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_file_content = template_file.read()

    title = extract_title(markdown_file_content)
    html_content = markdown_to_html_node(markdown_file_content).to_html()
    template_file_content = template_file_content.replace("{{ Title }}", title)
    template_file_content = template_file_content.replace("{{ Content }}", html_content)

    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(dest_path,"w") as new_file:
        new_file.write(template_file_content)

def extract_title(markdown):
    if markdown.startswith("# "):
        title = markdown.split("\n")[0]
        title = title.replace("# ", "", 1)
        return title
    raise Exception ("H1 title not found")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    elements = os.listdir(dir_path_content)
    for element in elements:
        path_to_element = os.path.join(dir_path_content, element)
        relative_path = os.path.relpath(path_to_element, dir_path_content)
        path_to_dest = os.path.join(dest_dir_path,relative_path)
        if os.path.isfile(path_to_element) and path_to_element[-3:] == ".md": # if element is file
            path_to_dest = os.path.splitext(path_to_dest)[0] + ".html"
            print(f"Generating page from: {path_to_element} -> {path_to_dest} | Using: {template_path}")
            generate_page(path_to_element, template_path, path_to_dest)
        elif os.path.isdir(path_to_element): # element is directory
            print(f"Iterating to: {path_to_element} | {path_to_dest}")
            os.makedirs(path_to_dest, exist_ok=True)
            generate_pages_recursive(path_to_element, template_path, path_to_dest)