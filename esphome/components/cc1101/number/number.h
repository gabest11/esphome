#pragma once

#include "esphome/components/number/number.h"
#include "../cc1101.h"
#include <cmath>

namespace esphome {
namespace cc1101 {

// maybe there is a way to specialize type dependent member pointers

template<void (CC1101Component::*F)(float)>
class NumberFloat : public number::Number, public Parented<CC1101Component> {
 protected:
  void control(float value) override {
    this->publish_state(value);
    (this->parent_->*F)(value);
  }
};

template<void (CC1101Component::*F)(uint8_t)>
class NumberUInt8 : public number::Number, public Parented<CC1101Component> {
 protected:
  void control(float value) override {
    this->publish_state(value);
    (this->parent_->*F)((uint8_t) std::lround(value));
  }
};

template<void (CC1101Component::*F)(int8_t)>
class NumberInt8 : public number::Number, public Parented<CC1101Component> {
 protected:
  void control(float value) override {
    this->publish_state(value);
    (this->parent_->*F)((int8_t) std::lround(value));
  }
};

using OutputPowerNumber = NumberFloat<&CC1101Component::set_output_power>;
using TunerFrequencyNumber = NumberFloat<&CC1101Component::set_tuner_frequency>;
using TunerIfFrequencyNumber = NumberFloat<&CC1101Component::set_tuner_if_frequency>;
using TunerBandwidthNumber = NumberFloat<&CC1101Component::set_tuner_bandwidth>;
using TunerChannelNumber = NumberUInt8<&CC1101Component::set_tuner_channel>;
using TunerChannelSpacingNumber = NumberFloat<&CC1101Component::set_tuner_channel_spacing>;
using TunerFskDeviationNumber = NumberFloat<&CC1101Component::set_tuner_fsk_deviation>;
using TunerMskDeviationNumber = NumberUInt8<&CC1101Component::set_tuner_msk_deviation>;
using TunerSymbolRateNumber = NumberFloat<&CC1101Component::set_tuner_symbol_rate>;
using AgcCarrierSenseAbsThrNumber = NumberInt8<&CC1101Component::set_agc_carrier_sense_abs_thr>;

}  // namespace cc1101
}  // namespace esphome
