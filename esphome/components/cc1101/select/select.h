#pragma once

#include "esphome/components/select/select.h"
#include "../cc1101.h"

namespace esphome {
namespace cc1101 {

template<class T, void (CC1101Component::*F)(T)>
class Select : public select::Select, public Parented<CC1101Component> {
 protected:
  void control(const std::string &value) override {
    this->publish_state(value);
    if (auto index = this->active_index()) {
      (this->parent_->*F)((T) *index);
    }
  }
};

using RxAttenuationSelect = Select<RxAttenuation, &CC1101Component::set_rx_attenuation>;
using TunerSyncModeSelect = Select<SyncMode, &CC1101Component::set_tuner_sync_mode>;
using TunerModulationSelect = Select<Modulation, &CC1101Component::set_tuner_modulation>;
using AgcMagnTargetSelect = Select<MagnTarget, &CC1101Component::set_agc_magn_target>;
using AgcMaxLnaGainSelect = Select<MaxLnaGain, &CC1101Component::set_agc_max_lna_gain>;
using AgcMaxDvgaGainSelect = Select<MaxDvgaGain, &CC1101Component::set_agc_max_dvga_gain>;
using AgcCarrierSenseRelThrSelect = Select<CarrierSenseRelThr, &CC1101Component::set_agc_carrier_sense_rel_thr>;
using AgcFilterLengthFskMskSelect = Select<FilterLengthFskMsk, &CC1101Component::set_agc_filter_length_fsk_msk>;
using AgcFilterLengthAskOokSelect = Select<FilterLengthAskOok, &CC1101Component::set_agc_filter_length_ask_ook>;
using AgcFreezeSelect = Select<Freeze, &CC1101Component::set_agc_freeze>;
using AgcWaitTimeSelect = Select<WaitTime, &CC1101Component::set_agc_wait_time>;
using AgcHystLevelSelect = Select<HystLevel, &CC1101Component::set_agc_hyst_level>;

}  // namespace cc1101
}  // namespace esphome
