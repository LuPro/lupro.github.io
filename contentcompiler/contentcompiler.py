import argparse
import frontmatter
from os import listdir
from os.path import isfile, join, splitext
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

from mdparser import MarkdownParser

_base_url = "https://lprod.dev/"
_base_blog_url = _base_url + "blog/"


def populate_template(md_data, template):
    metadata, content = frontmatter.parse(md_data)

    parsed_tree = MarkdownParser().parse(content)

    title = metadata.get("title", "Untitled Blog Post")
    byline = metadata.get("description", "")
    preview = metadata.get("preview", "")
    date = metadata.get("date", "")
    if type(date) == datetime:
        full_date = datetime(date.year, date.month, date.day, date.hour, tzinfo=timezone.utc)
    else:
        full_date = datetime(date.year, date.month, date.day, tzinfo=timezone.utc)

    date_string = ""
    if date != "":
        date_string = date.strftime("%Y-%m-%d")
    tags = metadata.get("tags", "")

    template = template.replace("$TITLE", title)
    template = template.replace("$SUBTITLE", byline)
    template = template.replace("$DATE", date_string)

    content_html = parsed_tree.html()
    # print(parsed_tree.dump())
    feed_html = parsed_tree.html(True)
    template = template.replace("$CONTENT", content_html)
    return {
        "title": title,
        "byline": byline,
        "preview": preview,
        "date": full_date,
        "tags": tags,
        "body": template,
        "embed_body": byline + "\n\n" + feed_html
    }


def parse_blogs(template):
    source_path = "blog_sources"
    dest_path = "blog"
    source_files = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    blogs = []
    print("Parsing blogs", source_files)

    for source_file in source_files:
        if splitext(source_file)[1] != ".md":
            continue

        with open(join(source_path, source_file), 'r') as blog_reader:
            blog_source = blog_reader.read()
            data = populate_template(blog_source, template)

            file_name = splitext(source_file)[0]
            data["url"] = _base_blog_url + file_name + ".html"
            blogs.append(data)

            dest_full_path = join(dest_path, file_name + ".html")
            with open(dest_full_path, "w") as blog_writer:
                blog_writer.write(data["body"])

    kde_feed = FeedGenerator()
    kde_feed.title("lprod KDE Blog")
    kde_feed.link(href=_base_url + "kde_rss.xml", rel="alternate")
    kde_feed.link(href=_base_url + "kde_rss.xml", rel="self")
    kde_feed.description("My exploits in and around KDE projects")
    kde_feed.language("en")
    kde_feed.lastBuildDate(datetime.now(timezone.utc))

    global_feed = FeedGenerator()
    global_feed.title("lprod Blog")
    global_feed.link(href=_base_url + "rss.xml", rel="alternate")
    global_feed.link(href=_base_url + "rss.xml", rel="self")
    global_feed.description("Random ramblings in various projects I work on")
    global_feed.language("en")
    global_feed.lastBuildDate(datetime.now(timezone.utc))

    for blog in blogs:
        global_entry = global_feed.add_entry()
        global_entry.id(blog["url"])
        global_entry.title(blog["title"])
        global_entry.link(href=blog["url"])
        global_entry.description(blog["embed_body"])
        global_entry.author({"name": "Luis Büchi"})
        global_entry.published(blog["date"])

        if "KDE" in blog["tags"]:
            kde_entry = kde_feed.add_entry()
            kde_entry.id(blog["url"])
            kde_entry.title(blog["title"])
            kde_entry.link(href=blog["url"])
            kde_entry.description(blog["embed_body"])
            kde_entry.author({"name": "Luis Büchi"})
            kde_entry.published(blog["date"])

    # print(global_feed.rss_str(pretty=True))
    global_feed.rss_file("rss.xml")
    # global_feed.atom_file("atom.xml")
    # print(kde_feed.rss_str(pretty=True))
    kde_feed.rss_file("kde_rss.xml")
    # kde_feed.atom_file("kde_atom.xml")


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
