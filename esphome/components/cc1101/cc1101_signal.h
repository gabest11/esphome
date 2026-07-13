#pragma once

#include <vector>
#include <functional>
#include <map>
#include <string>

namespace esphome {
namespace cc1101 {

// Forward declaration to avoid circular dependency
class CC1101Component;

// Signal processing structures based on rtl_433_ESP
struct PulseData {
  uint64_t offset = 0;
  uint32_t sample_rate = 1000000;  // 1MHz default
  unsigned depth_bits = 8;
  unsigned start_ago = 0;
  unsigned end_ago = 0;
  unsigned int num_pulses = 0;
  int pulse[1200];  // PD_MAX_PULSES
  int gap[1200];    // PD_MAX_PULSES
  int ook_low_estimate = 0;
  int ook_high_estimate = 0;
  int fsk_f1_est = 0;
  int fsk_f2_est = 0;
  float freq1_hz = 0.0f;
  float freq2_hz = 0.0f;
  float centerfreq_hz = 0.0f;
  float range_db = 0.0f;
  float rssi_db = 0.0f;
  float snr_db = 0.0f;
  float noise_db = 0.0f;
  int signal_rssi = 0;
  unsigned long signal_duration = 0;
  int rssi[1200];  // Per-pulse RSSI if enabled
};

struct BitBuffer {
  uint16_t num_rows = 0;
  uint16_t free_row = 0;
  uint16_t bits_per_row[50];  // BITBUF_ROWS
  uint16_t syncs_before_row[50];
  uint8_t bb[50][128];  // BITBUF_ROWS x BITBUF_COLS
};

struct DecodedSignal {
  std::string protocol;
  std::string model;
  std::string data;
  float rssi;
  int pulses;
  unsigned long duration;
  std::string raw_data;
};

// Callback types
using SignalReceivedCallback = std::function<void(const DecodedSignal&)>;
using PulseReceivedCallback = std::function<void(const PulseData&)>;
using RawDataCallback = std::function<void(const std::vector<uint8_t>&)>;

// Signal processing modes
enum class SignalMode {
  SCAN,           // Continuous scanning for signals
  LEARN,          // Learning mode for remote copying
  TRANSMIT,       // Transmission mode
  DECODE          // Decode mode
};

// Protocol types
enum class ProtocolType {
  OOK,            // On-Off Keying
  FSK,            // Frequency Shift Keying
  ASK,            // Amplitude Shift Keying
  MSK             // Minimum Shift Keying
};

class CC1101SignalProcessor {
 public:
  CC1101SignalProcessor(CC1101Component* cc1101);
  
  // Signal processing
  void set_signal_mode(SignalMode mode);
  void set_protocol_type(ProtocolType type);
  void set_rssi_threshold(int threshold);
  void set_min_pulse_length(int length);
  void set_min_signal_length(unsigned long length);
  
  // Callbacks
  void set_signal_received_callback(SignalReceivedCallback callback);
  void set_pulse_received_callback(PulseReceivedCallback callback);
  void set_raw_data_callback(RawDataCallback callback);
  
  // Signal analysis
  void process_pulse_data(const PulseData& data);
  void analyze_signal_strength();
  void detect_protocol(const PulseData& data);
  
  // Remote learning
  void start_learning();
  void stop_learning();
  void save_learned_signal(const std::string& name, const PulseData& data);
  void load_learned_signal(const std::string& name);
  void transmit_learned_signal(const std::string& name);
  
  // Signal transmission
  void transmit_raw_signal(const PulseData& data);
  void transmit_protocol_signal(const std::string& protocol, const std::string& data);
  void transmit_repeat_signal();
  
  // Signal scanning
  void start_scanning();
  void stop_scanning();
  void scan_frequency_range(float start_freq, float end_freq, float step);
  
  // Decoding
  void enable_decoding(bool enable);
  void add_decoder(const std::string& name, std::function<bool(const PulseData&, DecodedSignal&)> decoder);
  
  // Statistics
  int get_signal_count() const { return signal_count_; }
  int get_decoded_count() const { return decoded_count_; }
  int get_learned_count() const { return learned_signals_.size(); }
  float get_signal_ratio() const;
  int get_rssi_threshold() const { return rssi_threshold_; }
  
 protected:
  CC1101Component* cc1101_;
  SignalMode current_mode_;
  ProtocolType protocol_type_;
  int rssi_threshold_;
  int min_pulse_length_;
  unsigned long min_signal_length_;
  
  // Callbacks
  SignalReceivedCallback signal_callback_;
  PulseReceivedCallback pulse_callback_;
  RawDataCallback raw_data_callback_;
  
  // Signal processing
  PulseData current_pulse_data_;
  std::vector<PulseData> pulse_buffer_;
  std::vector<DecodedSignal> decoded_signals_;
  
  // Remote learning
  std::map<std::string, PulseData> learned_signals_;
  bool learning_mode_;
  
  // Decoders
  std::map<std::string, std::function<bool(const PulseData&, DecodedSignal&)>> decoders_;
  bool decoding_enabled_;
  
  // Statistics
  int signal_count_;
  int decoded_count_;
  int ignored_count_;
  
  // Internal methods
  void process_interrupt();
  void analyze_pulse_timing();
  void detect_signal_end();
  void run_decoders();
  void update_statistics();
  
 public:
  // DC306A pulse decoding (now public so it can be called from YAML)
  void convert_pulses_to_bits();
};

}  // namespace cc1101
}  // namespace esphome
