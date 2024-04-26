import argparse
import frontmatter
from os import listdir
from os.path import isfile, join, splitext
from datetime import datetime

from mdparser import MarkdownParser


def populate_template(md_data, template):
    metadata, content = frontmatter.parse(md_data)

    parsed_tree = MarkdownParser().parse(content)
    # print("----- DUMP")
    # print(parsed_tree.dump())
    # print("----- HTML")
    # print(parsed_tree.html())

    title = metadata.get("title", "Untitled Blog Post")
    byline = metadata.get("description", "")
    date = metadata.get("date", "")
    date_string = ""
    if date != "":
        date_string = date.strftime("%Y-%m-%d")

    template = template.replace("$TITLE", title)
    template = template.replace("$SUBTITLE", byline)
    template = template.replace("$DATE", date_string)

    template = template.replace("$CONTENT", parsed_tree.html())
    return template


def parse_blogs(template):
    source_path = "blog_sources"
    dest_path = "blog"
    source_files = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    print("Found files", source_files)

    for source_file in source_files:
        if splitext(source_file)[1] != ".md":
            continue

        # print("Parsing file", source_file)

        with open(join(source_path, source_file), 'r') as blog_reader:
            blog_source = blog_reader.read()
            compiled_blog = populate_template(blog_source, template)

            file_name = splitext(source_file)[0]
            dest_full_path = join(dest_path, file_name + ".html")
            with open(dest_full_path, "w") as blog_writer:
                blog_writer.write(compiled_blog)


def main():
    arg_parser = argparse.ArgumentParser(
        description="Compile Markdown files into HTML files based on template")
    arguments = arg_parser.parse_args()

    template = ""
    with open('blog/blog_template.html', 'r') as template_reader:
        template = template_reader.read()

    parse_blogs(template)


if __name__ == '__main__':
    main()
