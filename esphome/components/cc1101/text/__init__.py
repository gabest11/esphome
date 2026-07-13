import esphome.codegen as cg
from esphome.components import mqtt, text, web_server
import esphome.config_validation as cv
from esphome.const import (
    CONF_ENTITY_CATEGORY,
    CONF_ICON,
    CONF_ID,
    CONF_MQTT_ID,
    CONF_WEB_SERVER,
    ENTITY_CATEGORY_CONFIG,
)
from esphome.core import CORE
from esphome.cpp_generator import MockObjClass
from esphome.cpp_helpers import setup_entity

from .. import CC1101_COMPONENT_SCHEMA, CONF_CC1101_ID, for_each_conf, ns

CONF_DUMMY_TEXT = "dummy_text"
ICON_FORMAT_TEXT = "mdi:format-text"

DummyText = ns.class_("DummyText", text.Text)

# The text component isn't implemented the same way as switch, select, number.
# It is not possible to create our own text platform as it is now, so I adopted
# the necessary code from those.

_TEXT_SCHEMA = (
    cv.ENTITY_BASE_SCHEMA.extend(web_server.WEBSERVER_SORTING_SCHEMA)
    .extend(cv.MQTT_COMMAND_COMPONENT_SCHEMA)
    .extend(
        {
            cv.OnlyWith(CONF_MQTT_ID, "mqtt"): cv.declare_id(mqtt.MQTTTextComponent),
        }
    )
)

_UNDEF = object()


def text_schema(
    class_: MockObjClass = _UNDEF,
    *,
    entity_category: str = _UNDEF,
    device_class: str = _UNDEF,
    icon: str = _UNDEF,
):
    schema = _TEXT_SCHEMA
    if class_ is not _UNDEF:
        schema = schema.extend({cv.GenerateID(): cv.declare_id(class_)})
    if entity_category is not _UNDEF:
        schema = schema.extend(
            {
                cv.Optional(
                    CONF_ENTITY_CATEGORY, default=entity_category
                ): cv.entity_category
            }
        )
    if icon is not _UNDEF:
        schema = schema.extend({cv.Optional(CONF_ICON, default=icon): cv.icon})
    return schema


TEXT_SCHEMA = text_schema()  # for compatibility


async def setup_text_core_(
    var,
    config,
    *,
    min_length: int | None,
    max_length: int | None,
    pattern: str | None,
):
    await setup_entity(var, config)
    cg.add(var.traits.set_min_length(min_length))
    cg.add(var.traits.set_max_length(max_length))
    if pattern is not None:
        cg.add(var.traits.set_pattern(pattern))

    if (mqtt_id := config.get(CONF_MQTT_ID)) is not None:
        mqtt_ = cg.new_Pvariable(mqtt_id, var)
        await mqtt.register_mqtt_component(mqtt_, config)

    if web_server_config := config.get(CONF_WEB_SERVER):
        await web_server.add_entity_config(var, web_server_config)


async def register_text(
    var,
    config,
    min_length: int | None = 0,
    max_length: int | None = 255,
    pattern: str | None = None,
):
    if not CORE.has_id(config[CONF_ID]):
        var = cg.Pvariable(config[CONF_ID], var)
    cg.add(cg.App.register_text(var))
    await setup_text_core_(
        var, config, min_length=min_length, max_length=max_length, pattern=pattern
    )


TYPES = {
    None: {
        CONF_DUMMY_TEXT: [
            text_schema(
                DummyText,
                entity_category=ENTITY_CATEGORY_CONFIG,
                icon=ICON_FORMAT_TEXT,
            ),
            0,
            64,
        ]
    },
}

CONFIG_SCHEMA = CC1101_COMPONENT_SCHEMA.extend(
    {cv.Optional(k): v[0] for k, v in TYPES[None].items()},
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_CC1101_ID])

    async def new_text(c, args, setter):
        var = cg.new_Pvariable(c[CONF_ID])
        await register_text(var, c, min_length=args[0], max_length=args[1])
        await cg.register_parented(var, parent)
        cg.add(getattr(parent, setter + "_text")(var))

    await for_each_conf(config, TYPES, new_text)
