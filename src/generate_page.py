import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from: {from_path} -> {dest_path} \n Using: {template_path}")
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
        title = title.replace("# ", "")
        return title
    raise Exception ("H1 title not found")
    