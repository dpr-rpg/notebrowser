"""Functions for building the site."""
import shutil
from importlib import resources
from pathlib import Path
from typing import Callable

from notebrowser import rendering
from notebrowser.assets import css, fonts
from notebrowser.configuration import (
    Configuration,
    Directories,
    SiteData,
    config_fn,
    load_configuration,
)
from notebrowser.loading import load_records


def initialize(base_dir: Path):
    """Initialize project."""
    initialize_project_directory(base_dir)
    deploy_default_assets(base_dir)
    create_config_file(base_dir)


def initialize_project_directory(base_dir: Path) -> None:
    """Create input data directory structure."""
    for d in Directories():
        (base_dir / d).mkdir(parents=True, exist_ok=True)


def deploy_default_assets(base_dir: Path) -> None:
    """Add default css and font files to assets."""
    dirs = Directories()
    _deploy_assets(css, ".css", base_dir / dirs.css)
    _deploy_assets(fonts, ".woff2", base_dir / dirs.fonts, is_binary=True)


def create_config_file(base_dir: Path) -> Path:
    """Write a default configuration file."""
    config_file = base_dir / config_fn
    config = Configuration()
    config.to_file(config_file)
    return config_file


def make_site(base_dir: Path) -> SiteData:
    """Load data, clean site directory, and build site."""
    dirs = Directories()
    configuration = load_configuration(base_dir / config_fn)
    records = load_records(base_dir / dirs.records)
    site_data = SiteData(
        site_dir=base_dir / dirs.site,
        config=configuration,
        records=records,
    )
    pages = render_pages(site_data)
    clean(site_data)
    write_pages(site_data, pages)
    copy_assets(site_data, base_dir / dirs.assets)
    return site_data


def _deploy_assets(module, suffix: str, target_dir: Path, is_binary=False) -> None:
    read: Callable
    if is_binary:
        read = resources.read_binary
        mode = "wb"
    else:
        read = resources.read_text
        mode = "w"
    for asset in resources.files(module).iterdir():
        if asset.name.endswith(suffix):
            data = read(module, asset.name)
            with open(target_dir / asset.name, mode) as new_file:
                new_file.write(data)


def clean(site_data: SiteData) -> None:
    """Remove any existing site files."""
    if site_data.site_dir.exists():
        shutil.rmtree(site_data.site_dir)


def render_pages(site_data: SiteData) -> dict[Path, str]:
    """Create page content."""
    homepage = (site_data.homepage, rendering.render_homepage(site_data))
    record_pages = [
        (page, rendering.render_record_page(site_data, uri))
        for uri, page in site_data.record_pages.items()
    ]
    all_pages = [homepage] + record_pages
    return {
        path: rendering.apply_links(content, site_data) for path, content in all_pages
    }


def write_pages(site_data: SiteData, pages: dict[Path, str]) -> None:
    """Make directories and write pages to filesystem."""
    for page, content in pages.items():
        page_path = site_data.site_dir / page.relative_to(site_data.root)
        if not page_path.parent.exists():
            page_path.parent.mkdir(parents=True)
        with open(page_path, "w") as f:
            f.write(content)


def copy_assets(site_data: SiteData, asset_source: Path) -> None:
    """Copy assets to site directory."""
    asset_dest = site_data.site_dir / site_data.asset_dir.relative_to(site_data.root)
    if asset_source.exists():
        shutil.copytree(asset_source, asset_dest, dirs_exist_ok=True)
