package main

import (
	"strings"
	"testing"
)

func TestStringSlice_String(t *testing.T) {
	tests := []struct {
		name     string
		slice    stringSlice
		expected string
	}{
		{"empty", stringSlice{}, ""},
		{"single", stringSlice{"a.jpg"}, "a.jpg"},
		{"multiple", stringSlice{"a.jpg", "b.png", "c.webp"}, "a.jpg, b.png, c.webp"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.slice.String(); got != tt.expected {
				t.Errorf("stringSlice.String() = %q, want %q", got, tt.expected)
			}
		})
	}
}

func TestStringSlice_Set(t *testing.T) {
	var s stringSlice

	// First value
	if err := s.Set("a.jpg"); err != nil {
		t.Errorf("stringSlice.Set() error = %v", err)
	}
	if len(s) != 1 || s[0] != "a.jpg" {
		t.Errorf("stringSlice after first Set = %v, want [a.jpg]", s)
	}

	// Second value (should append)
	if err := s.Set("b.png"); err != nil {
		t.Errorf("stringSlice.Set() error = %v", err)
	}
	if len(s) != 2 || s[1] != "b.png" {
		t.Errorf("stringSlice after second Set = %v, want [a.jpg b.png]", s)
	}
}

func TestExtensionFromMime(t *testing.T) {
	tests := []struct {
		mimeType string
		expected string
	}{
		{"image/png", ".png"},
		{"image/jpeg", ".jpg"},
		{"image/webp", ".webp"},
		{"image/gif", ".png"},    // unsupported, defaults to .png
		{"unknown/type", ".png"}, // unknown, defaults to .png
		{"", ".png"},             // empty, defaults to .png
	}

	for _, tt := range tests {
		t.Run(tt.mimeType, func(t *testing.T) {
			if got := extensionFromMime(tt.mimeType); got != tt.expected {
				t.Errorf("extensionFromMime(%q) = %q, want %q", tt.mimeType, got, tt.expected)
			}
		})
	}
}

func TestMimeFromExtension(t *testing.T) {
	tests := []struct {
		path     string
		expected string
	}{
		{"image.png", "image/png"},
		{"image.PNG", "image/png"},
		{"image.jpg", "image/jpeg"},
		{"image.jpeg", "image/jpeg"},
		{"image.JPEG", "image/jpeg"},
		{"image.webp", "image/webp"},
		{"image.gif", "image/gif"},
		{"image.bmp", "image/png"}, // unsupported, defaults to image/png
		{"image", "image/png"},     // no extension, defaults to image/png
		{"/path/to/image.jpg", "image/jpeg"},
	}

	for _, tt := range tests {
		t.Run(tt.path, func(t *testing.T) {
			if got := mimeFromExtension(tt.path); got != tt.expected {
				t.Errorf("mimeFromExtension(%q) = %q, want %q", tt.path, got, tt.expected)
			}
		})
	}
}

func TestValidAspectRatios(t *testing.T) {
	valid := []string{"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9", "1:4", "4:1", "1:8", "8:1"}
	invalid := []string{"1:2", "16:10", "4:4", "invalid", ""}

	for _, ratio := range valid {
		t.Run("valid_"+ratio, func(t *testing.T) {
			if !validAspectRatios[ratio] {
				t.Errorf("validAspectRatios[%q] = false, want true", ratio)
			}
		})
	}

	for _, ratio := range invalid {
		t.Run("invalid_"+ratio, func(t *testing.T) {
			if validAspectRatios[ratio] {
				t.Errorf("validAspectRatios[%q] = true, want false", ratio)
			}
		})
	}
}

func TestValidSizes(t *testing.T) {
	valid := []string{"0.5K", "1K", "2K", "4K"}
	invalid := []string{"1k", "0.5k", "3K", "8K", "HD", ""}

	for _, size := range valid {
		t.Run("valid_"+size, func(t *testing.T) {
			if !validSizes[size] {
				t.Errorf("validSizes[%q] = false, want true", size)
			}
		})
	}

	for _, size := range invalid {
		t.Run("invalid_"+size, func(t *testing.T) {
			if validSizes[size] {
				t.Errorf("validSizes[%q] = true, want false", size)
			}
		})
	}
}

func TestResolveModel(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"lite", "gemini-3.1-flash-lite-image"},
		{"flash", "gemini-3.1-flash-image"},
		{"pro", "gemini-3-pro-image"},
		{"gemini-3-pro-image", "gemini-3-pro-image"},
		{"gemini-2.5-flash-image", "gemini-2.5-flash-image"},
		{"some-future-model", "some-future-model"}, // unknown IDs pass through
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			if got := resolveModel(tt.input); got != tt.expected {
				t.Errorf("resolveModel(%q) = %q, want %q", tt.input, got, tt.expected)
			}
		})
	}
}

func TestModelCapabilities(t *testing.T) {
	tests := []struct {
		name   string
		model  string
		aspect string
		size   string
		valid  bool
	}{
		{"flash_supports_0.5K", "gemini-3.1-flash-image", "1:1", "0.5K", true},
		{"flash_supports_4K", "gemini-3.1-flash-image", "16:9", "4K", true},
		{"flash_supports_extreme_ratio", "gemini-3.1-flash-image", "8:1", "1K", true},
		{"lite_rejects_2K", "gemini-3.1-flash-lite-image", "1:1", "2K", false},
		{"lite_rejects_0.5K", "gemini-3.1-flash-lite-image", "1:1", "0.5K", false},
		{"lite_supports_1K", "gemini-3.1-flash-lite-image", "16:9", "1K", true},
		{"lite_rejects_extreme_ratio", "gemini-3.1-flash-lite-image", "4:1", "1K", false},
		{"pro_rejects_0.5K", "gemini-3-pro-image", "1:1", "0.5K", false},
		{"pro_supports_4K", "gemini-3-pro-image", "21:9", "4K", true},
		{"pro_rejects_extreme_ratio", "gemini-3-pro-image", "1:8", "1K", false},
		{"legacy_supports_1K", "gemini-2.5-flash-image", "1:1", "1K", true},
		{"legacy_rejects_4K", "gemini-2.5-flash-image", "1:1", "4K", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			caps, known := modelCapabilities[tt.model]
			if !known {
				t.Fatalf("modelCapabilities missing entry for %q", tt.model)
			}
			got := caps.aspectRatios[tt.aspect] && caps.sizes[tt.size]
			if got != tt.valid {
				t.Errorf("model %s aspect=%s size=%s: valid = %v, want %v", tt.model, tt.aspect, tt.size, got, tt.valid)
			}
		})
	}
}

func TestLegacyModelOmitsSizeParam(t *testing.T) {
	if modelCapabilities["gemini-2.5-flash-image"].sizeParam {
		t.Error("gemini-2.5-flash-image should not send imageConfig.imageSize")
	}
	for _, model := range []string{"gemini-3.1-flash-lite-image", "gemini-3.1-flash-image", "gemini-3-pro-image"} {
		if !modelCapabilities[model].sizeParam {
			t.Errorf("%s should send imageConfig.imageSize", model)
		}
	}
}

func TestExtensionAutoCorrection(t *testing.T) {
	tests := []struct {
		name        string
		userOutput  string
		mimeType    string
		expectedExt string
	}{
		{"png_to_jpg", "output.png", "image/jpeg", ".jpg"},
		{"jpg_stays_jpg", "output.jpg", "image/jpeg", ".jpg"},
		{"png_stays_png", "output.png", "image/png", ".png"},
		{"webp_to_jpg", "output.webp", "image/jpeg", ".jpg"},
		{"no_ext_to_jpg", "output", "image/jpeg", ".jpg"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			correctExt := extensionFromMime(tt.mimeType)

			// Simulate the auto-correction logic from run()
			outputPath := tt.userOutput
			currentExt := strings.ToLower(getExt(outputPath))
			if currentExt != correctExt {
				outputPath = strings.TrimSuffix(outputPath, getExt(outputPath)) + correctExt
			}

			if !strings.HasSuffix(outputPath, tt.expectedExt) {
				t.Errorf("auto-correction for %q with mime %q = %q, want suffix %q",
					tt.userOutput, tt.mimeType, outputPath, tt.expectedExt)
			}
		})
	}
}

// Helper to get extension (mirrors filepath.Ext behavior)
func getExt(path string) string {
	for i := len(path) - 1; i >= 0; i-- {
		if path[i] == '.' {
			return path[i:]
		}
		if path[i] == '/' {
			break
		}
	}
	return ""
}
