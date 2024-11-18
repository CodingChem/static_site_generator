import os
from modules.files import copy_files as file
from modules.text_node.textparser import extract_title, markdown_to_html_node


def main():
    # reset directory
    public_dir = os.path.curdir + "/public/"
    static_dir = os.path.curdir + "/static/"
    file.clear_directory(public_dir)
    file.copy_files(static_dir, public_dir)
    from_path = os.path.curdir + "/content"
    template_path = os.path.curdir + "/template.html"
    dest_path = os.path.curdir + "/public"
    generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    markdown_title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    document = template.replace("{{ Title }}", markdown_title).replace(
        "{{ Content }}", html
    )
    dest_dirs = "/".join(dest_path.split("/")[:-1]) + "/"
    if not os.path.exists(dest_dirs):
        os.makedirs(dest_dirs)

    with open(dest_path, "w") as output:
        output.write(document)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(
            dir_path_content, template_path, dest_dir_path.replace(".md", ".html")
        )
    else:
        for entry in os.listdir(dir_path_content):
            new_content, new_dest = (
                dir_path_content + "/" + entry,
                dest_dir_path + "/" + entry,
            )
            generate_pages_recursive(new_content, template_path, new_dest)


if __name__ == "__main__":
    main()
