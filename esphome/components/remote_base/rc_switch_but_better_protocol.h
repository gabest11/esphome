#pragma once

#include "remote_base.h"

namespace esphome {
namespace remote_base {

using RcSwitchButBetterData = std::string;

class RcSwitchButBetterProtocol : public RemoteProtocol<RcSwitchButBetterData> {
 public:
  RcSwitchButBetterProtocol() = default;
  RcSwitchButBetterProtocol(uint16_t sync_high, uint16_t sync_low, uint16_t zero_high, uint16_t zero_low,
                            uint16_t one_high, uint16_t one_low, uint8_t repeat, bool inverted, bool reversed,
                            const std::string &signal_type, uint16_t nbits, uint16_t nbits_min)
      : sync_high_(sync_high),
        sync_low_(sync_low),
        zero_high_(zero_high),
        zero_low_(zero_low),
        one_high_(one_high),
        one_low_(one_low),
        repeat_(repeat),
        flags_(0),
        nbits_(nbits),
        nbits_min_(nbits_min) {
    if (inverted)
      this->flags_ |= INVERTED;
    if (reversed)
      this->flags_ |= REVERSED;
    if (signal_type == "PPM")
      this->flags_ |= TYPE_PPM;
    else  // if(signal_type == "PWM")
      this->flags_ |= TYPE_PWM;
  }

  void set_nbits(uint16_t nbits, uint16_t nbits_min = 0) {
    this->nbits_ = nbits;
    this->nbits_min_ = nbits_min > 0 && nbits_min < nbits ? nbits_min : nbits;
  }

  void encode(RemoteTransmitData *dst, const RcSwitchButBetterData &data) override;
  optional<RcSwitchButBetterData> decode(RemoteReceiveData src) override;
  void dump(const RcSwitchButBetterData &data) override;

 protected:
  uint16_t sync_high_{};
  uint16_t sync_low_{};
  uint16_t zero_high_{};
  uint16_t zero_low_{};
  uint16_t one_high_{};
  uint16_t one_low_{};
  uint8_t repeat_{};
  uint8_t flags_{};
  uint16_t nbits_{};
  uint16_t nbits_min_{};

  enum RcSwitchButBetterFlag : uint8_t {
    TYPE_PWM = 0b00000000,
    TYPE_PPM = 0b00000001,
    // ... = 0b00000010,
    // ... = 0b00000011,
    TYPE_MASK = 0b00000011,
    INVERTED = 0b00000100,
    REVERSED = 0b00001000,
  };

  std::vector<uint8_t> code_;

  uint32_t get_bits_(uint16_t pos, uint8_t nbits) const;
  void set_bits_(uint16_t pos, uint8_t nbits, uint32_t c);

  bool is_pwm_() const { return (this->flags_ & TYPE_MASK) == TYPE_PWM; }
  bool is_ppm_() const { return (this->flags_ & TYPE_MASK) == TYPE_PPM; }
  bool is_inverted_() const { return (this->flags_ & INVERTED) != 0; }
  bool is_reversed_() const { return (this->flags_ & REVERSED) != 0; }

  bool receive_item_(RemoteReceiveData &src, uint32_t high, uint32_t low) const;
  uint16_t receive_code_(RemoteReceiveData &src);
  void transmit_item_(RemoteTransmitData *dst, uint32_t high, uint32_t low) const;
  void transmit_code_(RemoteTransmitData *dst) const;

  virtual void setup() {}
  virtual bool to_data(RcSwitchButBetterData &data, uint16_t nbits) const;
  virtual bool to_code(const RcSwitchButBetterData &data);
};

template<typename... Ts> class RcSwitchButBetterAction : public RemoteTransmitterActionBase<Ts...> {
 public:
  TEMPLATABLE_VALUE(RcSwitchButBetterProtocol, protocol);
  TEMPLATABLE_VALUE(std::string, code);

  void encode(RemoteTransmitData *dst, Ts... x) override {
    RcSwitchButBetterProtocol protocol = this->protocol_.value(x...);
    std::string code = this->code_.value(x...);
    protocol.set_nbits(code.size());
    RcSwitchButBetterData data = code;
    protocol.encode(dst, data);
  }
};

class RcSwitchButBetterBinarySensor : public RemoteReceiverBinarySensorBase, public RemoteReceiverDumperBase {
 public:
  void set_protocol(const RcSwitchButBetterProtocol &protocol) { this->protocol_ = protocol; }
  void set_code(const std::string &code) {
    this->code_ = code;
    this->protocol_.set_nbits(this->code_.size());
  }

 protected:
  RcSwitchButBetterProtocol protocol_;
  std::string code_;

  bool matches(RemoteReceiveData src) override {
    auto data = this->protocol_.decode(src);
    if (!data.has_value() || data->size() != this->code_.size()) {
      return false;
    }
    for (size_t i = 0; i < this->code_.size(); i++) {
      if ((this->code_[i] == '0' || this->code_[i] == '1') && this->code_[i] != (*data)[i]) {
        return false;
      }
    }
    return true;
  }

  bool dump(RemoteReceiveData src) override {
    auto data = this->protocol_.decode(src);
    if (!data.has_value()) {
      return false;
    }
    this->protocol_.dump(*data);
    return true;
  }
};

// using RcSwitchButBetterTrigger = RemoteReceiverTrigger<RcSwitchButBetterProtocol>;
// using RcSwitchButBetterDumper = RemoteReceiverDumper<RcSwitchButBetterProtocol>;

using RcSwitchButBetterDumper = RcSwitchButBetterBinarySensor;

}  // namespace remote_base
}  // namespace esphome
