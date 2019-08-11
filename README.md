# Readme

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE.md)

[![hacs][hacsbadge]](hacs)
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Use Jinja and data from Home Assistant to generate your README.md file_


## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `readme`.
4. Download _all_ the files from the `custom_components/readme/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. Choose:
   - Add `readme:` to your HA configuration.
   - In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Generate readme"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/readme/.translations/en.json
custom_components/readme/__init__.py
custom_components/readme/config_flow.py
custom_components/readme/const.py
custom_components/readme/default.j2
custom_components/readme/manifest.json
custom_components/readme/services.yaml
```

## Example configuration.yaml

```yaml
readme:
```

## Configuration options

Key | Type | Required | Description
-- | -- | -- | --
`convert_lovelace` | `boolean` | `False` | Generate a `ui.lovelace.yaml` file (only usefull if you use the UI to edit lovelace and want to share that in a yaml format.)

## Warnings!

This integration **will** replace your files!:

- README.md
- ui-lovelace.yaml (if you enable `convert_lovelace`)

## Usage

In the root of your configuration directory (folder) you will get a new directory (folder) called "templates" in that directory (folder) there will be a file called "README.j2" this is where you change the template that will be used for generation of the README.md file.

When you are happy with how the template look, run the service `readme.generate` in Home Assistant, this will generate the README.md file, and the ui-lovelace.yaml file if you enabled that.

## Usable variables

In addition to all [Jijna magic you can do](https://jinja.palletsprojects.com/en/2.10.x/templates/), there is also some additional variables you can use in the templates.

Variable | Description
-- | --
`states` | This is the same as with the rest of Home Assistant.
`custom_components` | Gives you a list of information about your custom_components

The information about custom components are fetched from the integrations manifest.json file, the folowing keys are aviable:

- `domain`
- `name`
- `documentation`
- `codeowner`

**Example usage of the  `custom_components` variable:**

```
{%- set custom_component_descriptions = {"readme": "Generates this awesome readme file."} -%}
{% for integration in custom_components %}
### [{{integration.name}}]({{integration.documentation}})
{% if integration.domain in custom_component_descriptions %}
_{{custom_component_descriptions[integration.domain]}}_
{% endif -%}
{% endfor -%}
```

If you only use this integration the output of that will be:

```
### [Generate readme](https://github.com/custom-components/readme)

_Generates this awesome readme file._
```

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[readme]: https://github.com/custom-components/readme
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/readme.svg?style=for-the-badge
[commits]: https://github.com/custom-components/readme/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/readme.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Joakim%20Sørensen%20%40ludeeus-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/readme.svg?style=for-the-badge
[releases]: https://github.com/custom-components/readme/releases
