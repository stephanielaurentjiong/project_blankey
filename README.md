# PROJECT BLANKEY #
LLM-based caption generator for content creating


# Image + Text Caption Recommendation Web App (Qwen-2.5 VL + vLLM)

## Project Context & Background
We are building a **web application** that allows users to upload an image along with a short text description (optional) and generates high-quality, attention-grabbing captions or titles.  

- **Objective**: Help users (e.g., content creators) generate captions that increase engagement.  
- **Motivation**: Automating caption generation reduces manual work, increases creativity, and provides personalized suggestions.  
- **Technology Stack Highlights**:  
  - **Qwen-2.5 VL**: End-to-end multimodal large language model (LLM) capable of understanding images and text simultaneously.   https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct-AWQ
  - **vLLM**: High-efficiency inference engine optimized for GPU, increasing throughput and reducing memory usage.  
  - **AWS Services**: SageMaker (model hosting), Lambda (serverless backend), S3 (storage).  
- **Team Roles**:  
  - **Scientist (S)** → Data collection, model training/fine-tuning, prompt engineering.  
  - **Engineer (E)** → Frontend, backend/API integration, deployment, and cloud infrastructure.  

---

## Phase 0: Project Setup & Quick Start Prototype
**Goal**: Validate the concept quickly using existing LLM APIs before deploying a large model.

### Action Items
| Task | Owner | Dependencies | Notes |
|------|-------|--------------|------|
| Select LLM API for prototype (e.g., Claude, GPT-4V) | S | None | Ensure API supports multimodal input if possible. |
| Design initial prompt schema | S | None | Decide input format and expected output style. |
| Build minimal frontend | E | None | Use React or Next.js. Add image upload, text input, submit button, and output display. Host in s3. |
| Integrate API call from frontend | E | Frontend ready | Use Axios/fetch to call API or Lambda; return JSON. |
| Display results in frontend | E | API integrated | Show caption, handle errors gracefully. |

**Outcome**: Proof-of-concept web app.  
**Duration**: 1–2 weeks  

---

## Phase 1: MVP – Required Features
**Goal**: End-to-end app using **Qwen-2.5 VL + vLLM** for inference.

### 1. Data Preparation
| Task | Owner | Dependencies | Notes |
|------|-------|--------------|------|
| Collect/curate dataset (image + text pairs) | S | None | Use COCO, LAION, or internal sources. |
| Store dataset in S3 | E | None | Structured storage for training + inference. |

### 2. Model Training / Deployment
| Task | Owner | Dependencies | Notes |
|------|-------|--------------|------|
| Select Qwen-2.5 VL backbone | S | Dataset collected | Decide full fine-tuning vs LoRA. |
| Prepare Docker image (PyTorch + vLLM + model) | E | Model ready | GPU optimized inference. Test locally. |
| Upload model weights to S3 | E | Training done | Versioning required. |
| Deploy SageMaker GPU Endpoint | E | Docker ready | Use `ml.g5.xlarge` or similar. Configure endpoint + autoscaling. |

### 3. Backend / API
| Task | Owner | Dependencies | Notes |
|------|-------|--------------|------|
| Lambda function for requests | E | Frontend ready | Accept image + text, format request. |
| Call SageMaker Endpoint | E | Endpoint deployed | Handle response + errors. |
| API Gateway setup | E | Lambda ready | Configure HTTPS endpoint, optional auth. |

### 4. Frontend
| Task | Owner | Dependencies | Notes |
|------|-------|--------------|------|
| Upload image + optional description | E | None | Validate file type and size. |
| Display single caption | E | Lambda ready | Show output, spinner for loading. |

**Outcome**: MVP working with required features.  

---

## Phase 2: Optional Features & Expansion
**Goal**: Enhance UX and prepare for iteration.

### Features
1. **Multiple Candidate Captions**  
   - Lambda generates multiple options.  
   - Frontend displays them (card-style UI).  

2. **User Feedback & Logging**  
   - Store input + output in DynamoDB or S3.  
   - Add like/edit feedback for users.  

3. **History / Favorites**  
   - Store per-user history.  
   - Display in frontend.  

4. **UX & Performance Improvements**  
   - Mobile-friendly design (TailwindCSS/Material UI).  
   - Streaming caption display for faster feel.  
   - Prompt tuning with logs.  
   - **Optional: Multi-turn Dialogue** → Allow users to refine captions interactively (chat-like interface).  

---

## Phase 3: RAG Integration (Trend-Aware Captions)
**Goal**: Make captions trend-aware by pulling real-time context.  

### Action Items
| Task | Owner | Dependencies | Notes |
|------|-------|--------------|------|
| Implement RAG pipeline | S/E | MVP ready | Use LangChain, Hugging Face, or scrapers. |
| Integrate RAG into prompt | S | RAG pipeline ready | Inject trending keywords into caption prompt. |
| Update Lambda for RAG context | E | SageMaker ready | Prepend/append trends before calling model. |
| Frontend display | E | Lambda updated | Highlight trend words if possible. |

**Outcome**: Captions that include current, popular phrases.  

---

## Phase 4: Industrial Optimization
- Auto-scaling GPU endpoints  
- Optimize vLLM memory and KV cache  
- Monitoring for latency, quality, and errors  
- Optional: move to serverless endpoints  

---

## Suggested Timeline
| Phase | Duration | Owner | Notes |
|-------|----------|-------|------|
| Phase 0: Quick Prototype | 1–2 weeks | S/E | Validate with API |
| Phase 1: MVP | 3–4 weeks | S/E | Core system ready |
| Phase 2: Optional Features | 2–3 weeks | S/E | Feedback + multi-turn |
| Phase 3: RAG Integration | 2 weeks | S/E | Trend-aware captions |
| Phase 4: Optimization | 2–3 weeks | S/E | Scaling + monitoring |

**Principles**  
1. Start simple → validate → expand  
2. Parallelize tasks where possible  
3. Each phase is self-contained  
4. Logging early enables better fine-tuning later  

---

## Glossary
| Term | Explanation |
|------|-------------|
| **AWS SageMaker** | Hosts Qwen-2.5 VL and provides GPU inference. |
| **Qwen-2.5 VL** | Multimodal LLM for image + text captioning. |
| **vLLM** | Efficient GPU inference engine for LLMs. |
| **LoRA** | Lightweight fine-tuning method. |
| **AWS Lambda** | Formats requests and calls SageMaker. |
| **S3** | Stores training data, images, and model weights. |
| **API Gateway** | HTTPS endpoint for frontend → backend communication. |
| **Docker** | Packages model + dependencies for SageMaker deployment. |
| **Prompt** | Instructions for the LLM to generate captions. |
| **KV Cache (vLLM)** | Memory optimization storing intermediate attention states. |

---

## Phase 0 Quick Start (Scientist) — Bedrock + Claude 3.5 Sonnet

Minimal prototype to generate a caption from an image using AWS Bedrock Anthropic Claude 3.5 Sonnet with a predefined prompt.

### Prerequisites
- AWS account with Bedrock access to Anthropic models (Claude 3.5 Sonnet)
- AWS credentials configured locally (env vars or `~/.aws/credentials`)
- Python 3.9+

### Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
python phase0/bedrock_caption_cli.py \
  --image /path/to/image.jpg \
  --context "sunset at the beach, chill vibe" \
  --region us-east-1
```

Outputs a single caption string to stdout.

Notes:
- Uses a built-in prompt to produce one concise caption (<100 chars), no emojis/hashtags.
- If the model returns JSON, the tool extracts `{ "caption": "..." }`; otherwise falls back to raw text.
- Set `AWS_PROFILE` or pass `--profile` to select a named profile.
