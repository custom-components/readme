"""
Use Jinja and data from Home Assistant to generate your README.md file

For more details about this component, please refer to
https://github.com/custom-components/readme
"""
import os
import json
from datetime import timedelta
from jinja2 import Template
import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery
from homeassistant.helpers.template import AllStates
from homeassistant.util import Throttle

from integrationhelper import Logger
from integrationhelper.const import CC_STARTUP_VERSION

from .const import DOMAIN_DATA, DOMAIN, ISSUE_URL, REQUIRED_FILES, VERSION

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Optional("convert_lovelace"): cv.boolean})},
    extra=vol.ALLOW_EXTRA,
)


class ReadmeConfiguration:
    """Configuration class for readme."""

    convert_lovelace = False


async def async_setup(hass, config):
    """Set up this component using YAML."""
    if config.get(DOMAIN) is None:
        # We get her if the integration is set up using config flow
        return True

    # Print startup message
    Logger("custom_components.readme").info(
        CC_STARTUP_VERSION.format(
            name=DOMAIN.capitalize(), version=VERSION, issue_link=ISSUE_URL
        )
    )

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # Create DATA dict
    hass.data[DOMAIN_DATA] = {}

    # Get "global" configuration.
    ReadmeConfiguration.convert_lovelace = config[DOMAIN].get("convert_lovelace")
    await add_services(hass)
    create_initial_files(hass)

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data={}
        )
    )
    return True


async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""
    conf = hass.data.get(DOMAIN_DATA)
    if config_entry.source == config_entries.SOURCE_IMPORT:
        if conf is None:
            hass.async_create_task(
                hass.config_entries.async_remove(config_entry.entry_id)
            )
        return False

    # Print startup message
    Logger("custom_components.readme").info(
        CC_STARTUP_VERSION.format(
            name=DOMAIN.capitalize(), version=VERSION, issue_link=ISSUE_URL
        )
    )

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # Create DATA dict
    hass.data[DOMAIN_DATA] = {}

    # Get "global" configuration.
    ReadmeConfiguration.convert_lovelace = config_entry.data.get("convert", False)
    await add_services(hass)
    create_initial_files(hass)

    return True


async def check_files(hass):
    """Return bool that indicates if all files are present."""
    # Verify that the user downloaded all files.
    base = f"{hass.config.path()}/custom_components/{DOMAIN}/"
    missing = []
    for file in REQUIRED_FILES:
        fullpath = "{}{}".format(base, file)
        if not os.path.exists(fullpath):
            missing.append(file)

    if missing:
        Logger("custom_components.readme").critical(
            f"The following files are missing: {str(missing)}"
        )
        returnvalue = False
    else:
        returnvalue = True

    return returnvalue


def create_initial_files(hass):
    """Create the initial files for this integration."""
    base = hass.config.path()

    if not os.path.exists(f"{base}/templates"):
        os.mkdir(f"{base}/templates")

    if not os.path.exists(f"{base}/templates/README.j2"):
        from shutil import copyfile

        copyfile(
            f"{base}/custom_components/readme/default.j2",
            f"{base}/templates/README.j2",
        )


def convert_lovelace(hass):
    """Convert the lovelace configuration."""
    base = hass.config.path()
    if os.path.exists(f"{base}/.storage/lovelace"):
        import yaml

        with open(f"{base}/.storage/lovelace", "r") as lovelace:
            content = lovelace.read()
            content = json.loads(content)
        content = content.get("data", {})
        content = content.get("config", {})
        with open(f"{base}/ui-lovelace.yaml", "w") as out_file:
            yaml.dump(content, out_file, default_flow_style=False)


async def async_remove_entry(hass, config_entry):
    """Handle removal of an entry."""
    hass.services.async_remove(DOMAIN, "generate")


async def add_services(hass):
    """Add services."""
    # Service registration
    async def service_generate(call):
        """Generate the files."""
        base = hass.config.path()
        if ReadmeConfiguration.convert_lovelace:
            convert_lovelace(hass)
        custom_components = get_custom_components(hass)
        hacs_components = get_hacs_components(hass)
        variables = {
            "custom_components": custom_components,
            "states": AllStates(hass),
            "hacs_components": hacs_components,
        }

        with open(f"{base}/templates/README.j2", "r") as readme:
            content = readme.read()

        template = Template(content)
        try:
            render = template.render(variables)
            with open(f"{base}/README.md", "w") as out_file:
                out_file.write(render)
        except Exception as exception:
            Logger("custom_components.readme").error(exception)

    hass.services.async_register(DOMAIN, "generate", service_generate)


def get_hacs_components(hass):
    try:
        from custom_components.hacs.share import get_hacs
    except ImportError:
        return []

    hacs = get_hacs()
    repositories = hacs.repositories
    installed = []

    for repo in repositories:
        if repo.data.installed:
            installed.append(
                {
                    "additional_info": repo.information.additional_info,
                    "authors": repo.data.authors,
                    "available_version": repo.display_available_version,
                    "beta": repo.data.show_beta,
                    "can_install": repo.can_install,
                    "category": repo.data.category,
                    "country": repo.data.country,
                    "config_flow": repo.data.config_flow,
                    "custom": repo.custom,
                    "default_branch": repo.data.default_branch,
                    "description": repo.data.description,
                    "domain": repo.data.domain,
                    "downloads": repo.data.downloads,
                    "file_name": repo.data.file_name,
                    "first_install": repo.status.first_install,
                    "full_name": repo.data.full_name,
                    "hide": repo.data.hide,
                    "hide_default_branch": repo.data.hide_default_branch,
                    "homeassistant": repo.data.homeassistant,
                    "id": repo.data.id,
                    "info": repo.information.info,
                    "installed_version": repo.display_installed_version,
                    "installed": repo.data.installed,
                    "issues": repo.data.open_issues,
                    "javascript_type": repo.information.javascript_type,
                    "last_updated": repo.data.last_updated,
                    "local_path": repo.content.path.local,
                    "main_action": repo.main_action,
                    "name": get_repository_name(repo),
                    "new": repo.data.new,
                    "pending_upgrade": repo.pending_upgrade,
                    "releases": repo.data.published_tags,
                    "selected_tag": repo.data.selected_tag,
                    "stars": repo.data.stargazers_count,
                    "state": repo.state,
                    "status_description": repo.display_status_description,
                    "status": repo.display_status,
                    "topics": repo.data.topics,
                    "updated_info": repo.status.updated_info,
                    "version_or_commit": repo.display_version_or_commit,
                    "documentation": "https://github.com/" + repo.data.full_name,
                }
            )

    return installed


def get_repository_name(repository) -> str:
    """Return the name of the repository for use in the frontend."""
    name = None

    if repository.repository_manifest.name:
        name = repository.repository_manifest.name
    else:
        name = repository.data.full_name.split("/")[-1]

    name = name.replace("-", " ").replace("_", " ").strip()

    if name.isupper():
        return name

    return name.title()


def get_custom_components(hass):
    """Return a list with custom_component info."""
    base = hass.config.path()
    custom_components = []

    for integration in os.listdir(f"{base}/custom_components"):
        if os.path.exists(f"{base}/custom_components/{integration}/manifest.json"):
            with open(
                f"{base}/custom_components/{integration}/manifest.json", "r"
            ) as manifest:
                content = manifest.read()
                content = json.loads(content)
            custom_components.append(
                {
                    "domain": content["domain"],
                    "name": content["name"],
                    "documentation": content["documentation"],
                    "codeowners": content["codeowners"],
                }
            )

    return custom_components
