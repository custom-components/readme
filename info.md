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