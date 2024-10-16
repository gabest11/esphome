import esphome.codegen as cg
from esphome.components import switch
import esphome.config_validation as cv
from esphome.const import (
    DEVICE_CLASS_SWITCH,
    ENTITY_CATEGORY_CONFIG,
    ICON_SECURITY,
)
from .. import (
    CONF_SI4713_ID,
    Si4713Component,
    si4713_ns,
    CONF_SECTION_PILOT,
    CONF_SECTION_COMPRESSOR,
    CONF_SECTION_LIMITER,
    CONF_SECTION_ASQ,
    CONF_SECTION_RDS,
    CONF_SECTION_OUTPUT,
    CONF_MUTE,
    CONF_MONO,
    CONF_ENABLE,
    CONF_OVERMOD,
    CONF_IALL,
    CONF_IALH,
    CONF_GPIO1,
    CONF_GPIO2,
    CONF_GPIO3,
    ICON_SINE_WAVE,
    ICON_VOLUME_MUTE,
    ICON_EAR_HEARING,
    ICON_FORMAT_TEXT,
)

MuteSwitch = si4713_ns.class_("MuteSwitch", switch.Switch)
MonoSwitch = si4713_ns.class_("MonoSwitch", switch.Switch)
PilotEnableSwitch = si4713_ns.class_("PilotEnableSwitch", switch.Switch)
AcompEnableSwitch = si4713_ns.class_("AcompEnableSwitch", switch.Switch)
LimiterEnableSwitch = si4713_ns.class_("LimiterEnableSwitch", switch.Switch)
AsqOvermodEnableSwitch = si4713_ns.class_("AsqOvermodEnableSwitch", switch.Switch)
AsqIallEnableSwitch = si4713_ns.class_("AsqIallEnableSwitch", switch.Switch)
AsqIalhEnableSwitch = si4713_ns.class_("AsqIalhEnableSwitch", switch.Switch)
RdsEnable = si4713_ns.class_("RdsEnable", switch.Switch)
RDSEnableSwitch = si4713_ns.class_("RDSEnableSwitch", switch.Switch)
GPIOSwitch = si4713_ns.class_("GPIOSwitch", switch.Switch)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_SI4713_ID): cv.use_id(Si4713Component),
        cv.Optional(CONF_MUTE): switch.switch_schema(
            MuteSwitch,
            device_class=DEVICE_CLASS_SWITCH,
            entity_category=ENTITY_CATEGORY_CONFIG,
            icon=ICON_VOLUME_MUTE,
        ),
        cv.Optional(CONF_MONO): switch.switch_schema(
            MonoSwitch,
            device_class=DEVICE_CLASS_SWITCH,
            entity_category=ENTITY_CATEGORY_CONFIG,
            icon=ICON_EAR_HEARING,
        ),
        cv.Optional(CONF_SECTION_PILOT): cv.Schema(
            {
                cv.Optional(CONF_ENABLE): switch.switch_schema(
                    PilotEnableSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    icon=ICON_SINE_WAVE,
                ),
            }
        ),
        cv.Optional(CONF_SECTION_COMPRESSOR): cv.Schema(
            {
                cv.Optional(CONF_ENABLE): switch.switch_schema(
                    AcompEnableSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    icon=ICON_SINE_WAVE,
                ),
            }
        ),
        cv.Optional(CONF_SECTION_LIMITER): cv.Schema(
            {
                cv.Optional(CONF_ENABLE): switch.switch_schema(
                    LimiterEnableSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    icon=ICON_SINE_WAVE,
                ),
            }
        ),
        cv.Optional(CONF_SECTION_ASQ): cv.Schema(
            {
                cv.Optional(CONF_OVERMOD): switch.switch_schema(
                    AsqOvermodEnableSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    # icon=ICON_,
                ),
                cv.Optional(CONF_IALL): switch.switch_schema(
                    AsqIallEnableSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    # icon=ICON_,
                ),
                cv.Optional(CONF_IALH): switch.switch_schema(
                    AsqIalhEnableSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    # icon=ICON_,
                ),
            }
        ),
        cv.Optional(CONF_SECTION_RDS): cv.Schema(
            {
                cv.Optional(CONF_ENABLE): switch.switch_schema(
                    RDSEnableSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    icon=ICON_FORMAT_TEXT,
                ),
            }
        ),
        cv.Optional(CONF_SECTION_OUTPUT): cv.Schema(
            {
                cv.Optional(CONF_GPIO1): switch.switch_schema(
                    GPIOSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    # icon=,
                ),
                cv.Optional(CONF_GPIO2): switch.switch_schema(
                    GPIOSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    # icon=,
                ),
                cv.Optional(CONF_GPIO3): switch.switch_schema(
                    GPIOSwitch,
                    device_class=DEVICE_CLASS_SWITCH,
                    entity_category=ENTITY_CATEGORY_CONFIG,
                    # icon=,
                ),
            }
        )
    }
)


async def new_switch(parent, config, id, setter):
    if c := config.get(id):
        s = await switch.new_switch(c)
        await cg.register_parented(s, parent)
        cg.add(setter(s))
        return s


async def to_code(config):
    parent = await cg.get_variable(config[CONF_SI4713_ID])
    await new_switch(parent, config, CONF_MUTE, parent.set_mute_switch)
    await new_switch(parent, config, CONF_MONO, parent.set_mono_switch)
    if pilot_config := config.get(CONF_SECTION_PILOT):
        await new_switch(parent, pilot_config, CONF_ENABLE, parent.set_pilot_enable_switch)
    if compressor_config := config.get(CONF_SECTION_COMPRESSOR):
        await new_switch(parent, compressor_config, CONF_ENABLE, parent.set_acomp_enable_switch)
    if limiter_config := config.get(CONF_SECTION_LIMITER):
        await new_switch(parent, limiter_config, CONF_ENABLE, parent.set_limiter_enable_switch)
    if asq_config := config.get(CONF_SECTION_ASQ):
        await new_switch(parent, asq_config, CONF_OVERMOD, parent.set_asq_overmod_enable_switch)
        await new_switch(parent, asq_config, CONF_IALL, parent.set_asq_iall_enable_switch)
        await new_switch(parent, asq_config, CONF_IALH, parent.set_asq_ialh_enable_switch)
    if rds_config := config.get(CONF_SECTION_RDS):
        await new_switch(parent, rds_config, CONF_ENABLE, parent.set_rds_enable_switch)
    if output_config := config.get(CONF_SECTION_OUTPUT):
        gpio1 = await new_switch(parent, output_config, CONF_GPIO1, parent.set_gpio1_switch)
        gpio2 = await new_switch(parent, output_config, CONF_GPIO2, parent.set_gpio2_switch)
        gpio3 = await new_switch(parent, output_config, CONF_GPIO3, parent.set_gpio3_switch)
        cg.add(gpio1.set_pin(1))
        cg.add(gpio2.set_pin(2))
        cg.add(gpio3.set_pin(3))
