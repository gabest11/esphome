#pragma once

#include "esphome/components/number/number.h"
#include "../qn8027.h"

namespace esphome {
namespace qn8027 {

class FrequencyDeviationNumber : public number::Number, public Parented<QN8027Component> {
 public:
  FrequencyDeviationNumber() = default;

 protected:
  void control(float value) override;
};

}  // namespace qn8027
}  // namespace esphome