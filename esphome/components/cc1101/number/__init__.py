import esphome.codegen as cg
from esphome.components import number
import esphome.config_validation as cv
from esphome.const import (
    CONF_CHANNEL,
    CONF_FREQUENCY,
    CONF_MODE,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    ENTITY_CATEGORY_CONFIG,
    UNIT_DECIBEL,
    UNIT_DECIBEL_MILLIWATT,
)

from .. import (
    CC1101_COMPONENT_SCHEMA,
    CONF_AGC,
    CONF_BANDWIDTH,
    CONF_CARRIER_SENSE_ABS_THR,
    CONF_CC1101_ID,
    CONF_CHANNEL_SPACING,
    CONF_FSK_DEVIATION,
    CONF_IF_FREQUENCY,
    CONF_MSK_DEVIATION,
    CONF_OUTPUT_POWER,
    CONF_SYMBOL_RATE,
    CONF_TUNER,
    UNIT_KILO_HERTZ,
    for_each_conf,
    ns,
)

NumberMode = number.NumberMode

OutputPowerNumber = ns.class_("OutputPowerNumber", number.Number)
TunerFrequencyNumber = ns.class_("TunerFrequencyNumber", number.Number)
TunerIfFrequencyNumber = ns.class_("TunerIfFrequencyNumber", number.Number)
TunerBandwidthNumber = ns.class_("TunerBandwidthNumber", number.Number)
TunerChannelNumber = ns.class_("TunerChannelNumber", number.Number)
TunerChannelSpacingNumber = ns.class_("TunerChannelSpacingNumber", number.Number)
TunerFskDeviationNumber = ns.class_("TunerFskDeviationNumber", number.Number)
TunerMskDeviationNumber = ns.class_("TunerMskDeviationNumber", number.Number)
TunerSymbolRateNumber = ns.class_("TunerSymbolRateNumber", number.Number)
AgcCarrierSenseAbsThrNumber = ns.class_("AgcCarrierSenseAbsThrNumber", number.Number)

TYPES = {
    None: {
        CONF_OUTPUT_POWER: [
            number.number_schema(
                OutputPowerNumber,
                unit_of_measurement=UNIT_DECIBEL_MILLIWATT,
                device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.OUTPUT_POWER_MIN,
            ns.OUTPUT_POWER_MAX,
            0.1,
            NumberMode.NUMBER_MODE_SLIDER,
        ],
    },
    CONF_TUNER: {
        CONF_FREQUENCY: [
            number.number_schema(
                TunerFrequencyNumber,
                unit_of_measurement=UNIT_KILO_HERTZ,
                device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.FREQUENCY_MIN,
            ns.FREQUENCY_MAX,
            1,
        ],
        CONF_IF_FREQUENCY: [
            number.number_schema(
                TunerIfFrequencyNumber,
                unit_of_measurement=UNIT_KILO_HERTZ,
                device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.IF_FREQUENCY_MIN,
            ns.IF_FREQUENCY_MAX,
            0.001,
        ],
        CONF_BANDWIDTH: [
            number.number_schema(
                TunerBandwidthNumber,
                unit_of_measurement=UNIT_KILO_HERTZ,
                device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.BANDWIDTH_MIN,
            ns.BANDWIDTH_MAX,
            0.001,
        ],
        CONF_CHANNEL: [
            number.number_schema(
                TunerChannelNumber,
                # unit_of_measurement=,
                # device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.CHANNEL_MIN,
            ns.CHANNEL_MAX,
            1,
            # NumberMode.NUMBER_MODE_BOX,
        ],
        CONF_CHANNEL_SPACING: [
            number.number_schema(
                TunerChannelSpacingNumber,
                unit_of_measurement=UNIT_KILO_HERTZ,
                device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.CHANNEL_SPACING_MIN,
            ns.CHANNEL_SPACING_MAX,
            0.001,
        ],
        CONF_FSK_DEVIATION: [
            number.number_schema(
                TunerFskDeviationNumber,
                unit_of_measurement=UNIT_KILO_HERTZ,
                device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.FSK_DEVIATION_MIN,
            ns.FSK_DEVIATION_MAX,
            0.001,
        ],
        CONF_MSK_DEVIATION: [
            number.number_schema(
                TunerMskDeviationNumber,
                # unit_of_measurement=,
                # device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.MSK_DEVIATION_MIN,
            ns.MSK_DEVIATION_MAX,
            1,
        ],
        CONF_SYMBOL_RATE: [
            number.number_schema(
                TunerSymbolRateNumber,
                # unit_of_measurement=,
                # device_class=DEVICE_CLASS_FREQUENCY,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.SYMBOL_RATE_MIN,
            ns.SYMBOL_RATE_MAX,
            1,
        ],
    },
    CONF_AGC: {
        CONF_CARRIER_SENSE_ABS_THR: [
            number.number_schema(
                AgcCarrierSenseAbsThrNumber,
                unit_of_measurement=UNIT_DECIBEL,
                device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
                entity_category=ENTITY_CATEGORY_CONFIG,
                # icon=ICON_,
            ),
            ns.CARRIER_SENSE_ABS_THR_MIN,
            ns.CARRIER_SENSE_ABS_THR_MAX,
            1,
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

    async def new_number(c, args, setter):
        # only override mode when it's set to auto in user config
        if CONF_MODE not in c or c[CONF_MODE] == NumberMode.NUMBER_MODE_AUTO:
            if len(args) > 3 and args[3] is not None:
                c[CONF_MODE] = args[3]
        n = await number.new_number(
            c, min_value=args[0], max_value=args[1], step=args[2]
        )
        await cg.register_parented(n, parent)
        cg.add(getattr(parent, setter + "_number")(n))

    await for_each_conf(config, TYPES, new_number)
