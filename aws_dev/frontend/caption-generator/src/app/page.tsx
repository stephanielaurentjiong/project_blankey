"use client";

import { useState, useRef } from "react";

// TypeScript interfaces
interface CaptionStyle {
  style: string;
  caption: string;
}

interface CaptionResponse {
  summary: string;
  captions: CaptionStyle[];
}

export default function CaptionGenerator() {
  // State management
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [results, setResults] = useState<CaptionResponse | null>(null);
  const [isDragging, setIsDragging] = useState<boolean>(false);

  // Ref for file input
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Image upload handlers
  const handleImageSelect = (file: File) => {
    if (file && file.type.startsWith("image/")) {
      setSelectedImage(file);

      // Create preview URL
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) {
          setImagePreview(e.target.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleImageSelect(file);
    }
  };

  const handleUploadAreaClick = () => {
    fileInputRef.current?.click();
  };

  // Drag and drop handlers
  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleImageSelect(files[0]);
    }
  };

  // Description input handler
  const handleDescriptionChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setDescription(e.target.value);
  };

  // Remove image handler
  const handleRemoveImage = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent triggering the upload click
    setSelectedImage(null);
    setImagePreview("");
    if (fileInputRef.current) {
      fileInputRef.current.value = ""; // Clear file input
    }
  };

  // Convert file to base64
  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const result = reader.result as string;
        // Remove data:image/jpeg;base64, prefix
        const base64 = result.split(",")[1];
        resolve(base64);
      };
      reader.onerror = (error) => reject(error);
    });
  };

  // Generate button handler - connects to AWS Lambda
  const handleGenerate = async () => {
    if (!selectedImage || !description.trim()) return;

    setIsGenerating(true);

    try {
      // Convert image to base64
      const imageBase64 = await fileToBase64(selectedImage);

      // Prepare request payload
      const payload = {
        image: imageBase64,
        description: description.trim(),
      };

      console.log("Sending request to Lambda...");
      console.log("Image file name:", selectedImage.name);
      console.log("Image file size:", selectedImage.size, "bytes");
      console.log("Description length:", description.length, "characters");
      console.log("Base64 image length:", imageBase64.length, "characters");
      console.log("Full payload:", payload);

      // Send request to your Lambda
      const response = await fetch(
        "https://xdjzzdgrff.execute-api.us-east-2.amazonaws.com/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Lambda response status:", response.status);
      console.log("Lambda response headers:", response.headers);
      console.log("Lambda response data:", data);

      if (data.success && data.output_text) {
        // Parse the output_text which should contain the JSON with captions
        const captionResponse: CaptionResponse = JSON.parse(data.output_text);
        setResults(captionResponse);

        console.log("Parsed captions:", captionResponse);
      } else {
        throw new Error(data.error || "Unknown error from Lambda");
      }
    } catch (error) {
      console.error("Error generating captions:", error);
      alert(
        `Error: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    } finally {
      setIsGenerating(false);
    }
  };

  // Copy caption to clipboard
  const handleCopyCaption = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text);

      // Visual feedback - temporarily change button text
      const button = document.querySelectorAll(".copy-button")[
        index
      ] as HTMLButtonElement;
      const originalText = button.textContent;
      button.textContent = "COPIED!";
      button.style.background = "#4caf50";

      setTimeout(() => {
        button.textContent = originalText;
        button.style.background = "";
      }, 2000);
    } catch (error) {
      console.error("Failed to copy text:", error);
      alert("Failed to copy to clipboard");
    }
  };

  // Check if generate button should be enabled
  const canGenerate =
    selectedImage && description.trim().length > 0 && !isGenerating;

  return (
    <div className="app-container">
      {/* Fluid Background */}
      <div className="fluid-bg">
        <div className="fluid-shape"></div>
        <div className="fluid-shape"></div>
        <div className="fluid-shape"></div>
      </div>

      {/* Header Container */}
      <header className="header">
        <h1>
          CAPTION
          <br />
          GENERATOR
          <br />
          AI
        </h1>
        <p>UPLOAD → DESCRIBE → GENERATE</p>
      </header>

      {/* Body Container */}
      <main className="main-content">
        <div className="content-wrapper">
          {/* Upload Section */}
          <section className="upload-section">
            <h2>Upload Image</h2>
            <div
              className={`upload-area ${selectedImage ? "has-image" : ""} ${
                isDragging ? "dragging" : ""
              }`}
              onClick={handleUploadAreaClick}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              {/* Hidden file input */}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileInputChange}
                style={{ display: "none" }}
              />

              {imagePreview ? (
                <div className="image-preview-container">
                  <div className="image-preview-wrapper">
                    <img
                      src={imagePreview}
                      alt="Preview"
                      className="image-preview"
                    />
                    <button
                      className="remove-image-btn"
                      onClick={handleRemoveImage}
                      title="Remove image"
                    >
                      ✕
                    </button>
                  </div>
                  <p className="upload-success">
                    ✓ Image uploaded successfully!
                  </p>
                  <p className="upload-change">
                    Click to change image or remove
                  </p>
                </div>
              ) : (
                <div className="upload-placeholder">
                  <div className="upload-icon">📸</div>
                  <p className="upload-text">
                    {isDragging ? "DROP IMAGE HERE" : "DROP IMAGE HERE"}
                  </p>
                  <p className="upload-subtext">OR CLICK TO BROWSE</p>
                </div>
              )}
            </div>
          </section>

          {/* Description Section */}
          <section className="description-section">
            <h2>Video Description</h2>
            <textarea
              className="description-input"
              placeholder="Describe your content here..."
              value={description}
              onChange={handleDescriptionChange}
              rows={4}
            />
            <div className="character-count">
              {description.length} characters
            </div>
          </section>

          {/* Generate Button */}
          <section className="button-section">
            <button
              className="generate-button"
              onClick={handleGenerate}
              disabled={!canGenerate}
            >
              {isGenerating ? (
                <>
                  <span>GENERATING...</span>
                  <div className="loading-dots">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                </>
              ) : (
                "GENERATE CAPTIONS"
              )}
            </button>
          </section>
          {/* Results Section */}
          {results && (
            <>
              <div className="organic-divider"></div>

              <section className={`results-section ${results ? "show" : ""}`}>
                <h2>Generated Captions</h2>
                <div className="summary">
                  <strong>{results.summary}</strong>
                </div>

                {results.captions.map((caption, index) => (
                  <div key={index} className="caption-result">
                    <div className="result-header">
                      <div className="result-title">
                        Caption {index + 1} - {caption.style}
                      </div>
                      <button
                        className="copy-button"
                        onClick={() =>
                          handleCopyCaption(caption.caption, index)
                        }
                      >
                        COPY
                      </button>
                    </div>
                    <div className="caption-text">{caption.caption}</div>
                  </div>
                ))}
              </section>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
