#pragma once

#include "esphome/components/text/text.h"
#include "../cc1101.h"

namespace esphome {
namespace cc1101 {

class DummyText : public text::Text, public Parented<CC1101Component> {
 protected:
  void control(const std::string &value) override {
    this->publish_state(value);
    // this->parent_->set_dummy_text(value);
  }
};

}  // namespace cc1101
}  // namespace esphome
