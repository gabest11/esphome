import esphome.codegen as cg
from esphome.components import switch
import esphome.config_validation as cv
from esphome.const import DEVICE_CLASS_SWITCH, ENTITY_CATEGORY_CONFIG

from .. import (
    CC1101_COMPONENT_SCHEMA,
    CONF_AGC,
    CONF_CARRIER_SENSE_ABOVE_THRESHOLD,
    CONF_CC1101_ID,
    CONF_DC_BLOCKING_FILTER,
    CONF_LNA_PRIORITY,
    CONF_TUNER,
    for_each_conf,
    ns,
)

DcBlockingFilterSwitch = ns.class_("DcBlockingFilterSwitch", switch.Switch)
CarrierSenseAboveThresholdSwitch = ns.class_(
    "CarrierSenseAboveThresholdSwitch", switch.Switch
)
AgcLnaPrioritySwitch = ns.class_("AgcLnaPrioritySwitch", switch.Switch)

TYPES = {
    None: {
        CONF_DC_BLOCKING_FILTER: [
            switch.switch_schema(
                DcBlockingFilterSwitch,
                device_class=DEVICE_CLASS_SWITCH,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
        ],
    },
    CONF_TUNER: {
        CONF_CARRIER_SENSE_ABOVE_THRESHOLD: [
            switch.switch_schema(
                CarrierSenseAboveThresholdSwitch,
                device_class=DEVICE_CLASS_SWITCH,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
        ],
    },
    CONF_AGC: {
        CONF_LNA_PRIORITY: [
            switch.switch_schema(
                AgcLnaPrioritySwitch,
                device_class=DEVICE_CLASS_SWITCH,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
        ],
    },
}

CONFIG_SCHEMA = CC1101_COMPONENT_SCHEMA.extend(
    {cv.Optional(k): v[0] for k, v in TYPES[None].items()},
    {
        cv.Optional(CONF_TUNER): cv.Schema(
            {cv.Optional(k): v[0] for k, v in TYPES[CONF_TUNER].items()}
        ),
        cv.Optional(CONF_AGC): cv.Schema(
            {cv.Optional(k): v[0] for k, v in TYPES[CONF_AGC].items()}
        ),
    },
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_CC1101_ID])

    async def new_switch(c, args, setter):
        s = await switch.new_switch(c)
        await cg.register_parented(s, parent)
        cg.add(getattr(parent, setter + "_switch")(s))

    await for_each_conf(config, TYPES, new_switch)
