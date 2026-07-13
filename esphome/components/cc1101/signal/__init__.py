import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, binary_sensor, text_sensor, switch, button
from esphome.const import (
    CONF_ID,
    CONF_NAME,
    CONF_ICON,
    CONF_DEVICE_CLASS,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ACCURACY_DECIMALS,
    CONF_ENTITY_CATEGORY,
    ENTITY_CATEGORY_DIAGNOSTIC,
    ENTITY_CATEGORY_CONFIG,
    ICON_SIGNAL,
    ICON_RADIO,
    ICON_MEMORY,
    ICON_PLAY,
    ICON_STOP,
    ICON_RECORD,
    UNIT_DB,
    UNIT_PERCENT,
    UNIT_COUNT,
)

from .. import cc1101_ns, CC1101Component

CONF_SIGNAL_PROCESSING = "signal_processing"
CONF_SIGNAL_MODE = "signal_mode"
CONF_RSSI_THRESHOLD = "rssi_threshold"
CONF_MIN_PULSE_LENGTH = "min_pulse_length"
CONF_MIN_SIGNAL_LENGTH = "min_signal_length"
CONF_PROTOCOL_TYPE = "protocol_type"
CONF_LEARNING_MODE = "learning_mode"
CONF_SCANNING_MODE = "scanning_mode"
CONF_SIGNAL_COUNT = "signal_count"
CONF_DECODED_COUNT = "decoded_count"
CONF_LEARNED_COUNT = "learned_count"
CONF_SIGNAL_RATIO = "signal_ratio"
CONF_LAST_SIGNAL = "last_signal"
CONF_LAST_PROTOCOL = "last_protocol"
CONF_LAST_RSSI = "last_rssi"
CONF_LEARNED_SIGNALS = "learned_signals"

# Signal modes
SIGNAL_MODE_SCAN = "scan"
SIGNAL_MODE_LEARN = "learn"
SIGNAL_MODE_TRANSMIT = "transmit"
SIGNAL_MODE_DECODE = "decode"

# Protocol types
PROTOCOL_TYPE_OOK = "ook"
PROTOCOL_TYPE_FSK = "fsk"
PROTOCOL_TYPE_ASK = "ask"
PROTOCOL_TYPE_MSK = "msk"

SignalMode = cc1101_ns.enum("SignalMode")
SIGNAL_MODES = {
    SIGNAL_MODE_SCAN: SignalMode.SCAN,
    SIGNAL_MODE_LEARN: SignalMode.LEARN,
    SIGNAL_MODE_TRANSMIT: SignalMode.TRANSMIT,
    SIGNAL_MODE_DECODE: SignalMode.DECODE,
}

ProtocolType = cc1101_ns.enum("ProtocolType")
PROTOCOL_TYPES = {
    PROTOCOL_TYPE_OOK: ProtocolType.OOK,
    PROTOCOL_TYPE_FSK: ProtocolType.FSK,
    PROTOCOL_TYPE_ASK: ProtocolType.ASK,
    PROTOCOL_TYPE_MSK: ProtocolType.MSK,
}

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(CC1101Component),
    cv.Optional(CONF_SIGNAL_PROCESSING, default=True): cv.boolean,
    cv.Optional(CONF_SIGNAL_MODE, default=SIGNAL_MODE_SCAN): cv.enum(SIGNAL_MODES),
    cv.Optional(CONF_RSSI_THRESHOLD, default=-82): cv.int_range(min=-120, max=0),
    cv.Optional(CONF_MIN_PULSE_LENGTH, default=50): cv.int_range(min=1, max=10000),
    cv.Optional(CONF_MIN_SIGNAL_LENGTH, default=40000): cv.int_range(min=1000, max=1000000),
    cv.Optional(CONF_PROTOCOL_TYPE, default=PROTOCOL_TYPE_OOK): cv.enum(PROTOCOL_TYPES),
    
    # Sensors
    cv.Optional(CONF_SIGNAL_COUNT): sensor.sensor_schema(
        unit_of_measurement=UNIT_COUNT,
        icon=ICON_SIGNAL,
        accuracy_decimals=0,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_DECODED_COUNT): sensor.sensor_schema(
        unit_of_measurement=UNIT_COUNT,
        icon=ICON_RADIO,
        accuracy_decimals=0,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_LEARNED_COUNT): sensor.sensor_schema(
        unit_of_measurement=UNIT_COUNT,
        icon=ICON_MEMORY,
        accuracy_decimals=0,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_SIGNAL_RATIO): sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        icon=ICON_SIGNAL,
        accuracy_decimals=1,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_LAST_RSSI): sensor.sensor_schema(
        unit_of_measurement=UNIT_DB,
        icon=ICON_SIGNAL,
        accuracy_decimals=1,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    
    # Text sensors
    cv.Optional(CONF_LAST_SIGNAL): text_sensor.text_sensor_schema(
        icon=ICON_RADIO,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_LAST_PROTOCOL): text_sensor.text_sensor_schema(
        icon=ICON_RADIO,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    
    # Switches
    cv.Optional(CONF_LEARNING_MODE): switch.switch_schema(
        icon=ICON_RECORD,
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    cv.Optional(CONF_SCANNING_MODE): switch.switch_schema(
        icon=ICON_SIGNAL,
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
})

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    
    # Signal processing configuration
    if CONF_SIGNAL_PROCESSING in config:
        cg.add(var.enable_signal_processing(config[CONF_SIGNAL_PROCESSING]))
    
    if CONF_SIGNAL_MODE in config:
        cg.add(var.set_signal_mode(SIGNAL_MODES[config[CONF_SIGNAL_MODE]]))
    
    if CONF_RSSI_THRESHOLD in config:
        cg.add(var.set_rssi_threshold(config[CONF_RSSI_THRESHOLD]))
    
    # Sensors
    if CONF_SIGNAL_COUNT in config:
        sens = yield sensor.new_sensor(config[CONF_SIGNAL_COUNT])
        cg.add(var.set_signal_count_sensor(sens))
    
    if CONF_DECODED_COUNT in config:
        sens = yield sensor.new_sensor(config[CONF_DECODED_COUNT])
        cg.add(var.set_decoded_count_sensor(sens))
    
    if CONF_LEARNED_COUNT in config:
        sens = yield sensor.new_sensor(config[CONF_LEARNED_COUNT])
        cg.add(var.set_learned_count_sensor(sens))
    
    if CONF_SIGNAL_RATIO in config:
        sens = yield sensor.new_sensor(config[CONF_SIGNAL_RATIO])
        cg.add(var.set_signal_ratio_sensor(sens))
    
    if CONF_LAST_RSSI in config:
        sens = yield sensor.new_sensor(config[CONF_LAST_RSSI])
        cg.add(var.set_last_rssi_sensor(sens))
    
    # Text sensors
    if CONF_LAST_SIGNAL in config:
        sens = yield text_sensor.new_text_sensor(config[CONF_LAST_SIGNAL])
        cg.add(var.set_last_signal_sensor(sens))
    
    if CONF_LAST_PROTOCOL in config:
        sens = yield text_sensor.new_text_sensor(config[CONF_LAST_PROTOCOL])
        cg.add(var.set_last_protocol_sensor(sens))
    
    # Switches
    if CONF_LEARNING_MODE in config:
        sw = yield switch.new_switch(config[CONF_LEARNING_MODE])
        cg.add(sw.setup_lambda([var](bool state) {
            if (state) {
                var->start_learning();
            } else {
                var->stop_learning();
            }
        }))
    
    if CONF_SCANNING_MODE in config:
        sw = yield switch.new_switch(config[CONF_SCANNING_MODE])
        cg.add(sw.setup_lambda([var](bool state) {
            if (state) {
                var->start_scanning();
            } else {
                var->stop_scanning();
            }
        }))

