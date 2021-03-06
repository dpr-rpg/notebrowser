"""Functions for rendering pages."""
from functools import reduce
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, Template

from notebrowser.configuration import SiteData
from notebrowser.records import Record, TextRecord
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
    template = jinja_env.get_template("homepage.html.jinja")
    return template.render(site_data=site_data)


def _template_dispatch(record: Record) -> Template:
    if isinstance(record, TextRecord):
        template_file = "textrecord_page.html.jinja"
    else:
        template_file = "record_page.html.jinja"
    return jinja_env.get_template(template_file)


def render_record_page(site_data: SiteData, uri: URI) -> str:
    """Render a page for a single record."""
    record = site_data.records[uri]
    template = _template_dispatch(record)
    mentions = [
        m_uri for m_uri, m_rec in site_data.records.items() if uri in m_rec.references
    ]
    return template.render(site_data=site_data, record=record, mentions=mentions)
