#include "rc_switch_but_better_protocol.h"
#include "esphome/core/application.h"
#include "esphome/core/log.h"
#include <cinttypes>

namespace esphome {
namespace remote_base {

static const char *const TAG = "remote.rc_switch_but_better";

// RcSwitchButBetterProtocol

optional<RcSwitchButBetterData> RcSwitchButBetterProtocol::decode(RemoteReceiveData src) {
  this->setup();

  ESP_LOGV(TAG, "decode %d %d %d", (int) src.size(), (int) src[0], (int) src[1]);

  RcSwitchButBetterData data;
  this->code_.resize(std::max((this->nbits_ + 7) >> 3, 8));

  uint32_t samples = (this->nbits_ + 1) * 2;                                    // sync + nbits
  uint32_t search_end = src.size() > samples ? src.size() - samples + 1 : 0ul;  // last possible sync + 1
  uint32_t search_limit = std::min(search_end, samples * 3 / 2);                // limit search

  while (src.get_index() < search_limit) {
    if (this->receive_item_(src, this->sync_high_, this->sync_low_)) {
      if (this->receive_code_(src)) {
        ESP_LOGD(TAG, "receive @%" PRIu32 " %" PRIx64 " (%d)", src.get_index(), *(uint64_t *) &this->code_[0],
                 this->nbits_);
        // found something, extend search till the end
        search_limit = search_end;
        // transform may also return false if it needs more packets to complete data
        if (this->to_data(data)) {
          ESP_LOGD(TAG, "%s", data.c_str());
          return data;
        }
      }
    } else {
      src.advance(1);
    }
  }

  // try again without sync

  src.reset();

  samples = this->nbits_ * 2;                                      // nbits
  search_end = src.size() > samples ? src.size() - samples : 0ul;  // last possible sync + 1
  search_limit = std::min(search_end, samples * 3 / 2);            // limit search

  while (src.get_index() < search_limit) {
    if (this->receive_code_(src)) {
      ESP_LOGD(TAG, "receive @%" PRIu32 " %" PRIx64 " (%d)", src.get_index(), *(uint64_t *) &this->code_[0],
               this->nbits_);
      // found something, extend search till the end
      search_limit = search_end;
      // transform may also return false if it needs more packets to complete data
      if (this->to_data(data)) {
        ESP_LOGD(TAG, "%s", data.c_str());
        return data;
      }
    } else {
      src.advance(1);
    }
  }

  return {};
}

void RcSwitchButBetterProtocol::encode(RemoteTransmitData *dst, const RcSwitchButBetterData &data) {
  this->setup();
  this->code_.resize(std::max((this->nbits_ + 7) >> 3, 8), 0);

  if (this->to_code(data)) {
    ESP_LOGD(TAG, "encode %s", data.c_str());
    dst->set_carrier_frequency(38000);  // TODO: channel?
    for (int i = 0; i < this->repeat_; i++) {
      this->transmit_code_(dst);
    }
  }
}

void RcSwitchButBetterProtocol::dump(const RcSwitchButBetterData &data) { ESP_LOGI(TAG, "%s", data.c_str()); }

bool RcSwitchButBetterProtocol::receive_item_(RemoteReceiveData &src, uint32_t high, uint32_t low) const {
  if (!this->is_inverted_()) {
    ESP_LOGV(TAG, "receive_item %d %d %d %d", (int) src.peek(0), (int) src.peek_mark(high, 0), (int) src.peek(1), (int) src.peek_space(low, 1));
    if (!(this->is_ppm_() ? src.peek_mark_at_most(high, 0) : src.peek_mark(high, 0)))
      return false;
    if (!src.peek_space(low, 1))
      return false;
    src.advance(2);
  } else {
    if (src.get_index() == 0) {
      // assume space at the beginning
      if (!(this->is_ppm_() ? src.peek_mark_at_most(low, 0) : src.peek_mark(low, 0)))
        return false;
      src.advance(1);
    } else {
      if (!src.peek_space(high, 0))
        return false;
      if (!(this->is_ppm_() ? src.peek_mark_at_most(low, 1) : src.peek_mark(low, 1)))
        return false;
      src.advance(2);
    }
  }
  return true;
}

bool RcSwitchButBetterProtocol::receive_code_(RemoteReceiveData &src) {
  uint16_t nbits = 0;

  while (nbits < this->nbits_ && src.get_index() < src.size() - 1) {
    size_t pos = !this->is_reversed_() ? nbits : this->nbits_ - nbits - 1;
    uint8_t bit = 1 << (pos & 7);
    uint8_t &dst = this->code_[pos >> 3];

    if (this->receive_item_(src, this->zero_high_, this->zero_low_)) {
      dst &= ~bit;
    } else if (this->receive_item_(src, this->one_high_, this->one_low_)) {
      dst |= bit;
    } else if (0 < this->nbits_min_ && this->nbits_min_ <= nbits) {
      return true;
    } else {
      break;
    }

    ESP_LOGV(TAG, "receive_code_ %02X (%d %d)", dst, (int) pos, (int) nbits);

    if (++nbits == this->nbits_) {
      if (src.get_index() < src.size() - 1) {
        uint32_t index = src.get_index();
        if (this->receive_item_(src, this->zero_high_, this->zero_low_) ||
            this->receive_item_(src, this->one_high_, this->one_low_)) {
          ESP_LOGD(TAG, "ignore %" PRIx64 " (%d)", *(uint64_t *) &this->code_[0], (int) nbits);
          src.reset();
          src.advance(index);
          break;
        }
      }
      return true;
    }
  }

  return false;
}

void RcSwitchButBetterProtocol::transmit_item_(RemoteTransmitData *dst, uint32_t high, uint32_t low) const {
  if (!this->is_inverted_()) {
    dst->mark(high);
    dst->space(low);
  } else {
    dst->space(high);
    dst->mark(low);
  }
}

void RcSwitchButBetterProtocol::transmit_code_(RemoteTransmitData *dst) const {
  this->transmit_item_(dst, this->sync_high_, this->sync_low_);
  for (uint16_t j = 0; j < this->nbits_; j++) {
    uint16_t i = this->is_reversed_() ? j : this->nbits_ - j - 1;
    if (this->code_[i >> 3] & (1 << (i & 7))) {
      this->transmit_item_(dst, this->one_high_, this->one_low_);
    } else {
      this->transmit_item_(dst, this->zero_high_, this->zero_low_);
    }
  }
}

//

uint32_t RcSwitchButBetterProtocol::get_bits_(uint16_t pos, uint8_t nbits) const {
  if (pos + nbits > this->code_.size() * 8) {
    ESP_LOGE(TAG, "get_bits_ out of range");
    return 0;
  }

  // if (zero_pos_at_msb) {
  pos = this->nbits_ - (pos + nbits);
  // }

  uint32_t c = 0;

  if ((pos & 7) == 0) {
    for (uint8_t i = 0; i < nbits; i += 8, pos += 8) {
      c |= (uint32_t) this->code_[pos >> 3] << i;
    }
    if ((nbits & 7) != 0) {
      c &= 0xffffffff >> (32 - nbits);
    }
  } else {
    for (uint8_t i = 0; i < nbits; i++, pos++) {
      if (this->code_[pos >> 3] & (1 << (pos & 7)))
        c |= (uint32_t) 1 << i;
    }
  }

  return c;
}

void RcSwitchButBetterProtocol::set_bits_(uint16_t pos, uint8_t nbits, uint32_t c) {
  // TODO
}

bool RcSwitchButBetterProtocol::to_data(RcSwitchButBetterData &data) const {
  data.resize(this->nbits_);
  for (size_t i = 0; i < data.size(); i++) {
    data[i] = (this->code_[i >> 3] & (1 << (i & 7))) ? '1' : '0';
  }
  return true;
}

bool RcSwitchButBetterProtocol::to_code(const RcSwitchButBetterData &data) {
  for (size_t i = 0; i < data.size(); i++) {
    if (data[i] == '1') {
      this->code_[i >> 3] |= 1 << (i & 7);
    }
  }
  return true;
}

}  // namespace remote_base
}  // namespace esphome
