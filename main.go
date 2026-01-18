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
	apiEndpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
	httpTimeout = 120 * time.Second
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

func main() {
	if err := run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func run() error {
	// Define flags
	var inputImages stringSlice
	flag.Var(&inputImages, "i", "Input image file (can be repeated for multi-image composition)")
	output := flag.String("o", "", "Output filename (auto-generated if not specified)")
	aspect := flag.String("aspect", "1:1", "Aspect ratio (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)")
	size := flag.String("size", "1K", "Image size (1K, 2K, 4K)")
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

	// Validate API key
	apiKey := os.Getenv("GEMINI_API_KEY")
	if apiKey == "" {
		return fmt.Errorf("GEMINI_API_KEY environment variable not set")
	}

	// Validate aspect ratio
	if !validAspectRatios[*aspect] {
		return fmt.Errorf("invalid aspect ratio: %s (valid: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9)", *aspect)
	}

	// Validate size
	if !validSizes[*size] {
		return fmt.Errorf("invalid size: %s (valid: 1K, 2K, 4K)", *size)
	}

	fmt.Printf("Generating image...\n")
	fmt.Printf("  Prompt: %s\n", prompt)
	if len(inputImages) > 0 {
		fmt.Printf("  Inputs: %s\n", strings.Join(inputImages, ", "))
	}
	fmt.Printf("  Aspect: %s\n", *aspect)
	fmt.Printf("  Size:   %s\n", *size)

	// Generate image
	imageData, mimeType, err := generateImage(apiKey, prompt, inputImages, *aspect, *size)
	if err != nil {
		return err
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

func generateImage(apiKey, prompt string, inputImages []string, aspectRatio, imageSize string) ([]byte, string, error) {
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
	httpReq, err := http.NewRequest("POST", apiEndpoint, bytes.NewReader(reqBody))
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
	fmt.Fprintf(os.Stderr, `nanobanana - Generate images using Gemini API

Usage:
  nanobanana [options] "prompt"

Options:
  -i <file>      Input image file (can be repeated for multi-image composition)
                  Supported formats: PNG, JPEG, WebP, GIF
  -o <file>      Output filename (auto-generated if not specified)
  -aspect <ratio> Aspect ratio (default: 1:1)
                  Valid: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  -size <size>   Image size (default: 1K)
                  Valid: 1K, 2K, 4K
  -h             Show this help
  -version       Show version

Environment:
  GEMINI_API_KEY  Required. Your Gemini API key.

Examples:
  # Text-to-image generation
  nanobanana "a cute cat"
  nanobanana -o output.png "a sunset over mountains"
  nanobanana -aspect 16:9 -size 2K "cinematic landscape"

  # Image editing (single input)
  nanobanana -i photo.jpg "transform into watercolor style"
  nanobanana -i portrait.png "make it look like a Van Gogh painting"

  # Multi-image composition
  nanobanana -i background.png -i subject.png "place subject in the scene"
  nanobanana -i dress.png -i model.png "show the dress on the model"

  # Combined options
  nanobanana -i input.jpg -aspect 16:9 -size 2K -o output.png "cinematic edit"
`)
}
