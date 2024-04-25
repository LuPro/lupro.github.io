import argparse
import re
from os import listdir
from os.path import isfile, join, splitext

from mdparser import MarkdownParser


def ugly_md_converter(data):
    data = "<p>\n" + data
    data = data.replace("\n\n", "\n</p>\n<p>\n")
    data += "</p>"

    # I know, markdown is not a regular language
    # [\s\S] instead of . for multiline highlighting
    # code block
    data = re.sub(r"```([\s\S]+?)```", r"<pre>\g<1></pre>", data)

    # code inline
    data = re.sub(r"`(.+?)`", r"<code>\g<1></code>", data)

    # bold
    data = re.sub(r"\*\*(.+?)\*\*", r"<b>\g<1></b>", data)

    # italics
    data = re.sub(r"\*(.+?)\*", r"<i>\g<1></i>", data)

    # links
    data = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\g<2>">\g<1></a>', data)

    # media video
    data = re.sub(
        r"\[\[vid (.+?)\]\]",
        r'<video controls><source src="\g<1>"/>Video tag unsupported!</video>',
        data
    )

    # media image
    data = re.sub(r"\[\[(.+?)\]\]", r'<img src="\g<1>"/>', data)

    return data


def populate_template(md_data, template):
    blog_lines = md_data.split('\n')

    blog_title = blog_lines[0].replace("# ", "", 1)
    blog_subtitle = blog_lines[1]
    blog_date = blog_lines[2]
    blog_content = ugly_md_converter(('\n').join(blog_lines[3:]))

    parsed_tree = MarkdownParser().parse(md_data)
    print("----- DUMP")
    print(parsed_tree.dump())
    print("----- HTML")
    print(parsed_tree.html())

    template = template.replace("$TITLE", blog_title)
    template = template.replace("$SUBTITLE", blog_subtitle)
    template = template.replace("$DATE", blog_date)

    # template = template.replace("$CONTENT", blog_content)
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

        print("Parsing file", source_file)

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
