import argparse
import frontmatter
from os import listdir
from os.path import isfile, join, splitext, basename
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

from mdparser import MarkdownParser

_base_url = "https://lprod.dev"
_base_blog_url = "/blog/"


def debug_parse_blog(path):
    with open(path, 'r') as blog_reader:
        blog_source = blog_reader.read()
        metadata, content = frontmatter.parse(blog_source)
        parsed_tree = MarkdownParser().parse(content)
        print(parsed_tree.dump())


def populate_blog_template(md_data, template):
    metadata, content = frontmatter.parse(md_data)

    parsed_tree = MarkdownParser().parse(content)

    title = metadata.get("title", "Untitled Blog Post")
    byline = metadata.get("description", "")
    preview = metadata.get("preview", "")
    date = metadata.get("date", "")
    if date is datetime:
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
    template = template.replace("$CURR_YEAR", str(datetime.now().year))

    content_html = parsed_tree.html()
    # print(parsed_tree.dump())
    feed_html = parsed_tree.html(True)
    template = template.replace("$CONTENT", content_html)
    return {
        "title": title,
        "byline": byline,
        "preview": preview,
        "date": full_date,
        "datestr": date_string,
        "tags": tags,
        "body": template,
        "embed_body": byline + "\n\n" + feed_html
    }


def parse_blogs(template):
    source_path = "blog_sources"
    dest_path = "blog"
    folder_entries = [f for f in listdir(source_path)]
    subfolders = [f for f in folder_entries if not isfile(join(source_path, f))]
    source_files = [f for f in listdir(source_path) if isfile(join(source_path, f))]
    source_files += [join(s, f) for s in subfolders for f in listdir(join(source_path, s)) if isfile(join(source_path, s, f))]
    blogs = []
    written_blogs = []
    print("Parsing blogs", source_files)

    for source_file in source_files:
        print("Parsing", source_file)
        if splitext(source_file)[1] != ".md":
            continue

        with open(join(source_path, source_file), 'r') as blog_reader:
            blog_source = blog_reader.read()
            data = populate_blog_template(blog_source, template)
            file_name = splitext(basename(source_file))[0]
            data["url"] = _base_blog_url + file_name + ".html"

            blogs.append(data)

            dest_full_path = join(dest_path, file_name + ".html")
            if dest_full_path in written_blogs:
                raise Exception(f"Name collision with previous blog: {file_name}")

            with open(dest_full_path, "w") as blog_writer:
                blog_writer.write(data["body"])

            written_blogs.append(dest_full_path)

    kde_feed = FeedGenerator()
    kde_feed.title("lprod KDE Blog")
    kde_feed.link(href=_base_url + "/kde_rss.xml", rel="alternate")
    kde_feed.link(href=_base_url + "/kde_rss.xml", rel="self")
    kde_feed.description("My exploits in and around KDE projects")
    kde_feed.language("en")
    kde_feed.lastBuildDate(datetime.now(timezone.utc))

    global_feed = FeedGenerator()
    global_feed.title("lprod Blog")
    global_feed.link(href=_base_url + "/rss.xml", rel="alternate")
    global_feed.link(href=_base_url + "/rss.xml", rel="self")
    global_feed.description("Random ramblings in various projects I work on")
    global_feed.language("en")
    global_feed.lastBuildDate(datetime.now(timezone.utc))

    for blog in blogs:
        global_entry = global_feed.add_entry()
        global_entry.id(_base_url + blog["url"])
        global_entry.title(blog["title"])
        global_entry.link(href=_base_url + blog["url"])
        global_entry.description(blog["embed_body"])
        global_entry.author({"name": "Luis Büchi"})
        global_entry.published(blog["date"])

        if "KDE" in blog["tags"]:
            kde_entry = kde_feed.add_entry()
            kde_entry.id(_base_url + blog["url"])
            kde_entry.title(blog["title"])
            kde_entry.link(href=_base_url + blog["url"])
            kde_entry.description(blog["embed_body"])
            kde_entry.author({"name": "Luis Büchi"})
            kde_entry.published(blog["date"])

    # print(global_feed.rss_str(pretty=True))
    global_feed.rss_file("rss.xml")
    # global_feed.atom_file("atom.xml")
    # print(kde_feed.rss_str(pretty=True))
    kde_feed.rss_file("kde_rss.xml")
    # kde_feed.atom_file("kde_atom.xml")

    return blogs


def populate_card_template(data, template):
    template = template.replace("$TITLE", data["title"])
    template = template.replace("$PREVIEW", data["preview"])
    template = template.replace("$DATE", data["datestr"])
    template = template.replace("$URL", data["url"])
    template = template.replace("$TAGS", "\n".join([f"<span class='tag'>#{t}</span>" for t in data["tags"]]))

    return template


def update_main_page(blogs, main_template, filtered_page_template, card_template):
    cards = []
    blog_list = ""

    # All blogs
    blogs.sort(key=lambda x: x["date"], reverse=True)

    # Blogs sorted by their first tags for individual index pages
    filtered_blogs = {}

    for blog in blogs:
        iconSrc = ""
        altText = ""
        main_tag = blog["tags"][0]

        if main_tag == "TaleSpire":
            iconSrc = "static/assets/talespire-logo.svg"
            altText = "TaleSpire Logo"
        elif main_tag == "KDE":
            iconSrc = "static/assets/kde-logo-blue.svg"
            altText = "KDE Logo"

        entry = '<li>{}: <img class="icon" src="{}" alt="{}"/><a href="{}">{}</a></li>'.format(blog["datestr"], iconSrc, altText, blog["url"], blog["title"])

        if (main_tag not in filtered_blogs):
            filtered_blogs[main_tag] = {
                "cards": [],
                "blogs": []
            }

        card = populate_card_template(blog, card_template)

        # fill global list
        blog_list += entry
        if (len(cards) < 3):
            cards.append(card)

        # fill filtered list
        filtered_blogs[main_tag]["blogs"].append(entry)
        if (len(filtered_blogs[main_tag]["cards"]) < 3):
            filtered_blogs[blog["tags"][0]]["cards"].append(card)

    main_template = main_template.replace("$GALLERY", "\n".join(cards))
    main_template = main_template.replace("$BLOGS", blog_list)

    for tag, blog_elements in filtered_blogs.items():
        template_copy = filtered_page_template

        template_copy = template_copy.replace("$MAIN_TAG", tag)
        template_copy = template_copy.replace("$BLOGS", "\n".join(blog_elements["blogs"]))
        template_copy = template_copy.replace("$GALLERY", "\n".join(blog_elements["cards"]))
        with open(f"{tag.lower()}_blog.html", "w") as page_writer:
            page_writer.write(template_copy)

    with open("index.html", "w") as index_writer:
        index_writer.write(main_template)


def main():
    arg_parser = argparse.ArgumentParser(
        description="Compile Markdown files into HTML files based on template")
    arg_parser.add_argument('--manual', metavar='manual_source', help="Add path to a specific blog for parsing that one manually. Doesn't write an output file, just writes to stdout'")
    arguments = arg_parser.parse_args()

    if (arguments.manual != None):
        debug_parse_blog(arguments.manual)
        return

    post_template = ""
    with open('blog/blog_template.html', 'r') as template_reader:
        post_template = template_reader.read()

    blogs = parse_blogs(post_template)

    blog_template = ""
    with open('gallery_card_template.html', 'r') as template_reader:
        blog_template = template_reader.read()

    main_template = ""
    with open('main_page_template.html', 'r') as template_reader:
        main_template = template_reader.read()

    filtered_page_template = ""
    with open('tagged_blog_index_template.html', 'r') as template_reader:
        filtered_page_template = template_reader.read()

    update_main_page(blogs, main_template, filtered_page_template, blog_template)


if __name__ == '__main__':
    main()
