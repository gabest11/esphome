#include "acomp_preset_select.h"

namespace esphome {
namespace si4713 {

void AcompPresetSelect::control(const std::string &value) {
  this->publish_state(value);
  if (auto index = this->active_index()) {
    this->parent_->set_acomp_preset((AcompPreset) *index);
  }
}

}  // namespace si4713
}  // namespace esphome