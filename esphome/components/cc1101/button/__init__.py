import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button
from esphome.const import CONF_ID, CONF_ICON, ICON_PLAY, ICON_STOP, ICON_RECORD, ICON_MEMORY

from .. import cc1101_ns, CC1101Component

CONF_SAVE_SIGNAL = "save_signal"
CONF_TRANSMIT_SIGNAL = "transmit_signal"
CONF_START_LEARNING = "start_learning"
CONF_STOP_LEARNING = "stop_learning"
CONF_START_SCANNING = "start_scanning"
CONF_STOP_SCANNING = "stop_scanning"
CONF_CLEAR_LEARNED = "clear_learned"
CONF_SCAN_FREQUENCY = "scan_frequency"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(CC1101Component),
    cv.Optional(CONF_SAVE_SIGNAL): button.button_schema(
        icon=ICON_MEMORY,
    ),
    cv.Optional(CONF_TRANSMIT_SIGNAL): button.button_schema(
        icon=ICON_PLAY,
    ),
    cv.Optional(CONF_START_LEARNING): button.button_schema(
        icon=ICON_RECORD,
    ),
    cv.Optional(CONF_STOP_LEARNING): button.button_schema(
        icon=ICON_STOP,
    ),
    cv.Optional(CONF_START_SCANNING): button.button_schema(
        icon=ICON_PLAY,
    ),
    cv.Optional(CONF_STOP_SCANNING): button.button_schema(
        icon=ICON_STOP,
    ),
    cv.Optional(CONF_CLEAR_LEARNED): button.button_schema(
        icon=ICON_MEMORY,
    ),
    cv.Optional(CONF_SCAN_FREQUENCY): button.button_schema(
        icon=ICON_PLAY,
    ),
})

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    
    # Signal action buttons
    if CONF_SAVE_SIGNAL in config:
        btn = yield button.new_button(config[CONF_SAVE_SIGNAL])
        cg.add(btn.setup_lambda([var]() {
            var->save_learned_signal("signal_" + String(millis()));
        }))
    
    if CONF_TRANSMIT_SIGNAL in config:
        btn = yield button.new_button(config[CONF_TRANSMIT_SIGNAL])
        cg.add(btn.setup_lambda([var]() {
            var->transmit_learned_signal("last_signal");
        }))
    
    if CONF_START_LEARNING in config:
        btn = yield button.new_button(config[CONF_START_LEARNING])
        cg.add(btn.setup_lambda([var]() {
            var->start_learning();
        }))
    
    if CONF_STOP_LEARNING in config:
        btn = yield button.new_button(config[CONF_STOP_LEARNING])
        cg.add(btn.setup_lambda([var]() {
            var->stop_learning();
        }))
    
    if CONF_START_SCANNING in config:
        btn = yield button.new_button(config[CONF_START_SCANNING])
        cg.add(btn.setup_lambda([var]() {
            var->start_scanning();
        }))
    
    if CONF_STOP_SCANNING in config:
        btn = yield button.new_button(config[CONF_STOP_SCANNING])
        cg.add(btn.setup_lambda([var]() {
            var->stop_scanning();
        }))
    
    if CONF_CLEAR_LEARNED in config:
        btn = yield button.new_button(config[CONF_CLEAR_LEARNED])
        cg.add(btn.setup_lambda([var]() {
            // Clear learned signals - would need implementation
            ESP_LOGI("cc1101", "Clearing learned signals");
        }))
    
    if CONF_SCAN_FREQUENCY in config:
        btn = yield button.new_button(config[CONF_SCAN_FREQUENCY])
        cg.add(btn.setup_lambda([var]() {
            var->scan_frequency_range(433.0, 435.0, 0.1);
        }))










