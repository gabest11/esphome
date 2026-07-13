#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "esphome/components/spi/spi.h"
#include "esphome/components/remote_base/rc_switch_protocol.h"
#include "esphome/components/voltage_sampler/voltage_sampler.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/number/number.h"
#include "esphome/components/switch/switch.h"
#include "esphome/components/select/select.h"
#include "esphome/components/text/text.h"
#include <string>
#include "cc1101defs.h"
#include "cc1101sub.h"

namespace esphome {
namespace cc1101 {

// Forward declarations
class CC1101SignalProcessor;

class CC1101Component : public PollingComponent,
                        public spi::SPIDevice<spi::BIT_ORDER_MSB_FIRST, spi::CLOCK_POLARITY_LOW,
                                              spi::CLOCK_PHASE_LEADING, spi::DATA_RATE_1MHZ> {
 public:
  CC1101Component();

  void set_config_gdo0_pin(InternalGPIOPin *pin) { gdo0_ = pin; }
  void set_config_gdo0_adc_pin(voltage_sampler::VoltageSampler *pin) { gdo0_adc_ = pin; }

  void setup() override;
  void dump_config() override;
  void update() override;
  void loop() override;

  void begin_tx();
  void end_tx();
  
  // Data transmission methods
  void send_data(const uint8_t *data, size_t length);
  void send_data(const char *data);
  void send_data(const uint8_t *data, size_t length, uint32_t timeout_ms);
  void send_data(const char *data, uint32_t timeout_ms);
  
  // FSK transmission with automatic mode switching (async RX -> packet TX -> async RX)
  void send_data_fsk(const uint8_t *data, size_t length, uint8_t repeat_count = 10);
  
  // Data reception methods
  bool receive_data(uint8_t *data, size_t max_length, size_t *received_length);
  bool check_receive_flag();
  bool check_crc();
  bool check_rx_fifo();
  void flush_rx_fifo();
  
  // Advanced configuration methods
  void set_sync_word(uint16_t sync_word);
  void set_packet_format(bool variable_length, bool data_whitening, bool crc_enabled);
  void set_crc_enabled(bool enabled);
  void set_data_whitening(bool enabled);
  void set_manchester_encoding(bool enabled);
  void set_packet_length(uint8_t length);
  void set_packet_length_variable();
  
  // State management and mode tracking
  uint8_t get_mode();
  bool is_idle();
  bool is_rx();
  bool is_tx();
  bool is_calibrating();
  void wait_for_idle();
  void wait_for_rx();
  void wait_for_tx();
  
  // Power management methods
  void sleep();
  void idle();
  void reset();
  void wake_up();
  bool is_sleeping();
  
  // Enhanced frequency calibration for different bands
  void calibrate_frequency();
  void calibrate_433mhz();
  void calibrate_868mhz();
  void calibrate_915mhz();
  void set_frequency_band(uint32_t frequency);
  bool is_frequency_valid(uint32_t frequency);
  
  // Basic signal processing capabilities (simplified)
  void enable_signal_processing(bool enable);
  void start_learning();
  void stop_learning();
  void save_learned_signal(const std::string& name);
  void transmit_learned_signal(const std::string& name);
  void start_scanning();
  void stop_scanning();
  
  // Signal processor access
  CC1101SignalProcessor* get_signal_processor() { return signal_processor_; }
  void process_raw_pulse_data(const std::vector<int32_t>& pulse_data, float rssi_db);
  
  // Frequency-specific PA table optimization
  void optimize_pa_table_433mhz();
  void optimize_pa_table_868mhz();
  void optimize_pa_table_915mhz();
  void set_pa_table_433mhz();
  void set_pa_table_868mhz();
  void set_pa_table_915mhz();
  void set_custom_pa_table(const uint8_t *pa_table, size_t length);

  CC1101_SUB_NUMBER(output_power, float)
  CC1101_SUB_SELECT(rx_attenuation, RxAttenuation)
  CC1101_SUB_SWITCH(dc_blocking_filter)
  // TODO: CC1101_SUB_SWITCH(manchester)
  CC1101_SUB_NUMBER(tuner_frequency, float)
  CC1101_SUB_NUMBER(tuner_if_frequency, float)
  CC1101_SUB_NUMBER(tuner_bandwidth, float)
  CC1101_SUB_NUMBER(tuner_channel, uint8_t)
  CC1101_SUB_NUMBER(tuner_channel_spacing, float)
  CC1101_SUB_NUMBER(tuner_fsk_deviation, float)
  CC1101_SUB_NUMBER(tuner_msk_deviation, uint8_t)
  CC1101_SUB_NUMBER(tuner_symbol_rate, float)
  CC1101_SUB_SELECT(tuner_sync_mode, SyncMode)
  CC1101_SUB_SWITCH(tuner_carrier_sense_above_threshold)
  CC1101_SUB_SELECT(tuner_modulation, Modulation)
  CC1101_SUB_SELECT(agc_magn_target, MagnTarget)
  CC1101_SUB_SELECT(agc_max_lna_gain, MaxLnaGain)
  CC1101_SUB_SELECT(agc_max_dvga_gain, MaxDvgaGain)
  CC1101_SUB_NUMBER(agc_carrier_sense_abs_thr, int8_t)
  CC1101_SUB_SELECT(agc_carrier_sense_rel_thr, CarrierSenseRelThr)
  CC1101_SUB_SWITCH(agc_lna_priority)
  CC1101_SUB_SELECT(agc_filter_length_fsk_msk, FilterLengthFskMsk)
  CC1101_SUB_SELECT(agc_filter_length_ask_ook, FilterLengthAskOok)
  CC1101_SUB_SELECT(agc_freeze, Freeze)
  CC1101_SUB_SELECT(agc_wait_time, WaitTime)
  CC1101_SUB_SELECT(agc_hyst_level, HystLevel)
  CC1101_SUB_TEXT_SENSOR(chip_id)
  // TODO: PARTNUM
  // TODO: VERSION
  CC1101_SUB_SENSOR(rssi)
  CC1101_SUB_SENSOR(lqi)
  // TODO: CRC OK
  CC1101_SUB_SENSOR(temperature)

 protected:
  InternalGPIOPin *gdo0_;
  voltage_sampler::VoltageSampler *gdo0_adc_;
  std::string chip_id_;
  bool reset_;
  float output_power_requested_;
  float output_power_effective_;
  uint8_t pa_table_[8];
  union {
    struct CC1101State state_;
    uint8_t regs_[sizeof(struct CC1101State) / sizeof(uint8_t)];
  };
  
  // Signal processing (simplified)
  bool signal_processing_enabled_;
  bool learning_mode_;
  bool scanning_mode_;
  CC1101SignalProcessor *signal_processor_;  // Advanced signal processing

  void strobe_(Command cmd);
  void write_(Register reg);
  void write_(Register reg, uint8_t value);
  void write_(Register reg, uint8_t *buffer, size_t length);
  bool read_(Register reg);
  bool read_(Register reg, uint8_t *buffer, size_t length);
  // bool send_data_(const uint8_t* data, size_t length);
  void send_(Command cmd);
  bool wait_(Command cmd);

  template<class S, class T> void publish_(S *s, T state);
  // template specialization here in the header is not supported by the compiler
  void publish_switch_(switch_::Switch *s, bool state);
  void publish_select_(select::Select *s, size_t index);
  
  // Signal processing (simplified - no interrupt handler for now)
};

template<typename... Ts> class BeginTxAction : public Action<Ts...>, public Parented<CC1101Component> {
 public:
  void play(Ts... x) override { this->parent_->begin_tx(); }
};

template<typename... Ts> class EndTxAction : public Action<Ts...>, public Parented<CC1101Component> {
 public:
  void play(Ts... x) override { this->parent_->end_tx(); }
};

template<typename... Ts>
class CC1101RawAction : public remote_base::RCSwitchRawAction<Ts...>, public Parented<CC1101Component> {
 protected:
  void play(Ts... x) override {
    this->parent_->begin_tx();
    remote_base::RCSwitchRawAction<Ts...>::play(x...);
    this->parent_->end_tx();
  }

 public:
};

}  // namespace cc1101
}  // namespace esphome
