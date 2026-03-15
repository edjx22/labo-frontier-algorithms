# SSL Demo Documentation

This demo implements a Sound Source Localization (SSL) baseline using the GCC-PHAT algorithm.

## GCC-PHAT Algorithm

The Generalized Cross-Correlation with Phase Transform (GCC-PHAT) is a widely-used technique for estimating the time difference of arrival (TDOA) between signals received at two microphones.

### How it works:

1. **Cross-correlation**: Computes the correlation between two microphone signals at different time lags
2. **Phase Transform**: Applies a phase transform to emphasize the phase difference while suppressing amplitude effects
3. **Peak finding**: The lag with maximum correlation corresponds to the TDOA
4. **Angle estimation**: Converts TDOA to source angle using the microphone spacing

### Formula

```
GCC-PHAT(τ) = FFT⁻¹( X1(f) * X2*(f) / |X1(f) * X2*(f)| )
```

Where:
- `X1(f)` and `X2(f)` are the FFTs of the two microphone signals
- `τ` is the time lag

## Generated Plots

The demo generates two plots:

### 1. waveforms.png
Shows the synthetic two-microphone waveforms:
- Time-domain signals from mic1 and mic2
- Used to visualize the input signals

### 2. xcorr.png
Shows the GCC-PHAT cross-correlation result:
- Orange line: Cross-correlation values
- Red dashed line: Estimated delay
- Green dotted line: True delay
- Red dot: Peak location

## Usage Example

```python
from labo_frontier_algorithms.demo import run_ssl_demo

# Run the SSL demo
output_dir = run_ssl_demo("out")

# Output files:
# - out/waveforms.png: Input signal waveforms
# - out/xcorr.png: Cross-correlation result
# - out/result.json: Numeric results

print(f"Generated files in: {output_dir}")
```

### From command line:

```bash
python experiments/run_ssl_demo.py
```

This will create an `out/` directory with:
- `waveforms.png` - Input signal visualization
- `xcorr.png` - Cross-correlation plot
- `result.json` - Results in JSON format

## Parameters

The demo uses these default parameters:
- Sample rate: 16000 Hz
- Duration: 0.1 seconds
- Source frequency: 800 Hz
- Microphone spacing: 0.08 m (8 cm)
- True angle: 30 degrees
- SNR: 20 dB

## Expected Output

The result.json contains:
- `true_delay`: True TDOA in seconds
- `est_delay`: Estimated TDOA in seconds
- `true_angle_deg`: True source angle in degrees
- `est_angle_deg`: Estimated source angle in degrees
- `abs_error_deg`: Absolute angle error in degrees