from esphome import automation, pins
from esphome.automation import maybe_simple_id
import esphome.codegen as cg
from esphome.components import (
    binary_sensor,
    remote_base,
    sensor,
    spi,
    text_sensor,
    voltage_sampler,
)
import esphome.config_validation as cv
from esphome.const import (
    CONF_CHANNEL,
    CONF_CODE,
    CONF_FREQUENCY,
    CONF_ID,
    CONF_PROTOCOL,
    CONF_SENSOR,
    CONF_TEMPERATURE,
    CONF_WAIT_TIME,
    # DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
    ENTITY_CATEGORY_DIAGNOSTIC,
    ICON_CHIP,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_DECIBEL_MILLIWATT,
    UNIT_EMPTY,
)

CODEOWNERS = ["@gabest11"]
DEPENDENCIES = ["spi"]
AUTO_LOAD = [
    "remote_base",
    "voltage_sampler",
    "sensor",
    "binary_sensor",
    "text_sensor",
    "number",
    "switch",
    "select",
    "text",
]
MULTI_CONF = True
UNIT_MEGA_HERTZ = "MHz"
UNIT_KILO_HERTZ = "kHz"
UNIT_MILLI_VOLT = "mV"
UNIT_MICRO_AMPERE = "mA"
UNIT_DECIBEL_MICRO_VOLT = "dBuV"

ns = cg.esphome_ns.namespace("cc1101")
CC1101Component = ns.class_("CC1101Component", cg.PollingComponent, spi.SPIDevice)

CONF_CC1101_ID = "cc1101_id"

CONF_GDO0_PIN = "gdo0_pin"
CONF_GDO0_ADC_ID = "gdo0_adc_id"
CONF_OUTPUT_POWER = "output_power"
CONF_RX_ATTENUATION = "rx_attenuation"
CONF_DC_BLOCKING_FILTER = "dc_blocking_filter"

# tuner
CONF_TUNER = "tuner"
# CONF_FREQUENCY = "frequency"
CONF_IF_FREQUENCY = "if_frequency"
CONF_BANDWIDTH = "bandwidth"
# CONF_CHANNEL = "channel"
CONF_CHANNEL_SPACING = "channel_spacing"
CONF_FSK_DEVIATION = "fsk_deviation"
CONF_MSK_DEVIATION = "msk_deviation"
CONF_SYMBOL_RATE = "symbol_rate"
CONF_SYNC_MODE = "sync_mode"
CONF_CARRIER_SENSE_ABOVE_THRESHOLD = "carrier_sense_above_threshold"
CONF_MODULATION = "modulation"

# agc
CONF_AGC = "agc"
CONF_MAGN_TARGET = "magn_target"
CONF_MAX_LNA_GAIN = "max_lna_gain"
CONF_MAX_DVGA_GAIN = "max_dvga_gain"
CONF_CARRIER_SENSE_ABS_THR = "carrier_sense_abs_thr"
CONF_CARRIER_SENSE_REL_THR = "carrier_sense_rel_thr"
CONF_LNA_PRIORITY = "lna_priority"
CONF_FILTER_LENGTH_FSK_MSK = "filter_length_fsk_msk"
CONF_FILTER_LENGTH_ASK_OOK = "filter_length_ask_ook"
CONF_FREEZE = "freeze"
CONF_HYST_LEVEL = "hyst_level"

# sensor
CONF_CHIP_ID = "chip_id"
CONF_RSSI = "rssi"
CONF_LQI = "lqi"
# CONF_TEMPERATURE = "temperature"

SyncMode = ns.enum("SyncMode", True)
SYNC_MODE = {
    "None": SyncMode.SYNC_MODE_NONE,
    "15/16": SyncMode.SYNC_MODE_15_16,
    "16/16": SyncMode.SYNC_MODE_16_16,
    "30/32": SyncMode.SYNC_MODE_30_32,
}

Modulation = ns.enum("Modulation", True)
MODULATION = {
    "2-FSK": Modulation.MODULATION_2_FSK,
    "GFSK": Modulation.MODULATION_GFSK,
    "UNUSED 2": Modulation.MODULATION_UNUSED_2,
    "ASK/OOK": Modulation.MODULATION_ASK_OOK,
    "4-FSK": Modulation.MODULATION_4_FSK,
    "UNUSED 5": Modulation.MODULATION_UNUSED_5,
    "UNUSED 6": Modulation.MODULATION_UNUSED_6,
    "MSK": Modulation.MODULATION_MSK,
}

RxAttenuation = ns.enum("RxAttenuation", True)
RX_ATTENUATION = {
    "0dB": RxAttenuation.RX_ATTENUATION_0DB,
    "6dB": RxAttenuation.RX_ATTENUATION_6DB,
    "12dB": RxAttenuation.RX_ATTENUATION_12DB,
    "18dB": RxAttenuation.RX_ATTENUATION_18DB,
}

MagnTarget = ns.enum("MagnTarget", True)
MAGN_TARGET = {
    "24dB": MagnTarget.MAGN_TARGET_24DB,
    "27dB": MagnTarget.MAGN_TARGET_27DB,
    "30dB": MagnTarget.MAGN_TARGET_30DB,
    "33dB": MagnTarget.MAGN_TARGET_33DB,
    "36dB": MagnTarget.MAGN_TARGET_36DB,
    "38dB": MagnTarget.MAGN_TARGET_38DB,
    "40dB": MagnTarget.MAGN_TARGET_40DB,
    "42dB": MagnTarget.MAGN_TARGET_42DB,
}

MaxLnaGain = ns.enum("MaxLnaGain", True)
MAX_LNA_GAIN = {
    "Default": MaxLnaGain.MAX_LNA_GAIN_DEFAULT,
    "2.6dB": MaxLnaGain.MAX_LNA_GAIN_MINUS_2P6DB,
    "6.1dB": MaxLnaGain.MAX_LNA_GAIN_MINUS_6P1DB,
    "7.4dB": MaxLnaGain.MAX_LNA_GAIN_MINUS_7P4DB,
    "9.2dB": MaxLnaGain.MAX_LNA_GAIN_MINUS_9P2DB,
    "11.5dB": MaxLnaGain.MAX_LNA_GAIN_MINUS_11P5DB,
    "14.6dB": MaxLnaGain.MAX_LNA_GAIN_MINUS_14P6DB,
    "17.1dB": MaxLnaGain.MAX_LNA_GAIN_MINUS_17P1DB,
}

MaxDvgaGain = ns.enum("MaxDvgaGain", True)
MAX_DVGA_GAIN = {
    "Default": MaxDvgaGain.MAX_DVGA_GAIN_DEFAULT,
    "-1": MaxDvgaGain.MAX_DVGA_GAIN_MINUS_1,
    "-2": MaxDvgaGain.MAX_DVGA_GAIN_MINUS_2,
    "-3": MaxDvgaGain.MAX_DVGA_GAIN_MINUS_3,
}

CarrierSenseRelThr = ns.enum("CarrierSenseRelThr", True)
CARRIER_SENSE_REL_THR = {
    "Default": CarrierSenseRelThr.CARRIER_SENSE_REL_THR_DEFAULT,
    "+6dB": CarrierSenseRelThr.CARRIER_SENSE_REL_THR_PLUS_6DB,
    "+10dB": CarrierSenseRelThr.CARRIER_SENSE_REL_THR_PLUS_10DB,
    "+14dB": CarrierSenseRelThr.CARRIER_SENSE_REL_THR_PLUS_14DB,
}

FilterLengthFskMsk = ns.enum("FilterLengthFskMsk", True)
FILTER_LENGTH_FSK_MSK = {
    "8": FilterLengthFskMsk.FILTER_LENGTH_8,
    "16": FilterLengthFskMsk.FILTER_LENGTH_16,
    "32": FilterLengthFskMsk.FILTER_LENGTH_32,
    "64": FilterLengthFskMsk.FILTER_LENGTH_64,
}

FilterLengthAskOok = ns.enum("FilterLengthAskOok", True)
FILTER_LENGTH_ASK_OOK = {
    "4dB": FilterLengthAskOok.FILTER_LENGTH_4DB,
    "8dB": FilterLengthAskOok.FILTER_LENGTH_8DB,
    "12dB": FilterLengthAskOok.FILTER_LENGTH_12DB,
    "16dB": FilterLengthAskOok.FILTER_LENGTH_16DB,
}

Freeze = ns.enum("Freeze", True)
FREEZE = {
    "Default": Freeze.AGC_FREEZE_DEFAULT,
    "On Sync": Freeze.AGC_FREEZE_ON_SYNC,
    "Analog Only": Freeze.AGC_FREEZE_ANALOG_ONLY,
    "Analog And Digital": Freeze.AGC_FREEZE_ANALOG_AND_DIGITAL,
}

WaitTime = ns.enum("WaitTime", True)
WAIT_TIME = {
    "8": WaitTime.WAIT_TIME_8_SAMPLES,
    "16": WaitTime.WAIT_TIME_16_SAMPLES,
    "24": WaitTime.WAIT_TIME_24_SAMPLES,
    "32": WaitTime.WAIT_TIME_32_SAMPLES,
}

HystLevel = ns.enum("HystLevel", True)
HYST_LEVEL = {
    "None": HystLevel.HYST_LEVEL_NONE,
    "Low": HystLevel.HYST_LEVEL_LOW,
    "Medium": HystLevel.HYST_LEVEL_MEDIUM,
    "High": HystLevel.HYST_LEVEL_HIGH,
}

TYPES = {
    None: {
        CONF_OUTPUT_POWER: [cv.float_range(-70, 11)],
        CONF_RX_ATTENUATION: [cv.enum(RX_ATTENUATION)],
        CONF_DC_BLOCKING_FILTER: [cv.boolean],
    },
    CONF_TUNER: {
        CONF_FREQUENCY: [cv.float_range(300000, 928000)],
        CONF_IF_FREQUENCY: [cv.float_range(25, 788)],
        CONF_BANDWIDTH: [cv.float_range(58, 812)],
        CONF_CHANNEL: [cv.uint8_t],
        CONF_CHANNEL_SPACING: [cv.float_range(25, 405)],
        CONF_FSK_DEVIATION: [cv.float_range(1.5, 381)],
        CONF_MSK_DEVIATION: [cv.int_range(1, 8)],
        CONF_SYMBOL_RATE: [cv.float_range(600, 500000)],
        CONF_SYNC_MODE: [cv.enum(SYNC_MODE)],
        CONF_CARRIER_SENSE_ABOVE_THRESHOLD: [cv.boolean],
        CONF_MODULATION: [cv.enum(MODULATION)],
    },
    CONF_AGC: {
        CONF_MAGN_TARGET: [cv.enum(MAGN_TARGET)],
        CONF_MAX_LNA_GAIN: [cv.enum(MAX_LNA_GAIN)],
        CONF_MAX_DVGA_GAIN: [cv.enum(MAX_DVGA_GAIN)],
        CONF_CARRIER_SENSE_ABS_THR: [cv.int_range(-8, 7)],
        CONF_CARRIER_SENSE_REL_THR: [cv.enum(CARRIER_SENSE_REL_THR)],
        CONF_LNA_PRIORITY: [cv.boolean],
        CONF_FILTER_LENGTH_FSK_MSK: [cv.enum(FILTER_LENGTH_FSK_MSK)],
        CONF_FILTER_LENGTH_ASK_OOK: [cv.enum(FILTER_LENGTH_ASK_OOK)],
        CONF_FREEZE: [cv.enum(FREEZE)],
        CONF_WAIT_TIME: [cv.enum(WAIT_TIME)],
        CONF_HYST_LEVEL: [cv.enum(HYST_LEVEL)],
    },
    CONF_SENSOR: {
        CONF_CHIP_ID: [
            text_sensor.text_sensor_schema(
                # unit_of_measurement=UNIT_,
                # accuracy_decimals=3,
                # device_class=DEVICE_CLASS_,
                # state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
                icon=ICON_CHIP,
            ),
            "text_sensor",
        ],
        CONF_RSSI: [
            sensor.sensor_schema(
                unit_of_measurement=UNIT_DECIBEL_MILLIWATT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
                # icon=ICON_CHIP,
            ),
            "sensor",
        ],
        CONF_LQI: [
            sensor.sensor_schema(
                unit_of_measurement=UNIT_EMPTY,
                accuracy_decimals=0,
                # device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
                # icon=ICON_CHIP,
            ),
            "sensor",
        ],
        CONF_TEMPERATURE: [
            sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
                # icon=ICON_CHIP,
            ),
            "sensor",
        ],
    },
}

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(CC1101Component),
            cv.Optional(CONF_GDO0_PIN): cv.All(pins.internal_gpio_output_pin_schema),
            cv.Optional(CONF_GDO0_ADC_ID): cv.use_id(voltage_sampler.VoltageSampler),
        }
    )
    .extend(
        {cv.Optional(k): v[0] for k, v in TYPES[None].items()},
        {
            cv.Optional(CONF_TUNER): cv.Schema(
                {cv.Optional(k): v[0] for k, v in TYPES[CONF_TUNER].items()}
            ),
            cv.Optional(CONF_AGC): cv.Schema(
                {cv.Optional(k): v[0] for k, v in TYPES[CONF_AGC].items()}
            ),
            cv.Optional(CONF_SENSOR): cv.Schema(
                {cv.Optional(k): v[0] for k, v in TYPES[CONF_SENSOR].items()}
            ),
        },
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(spi.spi_device_schema(cs_pin_required=True))
)

CC1101_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_CC1101_ID): cv.use_id(CC1101Component),
    }
)


async def for_each_conf(config, types, callback):
    for section in types:
        if section is not None and section not in config:
            continue
        c = config[section] if section is not None else config
        for type, args in types[section].items():
            if type not in c:
                continue
            setter = "set_"
            if section is not None and section != CONF_SENSOR:
                setter += section + "_"
            setter += type
            # print(setter + "(" + repr(c[type]) + ")")
            await callback(c[type], args[1:], setter)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await spi.register_spi_device(var, config)
    if CONF_GDO0_PIN in config:
        gdo0_pin = await cg.gpio_pin_expression(config[CONF_GDO0_PIN])
        cg.add(var.set_config_gdo0_pin(gdo0_pin))
    if CONF_GDO0_ADC_ID in config:
        gdo0_adc_id = await cg.get_variable(config[CONF_GDO0_ADC_ID])
        cg.add(var.set_config_gdo0_adc_pin(gdo0_adc_id))

    async def set_var(c, args, setter):
        if len(args) > 0:
            s = None
            if args[0] == "sensor":
                s = await sensor.new_sensor(c)
            elif args[0] == "binary_sensor":
                s = await binary_sensor.new_binary_sensor(c)
            elif args[0] == "text_sensor":
                s = await text_sensor.new_text_sensor(c)
            if s is not None:
                cg.add(getattr(var, setter + "_" + args[0])(s))
        else:
            cg.add(getattr(var, setter)(c))

    await for_each_conf(config, TYPES, set_var)


BeginTxAction = ns.class_("BeginTxAction", automation.Action)
EndTxAction = ns.class_("EndTxAction", automation.Action)

CC1101_ACTION_SCHEMA = maybe_simple_id(
    {
        cv.GenerateID(CONF_ID): cv.use_id(CC1101Component),
    }
)


@automation.register_action("cc1101.begin_tx", BeginTxAction, CC1101_ACTION_SCHEMA)
@automation.register_action("cc1101.end_tx", EndTxAction, CC1101_ACTION_SCHEMA)
async def cc1101_action_to_code(config, action_id, template_arg, args):
    var = cg.new_Pvariable(action_id, template_arg)
    await cg.register_parented(var, config[CONF_ID])
    return var


CC1101RawAction = ns.class_("CC1101RawAction", remote_base.RCSwitchRawAction)

CC1101_TRANSMIT_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_CC1101_ID): cv.use_id(CC1101Component),
        }
    )
    .extend(remote_base.REMOTE_TRANSMITTABLE_SCHEMA)
    .extend(remote_base.RC_SWITCH_RAW_SCHEMA)
    .extend(remote_base.RC_SWITCH_TRANSMITTER)
)


@remote_base.register_action(
    "rc_switch_raw_cc1101", CC1101RawAction, CC1101_TRANSMIT_SCHEMA
)
async def rc_switch_raw_cc1101_action(var, config, args):
    proto = await cg.templatable(
        config[CONF_PROTOCOL],
        args,
        remote_base.RCSwitchBase,
        to_exp=remote_base.build_rc_switch_protocol,
    )
    cg.add(var.set_protocol(proto))
    cg.add(var.set_code(await cg.templatable(config[CONF_CODE], args, cg.std_string)))
    await cg.register_parented(var, config[CONF_CC1101_ID])
