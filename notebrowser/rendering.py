"""Functions for rendering pages."""
from functools import reduce
from pathlib import Path
from typing import Any

from notebrowser.sitedata import SiteData
from notebrowser.uri import URI, get_references


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
    return html_list(
        [f"{uri}: {record.name}" for uri, record in site_data.records.items()]
    )


def render_record_page(site_data: SiteData, uri: URI) -> str:
    """Render a page for a single record."""
    rec = site_data.records[uri]
    return f"<h1>{rec.name}</h1>\n<p>{rec.description}</p>"
