#pragma once

#include "esphome/components/switch/switch.h"
#include "../cc1101.h"

namespace esphome {
namespace cc1101 {

template<void (CC1101Component::*F)(bool)> class Switch : public switch_::Switch, public Parented<CC1101Component> {
 protected:
  void write_state(bool value) override {
    this->publish_state(value);
    (this->parent_->*F)(value);
  }
};

using DcBlockingFilterSwitch = Switch<&CC1101Component::set_dc_blocking_filter>;
using CarrierSenseAboveThresholdSwitch = Switch<&CC1101Component::set_tuner_carrier_sense_above_threshold>;
using AgcLnaPrioritySwitch = Switch<&CC1101Component::set_agc_lna_priority>;

}  // namespace cc1101
}  // namespace esphome
