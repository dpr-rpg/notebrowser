"""Functions for rendering pages."""
from functools import reduce
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader

from notebrowser.sitedata import SiteData
from notebrowser.uri import URI, get_references

jinja_env = Environment(loader=PackageLoader("notebrowser", "templates"))


def html_link(path: Path, text: str) -> str:
    """Generate an html link."""
    return f'<a href="{path}">{text}</a>'


def html_list(items: list[Any]) -> str:
    """Render a list of items as an HTML list."""
    return "<ul>" + "".join(f"<li>{str(item)}</li>" for item in items) + "</ul>\n"


def record_link(site_data: SiteData, uri: URI) -> str:
    """Generate a link to a record page."""
    record = site_data.records[uri]
    path = site_data.record_pages[uri]
    if record.shortname:
        name = record.shortname
    else:
        name = record.name
    return html_link(path, name)


def apply_links(text: str, site_data: SiteData) -> str:
    """Replace URIs with links to pages."""
    references = get_references(text)
    return reduce(
        lambda t, uri: t.replace(str(uri), record_link(site_data, uri)),
        references,
        text,
    )


def render_homepage(site_data: SiteData) -> str:
    """Render the homepage."""
    template = jinja_env.get_template("homepage.html")
    return template.render(site_data=site_data)


def render_record_page(site_data: SiteData, uri: URI) -> str:
    """Render a page for a single record."""
    template = jinja_env.get_template("record_page.html")
    record = site_data.records[uri]
    return template.render(site_data=site_data, record=record)
