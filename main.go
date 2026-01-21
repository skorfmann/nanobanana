package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// Version is set at build time via -ldflags
var Version = "dev"

// stringSlice implements flag.Value for repeatable string flags
type stringSlice []string

func (s *stringSlice) String() string {
	return strings.Join(*s, ", ")
}

func (s *stringSlice) Set(value string) error {
	*s = append(*s, value)
	return nil
}

const (
	geminiEndpoint     = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
	openrouterEndpoint = "https://openrouter.ai/api/v1/chat/completions"
	defaultModel       = "google/gemini-3-pro-image-preview"
	httpTimeout        = 120 * time.Second
)

var validAspectRatios = map[string]bool{
	"1:1":  true,
	"2:3":  true,
	"3:2":  true,
	"3:4":  true,
	"4:3":  true,
	"4:5":  true,
	"5:4":  true,
	"9:16": true,
	"16:9": true,
	"21:9": true,
}

var validSizes = map[string]bool{
	"1K": true,
	"2K": true,
	"4K": true,
}

// Request structures
type GenerateRequest struct {
	Contents         []Content        `json:"contents"`
	GenerationConfig GenerationConfig `json:"generationConfig"`
}

type Content struct {
	Parts []Part `json:"parts"`
}

type Part struct {
	Text       string      `json:"text,omitempty"`
	InlineData *InlineData `json:"inlineData,omitempty"`
}

type GenerationConfig struct {
	ResponseModalities []string     `json:"responseModalities"`
	ImageConfig        *ImageConfig `json:"imageConfig,omitempty"`
}

type ImageConfig struct {
	AspectRatio string `json:"aspectRatio,omitempty"`
	ImageSize   string `json:"imageSize,omitempty"`
}

// Response structures
type GenerateResponse struct {
	Candidates []Candidate `json:"candidates"`
	Error      *APIError   `json:"error,omitempty"`
}

type Candidate struct {
	Content ContentResponse `json:"content"`
}

type ContentResponse struct {
	Parts []PartResponse `json:"parts"`
}

type PartResponse struct {
	InlineData *InlineData `json:"inlineData,omitempty"`
	Text       string      `json:"text,omitempty"`
}

type InlineData struct {
	MimeType string `json:"mimeType"`
	Data     string `json:"data"`
}

type APIError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
	Status  string `json:"status"`
}

// OpenRouter request structures
type OpenRouterRequest struct {
	Model       string            `json:"model"`
	Messages    []OpenRouterMsg   `json:"messages"`
	Modalities  []string          `json:"modalities"`
	ImageConfig *ImageConfig      `json:"image_config,omitempty"`
}

type OpenRouterMsg struct {
	Role    string        `json:"role"`
	Content []interface{} `json:"content"`
}

type OpenRouterTextContent struct {
	Type string `json:"type"`
	Text string `json:"text"`
}

type OpenRouterImageContent struct {
	Type     string              `json:"type"`
	ImageURL OpenRouterImageURL  `json:"image_url"`
}

type OpenRouterImageURL struct {
	URL string `json:"url"`
}

// OpenRouter response structures
type OpenRouterResponse struct {
	Choices []OpenRouterChoice `json:"choices"`
	Error   *OpenRouterError   `json:"error,omitempty"`
}

type OpenRouterChoice struct {
	Message OpenRouterMessage `json:"message"`
}

type OpenRouterMessage struct {
	Content string               `json:"content,omitempty"`
	Images  []OpenRouterImageOut `json:"images,omitempty"`
}

type OpenRouterImageOut struct {
	ImageURL OpenRouterImageURL `json:"image_url"`
}

type OpenRouterError struct {
	Message string `json:"message"`
	Code    int    `json:"code,omitempty"`
}

// APIConfig holds the configuration for which API to use
type APIConfig struct {
	UseOpenRouter bool
	APIKey        string
	Model         string
}

// FileConfig represents the configuration file structure
type FileConfig struct {
	API    string `json:"api"`    // "gemini" or "openrouter"
	Model  string `json:"model"`  // OpenRouter model name
	Aspect string `json:"aspect"` // Default aspect ratio
	Size   string `json:"size"`   // Default image size
}

// getConfigPath returns the path to the config file following XDG spec
func getConfigPath() string {
	configHome := os.Getenv("XDG_CONFIG_HOME")
	if configHome == "" {
		home, err := os.UserHomeDir()
		if err != nil {
			return ""
		}
		configHome = filepath.Join(home, ".config")
	}
	return filepath.Join(configHome, "nanobanana", "config.json")
}

// loadConfig loads configuration from the XDG config file
func loadConfig() (*FileConfig, error) {
	configPath := getConfigPath()
	if configPath == "" {
		return nil, nil
	}

	data, err := os.ReadFile(configPath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, nil
		}
		return nil, fmt.Errorf("failed to read config file: %w", err)
	}

	var config FileConfig
	if err := json.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("failed to parse config file: %w", err)
	}

	return &config, nil
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func run() error {
	// Define flags with empty defaults (will be filled from config/defaults later)
	var inputImages stringSlice
	flag.Var(&inputImages, "i", "Input image file (can be repeated for multi-image composition)")
	output := flag.String("o", "", "Output filename (auto-generated if not specified)")
	aspectFlag := flag.String("aspect", "", "Aspect ratio (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)")
	sizeFlag := flag.String("size", "", "Image size (1K, 2K, 4K)")
	modelFlag := flag.String("model", "", "OpenRouter model to use (enables OpenRouter API)")
	help := flag.Bool("h", false, "Show help")
	showVersion := flag.Bool("version", false, "Show version")

	flag.Usage = printUsage
	flag.Parse()

	if *showVersion {
		fmt.Println("nanobanana", Version)
		return nil
	}

	if *help {
		printUsage()
		return nil
	}

	// Get prompt from remaining args
	args := flag.Args()
	if len(args) == 0 {
		printUsage()
		return fmt.Errorf("no prompt provided")
	}
	prompt := strings.Join(args, " ")

	// Load config file
	fileConfig, err := loadConfig()
	if err != nil {
		return err
	}

	// Apply defaults, then config file, then CLI flags (priority: CLI > config > defaults)
	aspect := "1:1"
	size := "1K"
	model := ""
	useOpenRouter := false

	// Apply config file values
	if fileConfig != nil {
		if fileConfig.Aspect != "" {
			aspect = fileConfig.Aspect
		}
		if fileConfig.Size != "" {
			size = fileConfig.Size
		}
		if fileConfig.Model != "" {
			model = fileConfig.Model
		}
		if fileConfig.API == "openrouter" {
			useOpenRouter = true
		}
	}

	// Apply CLI flags (override config)
	if *aspectFlag != "" {
		aspect = *aspectFlag
	}
	if *sizeFlag != "" {
		size = *sizeFlag
	}
	if *modelFlag != "" {
		model = *modelFlag
		useOpenRouter = true // -model flag implies OpenRouter
	}

	// Determine which API to use and validate API key
	config := APIConfig{}
	openrouterKey := os.Getenv("OPENROUTER_API_KEY")
	geminiKey := os.Getenv("GEMINI_API_KEY")

	if useOpenRouter || model != "" || (openrouterKey != "" && geminiKey == "") {
		// Use OpenRouter
		if openrouterKey == "" {
			return fmt.Errorf("OPENROUTER_API_KEY environment variable not set (required for OpenRouter API)")
		}
		config.UseOpenRouter = true
		config.APIKey = openrouterKey
		config.Model = model
		if config.Model == "" {
			config.Model = defaultModel
		}
	} else {
		// Use Gemini
		if geminiKey == "" {
			return fmt.Errorf("GEMINI_API_KEY environment variable not set (or use OPENROUTER_API_KEY)")
		}
		config.UseOpenRouter = false
		config.APIKey = geminiKey
	}

	// Validate aspect ratio
	if !validAspectRatios[aspect] {
		return fmt.Errorf("invalid aspect ratio: %s (valid: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)", aspect)
	}

	// Validate size
	if !validSizes[size] {
		return fmt.Errorf("invalid size: %s (valid: 1K, 2K, 4K)", size)
	}

	fmt.Printf("Generating image...\n")
	fmt.Printf("  Prompt: %s\n", prompt)
	if len(inputImages) > 0 {
		fmt.Printf("  Inputs: %s\n", strings.Join(inputImages, ", "))
	}
	fmt.Printf("  Aspect: %s\n", aspect)
	fmt.Printf("  Size:   %s\n", size)
	if config.UseOpenRouter {
		fmt.Printf("  API:    OpenRouter (%s)\n", config.Model)
	} else {
		fmt.Printf("  API:    Gemini\n")
	}

	// Generate image
	var imageData []byte
	var mimeType string
	var genErr error

	if config.UseOpenRouter {
		imageData, mimeType, genErr = generateImageOpenRouter(config, prompt, inputImages, aspect, size)
	} else {
		imageData, mimeType, genErr = generateImageGemini(config.APIKey, prompt, inputImages, aspect, size)
	}
	if genErr != nil {
		return genErr
	}

	// Determine output filename
	outputPath := *output
	correctExt := extensionFromMime(mimeType)
	if outputPath == "" {
		outputPath = fmt.Sprintf("image_%s%s", time.Now().Format("20060102_150405"), correctExt)
	} else {
		// Check if user-provided extension matches the actual format
		currentExt := strings.ToLower(filepath.Ext(outputPath))
		if currentExt != correctExt {
			// Auto-correct the extension
			outputPath = strings.TrimSuffix(outputPath, filepath.Ext(outputPath)) + correctExt
			fmt.Printf("\nInfo: API returned %s format, adjusted output to: %s\n", mimeType, outputPath)
		}
	}

	// Write file
	if err := os.WriteFile(outputPath, imageData, 0644); err != nil {
		return fmt.Errorf("failed to write output file: %w", err)
	}

	fmt.Printf("\nImage saved to: %s\n", outputPath)
	return nil
}

func generateImageGemini(apiKey, prompt string, inputImages []string, aspectRatio, imageSize string) ([]byte, string, error) {
	// Build parts: input images first, then text prompt (per Gemini API pattern)
	var parts []Part

	for _, imgPath := range inputImages {
		inlineData, err := loadImage(imgPath)
		if err != nil {
			return nil, "", err
		}
		parts = append(parts, Part{InlineData: inlineData})
	}

	parts = append(parts, Part{Text: prompt})

	// Build request
	req := GenerateRequest{
		Contents: []Content{
			{
				Parts: parts,
			},
		},
		GenerationConfig: GenerationConfig{
			ResponseModalities: []string{"IMAGE", "TEXT"},
			ImageConfig: &ImageConfig{
				AspectRatio: aspectRatio,
				ImageSize:   imageSize,
			},
		},
	}

	reqBody, err := json.Marshal(req)
	if err != nil {
		return nil, "", fmt.Errorf("failed to marshal request: %w", err)
	}

	// Create HTTP request
	httpReq, err := http.NewRequest("POST", geminiEndpoint, bytes.NewReader(reqBody))
	if err != nil {
		return nil, "", fmt.Errorf("failed to create request: %w", err)
	}

	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("x-goog-api-key", apiKey)

	// Execute request
	client := &http.Client{Timeout: httpTimeout}
	resp, err := client.Do(httpReq)
	if err != nil {
		return nil, "", fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, "", fmt.Errorf("failed to read response: %w", err)
	}

	// Parse response
	var genResp GenerateResponse
	if err := json.Unmarshal(body, &genResp); err != nil {
		return nil, "", fmt.Errorf("failed to parse response: %w", err)
	}

	// Check for API error
	if genResp.Error != nil {
		return nil, "", fmt.Errorf("API error: %s (code: %d)", genResp.Error.Message, genResp.Error.Code)
	}

	// Check HTTP status
	if resp.StatusCode != http.StatusOK {
		return nil, "", fmt.Errorf("HTTP error: %s", resp.Status)
	}

	// Extract image data
	if len(genResp.Candidates) == 0 {
		return nil, "", fmt.Errorf("no candidates in response")
	}

	for _, part := range genResp.Candidates[0].Content.Parts {
		if part.InlineData != nil {
			imageData, err := base64.StdEncoding.DecodeString(part.InlineData.Data)
			if err != nil {
				return nil, "", fmt.Errorf("failed to decode image data: %w", err)
			}
			return imageData, part.InlineData.MimeType, nil
		}
	}

	return nil, "", fmt.Errorf("no image data in response")
}

func generateImageOpenRouter(config APIConfig, prompt string, inputImages []string, aspectRatio, imageSize string) ([]byte, string, error) {
	// Build content parts for OpenRouter format
	var contentParts []interface{}

	// Add input images first
	for _, imgPath := range inputImages {
		inlineData, err := loadImage(imgPath)
		if err != nil {
			return nil, "", err
		}
		// OpenRouter expects data URLs
		dataURL := fmt.Sprintf("data:%s;base64,%s", inlineData.MimeType, inlineData.Data)
		contentParts = append(contentParts, OpenRouterImageContent{
			Type: "image_url",
			ImageURL: OpenRouterImageURL{
				URL: dataURL,
			},
		})
	}

	// Add text prompt
	contentParts = append(contentParts, OpenRouterTextContent{
		Type: "text",
		Text: prompt,
	})

	// Build request
	req := OpenRouterRequest{
		Model: config.Model,
		Messages: []OpenRouterMsg{
			{
				Role:    "user",
				Content: contentParts,
			},
		},
		Modalities: []string{"image", "text"},
		ImageConfig: &ImageConfig{
			AspectRatio: aspectRatio,
			ImageSize:   imageSize,
		},
	}

	reqBody, err := json.Marshal(req)
	if err != nil {
		return nil, "", fmt.Errorf("failed to marshal request: %w", err)
	}

	// Create HTTP request
	httpReq, err := http.NewRequest("POST", openrouterEndpoint, bytes.NewReader(reqBody))
	if err != nil {
		return nil, "", fmt.Errorf("failed to create request: %w", err)
	}

	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Authorization", "Bearer "+config.APIKey)

	// Execute request
	client := &http.Client{Timeout: httpTimeout}
	resp, err := client.Do(httpReq)
	if err != nil {
		return nil, "", fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Read response
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, "", fmt.Errorf("failed to read response: %w", err)
	}

	// Check HTTP status first
	if resp.StatusCode != http.StatusOK {
		return nil, "", fmt.Errorf("HTTP error: %s - %s", resp.Status, string(body))
	}

	// Parse response
	var orResp OpenRouterResponse
	if err := json.Unmarshal(body, &orResp); err != nil {
		return nil, "", fmt.Errorf("failed to parse response: %w", err)
	}

	// Check for API error
	if orResp.Error != nil {
		return nil, "", fmt.Errorf("API error: %s", orResp.Error.Message)
	}

	// Extract image data from OpenRouter response
	if len(orResp.Choices) == 0 {
		return nil, "", fmt.Errorf("no choices in response")
	}

	if len(orResp.Choices[0].Message.Images) == 0 {
		return nil, "", fmt.Errorf("no images in response")
	}

	// Parse the data URL (format: data:image/png;base64,...)
	dataURL := orResp.Choices[0].Message.Images[0].ImageURL.URL
	if !strings.HasPrefix(dataURL, "data:") {
		return nil, "", fmt.Errorf("unexpected image URL format: %s", dataURL[:min(50, len(dataURL))])
	}

	// Extract MIME type and base64 data
	// Format: data:image/png;base64,iVBORw0KGgo...
	parts := strings.SplitN(dataURL, ",", 2)
	if len(parts) != 2 {
		return nil, "", fmt.Errorf("invalid data URL format")
	}

	// Parse the header (data:image/png;base64)
	header := parts[0]
	b64Data := parts[1]

	// Extract MIME type from header
	mimeType := "image/png" // default
	if strings.HasPrefix(header, "data:") {
		headerParts := strings.Split(header[5:], ";")
		if len(headerParts) > 0 && headerParts[0] != "" {
			mimeType = headerParts[0]
		}
	}

	// Decode base64 data
	imageData, err := base64.StdEncoding.DecodeString(b64Data)
	if err != nil {
		return nil, "", fmt.Errorf("failed to decode image data: %w", err)
	}

	return imageData, mimeType, nil
}

func extensionFromMime(mimeType string) string {
	switch mimeType {
	case "image/png":
		return ".png"
	case "image/jpeg":
		return ".jpg"
	case "image/webp":
		return ".webp"
	default:
		return ".png"
	}
}

func mimeFromExtension(path string) string {
	ext := strings.ToLower(filepath.Ext(path))
	switch ext {
	case ".png":
		return "image/png"
	case ".jpg", ".jpeg":
		return "image/jpeg"
	case ".webp":
		return "image/webp"
	case ".gif":
		return "image/gif"
	default:
		return "image/png"
	}
}

func loadImage(path string) (*InlineData, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read image %s: %w", path, err)
	}

	return &InlineData{
		MimeType: mimeFromExtension(path),
		Data:     base64.StdEncoding.EncodeToString(data),
	}, nil
}

func printUsage() {
	fmt.Fprintf(os.Stderr, `nanobanana - Generate images using Gemini or OpenRouter API

Usage:
  nanobanana [options] "prompt"

Options:
  -i <file>      Input image file (can be repeated for multi-image composition)
                  Supported formats: PNG, JPEG, WebP, GIF
  -o <file>      Output filename (auto-generated if not specified)
                  Extension auto-corrected to match API response format
  -aspect <ratio> Aspect ratio (default: 1:1)
                  Valid: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  -size <size>   Image size (default: 1K)
                  Valid: 1K, 2K, 4K
  -model <model> OpenRouter model (enables OpenRouter API)
                  Default: google/gemini-3-pro-image-preview
  -h             Show this help
  -version       Show version

Environment:
  GEMINI_API_KEY      Gemini API key
  OPENROUTER_API_KEY  OpenRouter API key

Config File:
  Location: $XDG_CONFIG_HOME/nanobanana/config.json (default: ~/.config/nanobanana/config.json)

  Example config:
    {
      "api": "openrouter",
      "model": "google/gemini-3-pro-image-preview",
      "aspect": "16:9",
      "size": "2K"
    }

  Fields:
    api     - "gemini" or "openrouter" (default: gemini)
    model   - OpenRouter model name (only used with openrouter)
    aspect  - Default aspect ratio
    size    - Default image size

Priority (highest to lowest):
  1. CLI flags
  2. Config file
  3. Environment variables (for API keys only)
  4. Built-in defaults

Examples:
  # Text-to-image generation (Gemini)
  nanobanana "a cute cat"
  nanobanana -o output.jpg "a sunset over mountains"
  nanobanana -aspect 16:9 -size 2K "cinematic landscape"

  # Using OpenRouter
  nanobanana -model google/gemini-3-pro-image-preview "a cute cat"
  nanobanana -model google/gemini-2.5-flash-image-preview "a sunset"

  # Image editing (single input)
  nanobanana -i photo.jpg "transform into watercolor style"
  nanobanana -i portrait.jpg "make it look like a Van Gogh painting"

  # Multi-image composition
  nanobanana -i background.jpg -i subject.jpg "place subject in the scene"
  nanobanana -i dress.jpg -i model.jpg "show the dress on the model"

  # Combined options
  nanobanana -i input.jpg -aspect 16:9 -size 2K -o output.jpg "cinematic edit"
`)
}
