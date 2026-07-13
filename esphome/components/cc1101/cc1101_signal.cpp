#include "cc1101_signal.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
#include <algorithm>
#include <cmath>

namespace esphome {
namespace cc1101 {

static const char *const TAG = "cc1101.signal";

CC1101SignalProcessor::CC1101SignalProcessor(CC1101Component* cc1101) 
    : cc1101_(cc1101), current_mode_(SignalMode::SCAN), protocol_type_(ProtocolType::OOK),
      rssi_threshold_(-82), min_pulse_length_(50), min_signal_length_(40000),
      learning_mode_(false), decoding_enabled_(true), signal_count_(0), 
      decoded_count_(0), ignored_count_(0) {
  // Initialize pulse data
  memset(&current_pulse_data_, 0, sizeof(current_pulse_data_));
  current_pulse_data_.sample_rate = 1000000;
  
  // Add basic decoders
  add_decoder("generic_ook", [](const PulseData& data, DecodedSignal& result) -> bool {
    if (data.num_pulses < 16) return false;
    
    // Simple OOK decoder - look for patterns
    result.protocol = "OOK";
    result.model = "Generic";
    result.rssi = data.rssi_db;
    result.pulses = data.num_pulses;
    result.duration = data.signal_duration;
    
    // Convert pulses to binary representation
    std::string binary;
    for (unsigned int i = 0; i < data.num_pulses; i++) {
      if (data.pulse[i] > data.gap[i]) {
        binary += "1";
      } else {
        binary += "0";
      }
    }
    result.raw_data = binary;
    result.data = binary.substr(0, std::min(32, (int)binary.length()));
    
    return true;
  });
}

void CC1101SignalProcessor::set_signal_mode(SignalMode mode) {
  current_mode_ = mode;
  ESP_LOGD(TAG, "Signal mode changed to %d", (int)mode);
}

void CC1101SignalProcessor::set_protocol_type(ProtocolType type) {
  protocol_type_ = type;
  ESP_LOGD(TAG, "Protocol type changed to %d", (int)type);
}

void CC1101SignalProcessor::set_rssi_threshold(int threshold) {
  rssi_threshold_ = threshold;
  ESP_LOGD(TAG, "RSSI threshold set to %d", threshold);
}

void CC1101SignalProcessor::set_min_pulse_length(int length) {
  min_pulse_length_ = length;
  ESP_LOGD(TAG, "Min pulse length set to %d", length);
}

void CC1101SignalProcessor::set_min_signal_length(unsigned long length) {
  min_signal_length_ = length;
  ESP_LOGD(TAG, "Min signal length set to %lu", length);
}

void CC1101SignalProcessor::set_signal_received_callback(SignalReceivedCallback callback) {
  signal_callback_ = callback;
}

void CC1101SignalProcessor::set_pulse_received_callback(PulseReceivedCallback callback) {
  pulse_callback_ = callback;
}

void CC1101SignalProcessor::set_raw_data_callback(RawDataCallback callback) {
  raw_data_callback_ = callback;
}

void CC1101SignalProcessor::process_pulse_data(const PulseData& data) {
  if (data.num_pulses < 16) {
    ignored_count_++;
    return;
  }
  
  signal_count_++;
  current_pulse_data_ = data;
  
  // Store in buffer
  pulse_buffer_.push_back(data);
  if (pulse_buffer_.size() > 10) {
    pulse_buffer_.erase(pulse_buffer_.begin());
  }
  
  // Process based on current mode
  switch (current_mode_) {
    case SignalMode::SCAN:
      analyze_signal_strength();
      detect_protocol(data);
      break;
      
    case SignalMode::LEARN:
      if (learning_mode_) {
        ESP_LOGI(TAG, "Signal learned: %d pulses, %lu duration, RSSI: %.1f", 
                 data.num_pulses, data.signal_duration, data.rssi_db);
      }
      break;
      
    case SignalMode::DECODE:
      process_interrupt();
      break;
      
    case SignalMode::TRANSMIT:
      // Not applicable for reception
      break;
  }
  
  // Call pulse callback
  if (pulse_callback_) {
    pulse_callback_(data);
  }
}

void CC1101SignalProcessor::analyze_signal_strength() {
  if (current_pulse_data_.num_pulses == 0) return;
  
  float avg_rssi = 0.0f;
  int valid_pulses = 0;
  
  for (unsigned int i = 0; i < current_pulse_data_.num_pulses; i++) {
    if (current_pulse_data_.rssi[i] > rssi_threshold_) {
      avg_rssi += current_pulse_data_.rssi[i];
      valid_pulses++;
    }
  }
  
  if (valid_pulses > 0) {
    avg_rssi /= valid_pulses;
    ESP_LOGD(TAG, "Signal analysis: %d valid pulses, avg RSSI: %.1f", 
             valid_pulses, avg_rssi);
  }
}

void CC1101SignalProcessor::detect_protocol(const PulseData& data) {
  // Simple protocol detection based on pulse patterns
  if (data.num_pulses < 16) return;
  
  // Calculate average pulse and gap lengths
  float avg_pulse = 0.0f, avg_gap = 0.0f;
  for (unsigned int i = 0; i < data.num_pulses; i++) {
    avg_pulse += data.pulse[i];
    avg_gap += data.gap[i];
  }
  avg_pulse /= data.num_pulses;
  avg_gap /= data.num_pulses;
  
  // Detect patterns
  std::string detected_protocol = "Unknown";
  if (avg_pulse > avg_gap * 2) {
    detected_protocol = "OOK_Long";
  } else if (avg_gap > avg_pulse * 2) {
    detected_protocol = "OOK_Short";
  } else {
    detected_protocol = "OOK_Balanced";
  }
  
  ESP_LOGD(TAG, "Detected protocol: %s (avg pulse: %.1f, avg gap: %.1f)", 
           detected_protocol.c_str(), avg_pulse, avg_gap);
}

void CC1101SignalProcessor::start_learning() {
  learning_mode_ = true;
  ESP_LOGI(TAG, "Learning mode started");
}

void CC1101SignalProcessor::stop_learning() {
  learning_mode_ = false;
  ESP_LOGI(TAG, "Learning mode stopped");
}

void CC1101SignalProcessor::save_learned_signal(const std::string& name, const PulseData& data) {
  learned_signals_[name] = data;
  ESP_LOGI(TAG, "Signal saved as: %s (%d pulses)", name.c_str(), data.num_pulses);
}

void CC1101SignalProcessor::load_learned_signal(const std::string& name) {
  auto it = learned_signals_.find(name);
  if (it != learned_signals_.end()) {
    current_pulse_data_ = it->second;
    ESP_LOGI(TAG, "Signal loaded: %s", name.c_str());
  } else {
    ESP_LOGW(TAG, "Signal not found: %s", name.c_str());
  }
}

void CC1101SignalProcessor::transmit_learned_signal(const std::string& name) {
  auto it = learned_signals_.find(name);
  if (it != learned_signals_.end()) {
    transmit_raw_signal(it->second);
    ESP_LOGI(TAG, "Transmitting learned signal: %s", name.c_str());
  } else {
    ESP_LOGW(TAG, "Signal not found for transmission: %s", name.c_str());
  }
}

void CC1101SignalProcessor::transmit_raw_signal(const PulseData& data) {
  // NOTE: This method is not fully implemented yet
  // Would require full CC1101Component header inclusion
  ESP_LOGW(TAG, "transmit_raw_signal not implemented - use send_data_fsk() instead");
}

void CC1101SignalProcessor::transmit_protocol_signal(const std::string& protocol, const std::string& data) {
  // NOTE: This method is not fully implemented yet
  // Would require full CC1101Component header inclusion
  ESP_LOGW(TAG, "transmit_protocol_signal not implemented - use send_data_fsk() instead");
}

void CC1101SignalProcessor::start_scanning() {
  ESP_LOGI(TAG, "Signal scanning started");
  set_signal_mode(SignalMode::SCAN);
}

void CC1101SignalProcessor::stop_scanning() {
  ESP_LOGI(TAG, "Signal scanning stopped");
}

void CC1101SignalProcessor::scan_frequency_range(float start_freq, float end_freq, float step) {
  // NOTE: This method is not fully implemented yet
  // Would require full CC1101Component header inclusion
  ESP_LOGW(TAG, "scan_frequency_range not implemented yet");
}

void CC1101SignalProcessor::enable_decoding(bool enable) {
  decoding_enabled_ = enable;
  ESP_LOGI(TAG, "Decoding %s", enable ? "enabled" : "disabled");
}

void CC1101SignalProcessor::add_decoder(const std::string& name, 
                                       std::function<bool(const PulseData&, DecodedSignal&)> decoder) {
  decoders_[name] = decoder;
  ESP_LOGD(TAG, "Decoder added: %s", name.c_str());
}

float CC1101SignalProcessor::get_signal_ratio() const {
  if (signal_count_ == 0) return 0.0f;
  return (float)decoded_count_ / signal_count_ * 100.0f;
}

void CC1101SignalProcessor::process_interrupt() {
  if (!decoding_enabled_) return;
  
  // Run all decoders
  run_decoders();
}

void CC1101SignalProcessor::run_decoders() {
  if (current_pulse_data_.num_pulses < 16) return;
  
  for (auto& [name, decoder] : decoders_) {
    DecodedSignal result;
    if (decoder(current_pulse_data_, result)) {
      decoded_count_++;
      decoded_signals_.push_back(result);
      
      ESP_LOGI(TAG, "Decoded signal: %s - %s (RSSI: %.1f, %d pulses)", 
               result.protocol.c_str(), result.data.c_str(), 
               result.rssi, result.pulses);
      
      // Call signal callback
      if (signal_callback_) {
        signal_callback_(result);
      }
      
      // Keep only last 50 decoded signals
      if (decoded_signals_.size() > 50) {
        decoded_signals_.erase(decoded_signals_.begin());
      }
      
      break;  // Only use first successful decoder
    }
  }
}

void CC1101SignalProcessor::update_statistics() {
  ESP_LOGD(TAG, "Statistics - Signals: %d, Decoded: %d, Ignored: %d, Ratio: %.1f%%", 
           signal_count_, decoded_count_, ignored_count_, get_signal_ratio());
}

// Convert pulse timings to bit data for FSK signals
void CC1101SignalProcessor::convert_pulses_to_bits() {
  if (current_pulse_data_.num_pulses < 16) {
    ESP_LOGW(TAG, "Not enough pulses for bit conversion: %d", current_pulse_data_.num_pulses);
    return;
  }
  
  ESP_LOGW(TAG, "=== DECODER: Pulses=%d, Duration=%lu us, RSSI=%.1f ===", 
           current_pulse_data_.num_pulses, 
           current_pulse_data_.signal_duration,
           current_pulse_data_.rssi_db);
  
  // Calculate average pulse and gap lengths for threshold detection (MINIMAL LOGGING)
  float avg_pulse = 0.0f, avg_gap = 0.0f;
  int min_pulse = 999999, max_pulse = 0;
  int min_gap = 999999, max_gap = 0;
  
  for (unsigned int i = 0; i < current_pulse_data_.num_pulses; i++) {
    avg_pulse += current_pulse_data_.pulse[i];
    avg_gap += current_pulse_data_.gap[i];
    if (current_pulse_data_.pulse[i] < min_pulse) min_pulse = current_pulse_data_.pulse[i];
    if (current_pulse_data_.pulse[i] > max_pulse) max_pulse = current_pulse_data_.pulse[i];
    if (current_pulse_data_.gap[i] < min_gap) min_gap = current_pulse_data_.gap[i];
    if (current_pulse_data_.gap[i] > max_gap) max_gap = current_pulse_data_.gap[i];
  }
  avg_pulse /= current_pulse_data_.num_pulses;
  avg_gap /= current_pulse_data_.num_pulses;
  
  ESP_LOGW(TAG, "Pulse: %d-%d us (avg %.0f), Gap: %d-%d us (avg %.0f)", 
           min_pulse, max_pulse, avg_pulse, min_gap, max_gap, avg_gap);
  
  // Detect encoding and convert (MINIMAL LOGGING TO AVOID CRASH)
  int pulse_threshold = (min_pulse + max_pulse) / 2;
  
  std::string hex_stream = "";
  uint8_t current_byte = 0;
  int bit_count = 0;
  
  // Only process first 100 pulses to avoid log overflow
  unsigned int max_pulses = std::min((unsigned int)100, current_pulse_data_.num_pulses);
  
  for (unsigned int i = 0; i < max_pulses; i++) {
    // PWM: classify based on pulse width
    bool bit = current_pulse_data_.pulse[i] > pulse_threshold;
    
    // Build bytes
    current_byte = (current_byte << 1) | (bit ? 1 : 0);
    bit_count++;
    
    if (bit_count == 8) {
      char hex_str[4];
      snprintf(hex_str, sizeof(hex_str), "%02X", current_byte);
      hex_stream += hex_str;
      hex_stream += " ";
      bit_count = 0;
      current_byte = 0;
    }
  }
  
  // Output only the essential hex data
  ESP_LOGW(TAG, "=== HEX DATA ===");
  ESP_LOGW(TAG, "%s", hex_stream.c_str());
  ESP_LOGW(TAG, "Bytes: %d, Total pulses: %d", (int)hex_stream.length()/3, current_pulse_data_.num_pulses);
}

}  // namespace cc1101
}  // namespace esphome









