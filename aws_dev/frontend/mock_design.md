<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CAPTION.GENERATOR.AI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'JetBrains Mono', monospace;
            background: linear-gradient(45deg, #f8f8f8 0%, #ffffff 100%);
            min-height: 100vh;
            color: #1a1a1a;
            overflow-x: hidden;
            position: relative;
        }
        
        /* Organic fluid background shapes */
        .fluid-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }
        
        .fluid-shape {
            position: absolute;
            background: linear-gradient(45deg, #e5e5e5, #d0d0d0);
            border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
            opacity: 0.3;
            animation: morph 8s ease-in-out infinite;
        }
        
        .fluid-shape:nth-child(1) {
            width: 400px;
            height: 400px;
            top: -200px;
            left: -200px;
            animation-delay: 0s;
        }
        
        .fluid-shape:nth-child(2) {
            width: 300px;
            height: 300px;
            bottom: -150px;
            right: -150px;
            animation-delay: -4s;
            background: linear-gradient(45deg, #d0d0d0, #b8b8b8);
        }
        
        .fluid-shape:nth-child(3) {
            width: 250px;
            height: 250px;
            top: 30%;
            right: 10%;
            animation-delay: -2s;
            background: linear-gradient(45deg, #c8c8c8, #e5e5e5);
        }
        
        @keyframes morph {
            0%, 100% {
                border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
                transform: translate(0px, 0px) rotate(0deg) scale(1);
            }
            33% {
                border-radius: 70% 30% 50% 50% / 30% 60% 70% 40%;
                transform: translate(30px, -50px) rotate(120deg) scale(1.1);
            }
            66% {
                border-radius: 50% 60% 30% 60% / 50% 40% 60% 30%;
                transform: translate(-20px, 20px) rotate(240deg) scale(0.9);
            }
        }
        
        /* Brutalist container */
        .container {
            max-width: none;
            width: 100vw;
            min-height: 100vh;
            padding: 0;
            display: flex;
            flex-direction: column;
        }
        
        /* Harsh brutalist header */
        .header {
            background: #1a1a1a;
            border-bottom: 8px solid #000000;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -50%;
            width: 200%;
            height: 100%;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 2px,
                rgba(255, 255, 255, 0.05) 2px,
                rgba(255, 255, 255, 0.05) 4px
            );
            animation: slide 10s linear infinite;
        }
        
        @keyframes slide {
            0% { transform: translateX(0); }
            100% { transform: translateX(50px); }
        }
        
        .header h1 {
            font-size: clamp(2rem, 8vw, 4rem);
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: -0.05em;
            line-height: 0.9;
            color: #ffffff;
            text-shadow: 
                3px 3px 0px #666666,
                6px 6px 0px #999999,
                9px 9px 0px #cccccc;
            position: relative;
            z-index: 2;
            margin-bottom: 1rem;
        }
        
        .header p {
            font-size: 1.2rem;
            color: #cccccc;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            position: relative;
            z-index: 2;
        }
        
        /* Main brutal card */
        .caption-card {
            flex: 1;
            background: #ffffff;
            border: none;
            border-top: 16px solid #1a1a1a;
            padding: 0;
            position: relative;
            overflow: hidden;
        }
        
        /* Organic divider between sections */
        .organic-divider {
            height: 60px;
            background: #666666;
            position: relative;
            clip-path: polygon(0% 0%, 100% 0%, 100% 70%, 85% 100%, 15% 100%, 0% 70%);
            margin: 2rem 0;
            animation: wave 6s ease-in-out infinite;
        }
        
        @keyframes wave {
            0%, 100% {
                clip-path: polygon(0% 0%, 100% 0%, 100% 70%, 85% 100%, 15% 100%, 0% 70%);
            }
            50% {
                clip-path: polygon(0% 0%, 100% 0%, 100% 100%, 70% 85%, 30% 85%, 0% 100%);
            }
        }
        
        /* Input section with brutal styling */
        .input-section {
            padding: 3rem;
            background: #f8f8f8;
            position: relative;
        }
        
        .input-section::after {
            content: 'INPUT.ZONE';
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 0.7rem;
            color: #666666;
            font-weight: 700;
            letter-spacing: 0.2em;
        }
        
        /* Brutal upload area with organic hover */
        .upload-area {
            background: #ffffff;
            border: 4px solid #1a1a1a;
            padding: 3rem 2rem;
            position: relative;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.23, 1, 0.320, 1);
            margin-bottom: 2rem;
            overflow: hidden;
        }
        
        .upload-area::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, #666666, transparent);
            transition: left 0.6s ease;
            z-index: 1;
        }
        
        .upload-area:hover {
            border-color: #666666;
            transform: scale(1.02) rotate(0.5deg);
            box-shadow: 16px 16px 0px #cccccc;
        }
        
        .upload-area:hover::before {
            left: 100%;
        }
        
        .upload-area.has-image {
            border-color: #1a1a1a;
            background: #f0f0f0;
            transform: skew(-1deg);
        }
        
        .upload-area.has-image:hover {
            box-shadow: 16px 16px 0px #999999;
        }
        
        .upload-content {
            position: relative;
            z-index: 2;
            text-align: center;
        }
        
        .upload-icon {
            width: 64px;
            height: 64px;
            margin: 0 auto 1rem;
            color: #1a1a1a;
        }
        
        .upload-text {
            font-size: 1.5rem;
            font-weight: 800;
            color: #1a1a1a;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            letter-spacing: 0.1em;
        }
        
        .upload-subtext {
            color: #666666;
            font-size: 1rem;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Image preview with organic shape */
        .image-preview {
            display: none;
            max-width: 200px;
            max-height: 200px;
            margin: 1rem auto;
            border: 4px solid #1a1a1a;
            position: relative;
            clip-path: polygon(10% 0%, 100% 0%, 90% 100%, 0% 100%);
            transition: clip-path 0.5s ease;
        }
        
        .image-preview.show {
            display: block;
            animation: morphIn 0.8s cubic-bezier(0.23, 1, 0.320, 1);
        }
        
        @keyframes morphIn {
            0% {
                clip-path: polygon(50% 50%, 50% 50%, 50% 50%, 50% 50%);
                opacity: 0;
                transform: scale(0.5);
            }
            100% {
                clip-path: polygon(10% 0%, 100% 0%, 90% 100%, 0% 100%);
                opacity: 1;
                transform: scale(1);
            }
        }
        
        /* Brutal text input */
        .text-input {
            width: 100%;
            background: #ffffff;
            border: 4px solid #1a1a1a;
            padding: 1.5rem;
            color: #1a1a1a;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.1rem;
            font-weight: 400;
            resize: vertical;
            min-height: 120px;
            transition: all 0.3s ease;
        }
        
        .text-input::placeholder {
            color: #999999;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 0.05em;
        }
        
        .text-input:focus {
            outline: none;
            border-color: #666666;
            background: #f8f8f8;
            box-shadow: inset 8px 8px 0px rgba(102, 102, 102, 0.1);
        }
        
        /* Minimalistic button */
        .generate-btn {
            width: 100%;
            background: #1a1a1a;
            border: none;
            padding: 1.5rem;
            color: #ffffff;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            cursor: pointer;
            margin-top: 2rem;
            position: relative;
            transition: all 0.2s ease;
        }
        
        .generate-btn:hover:not(:disabled) {
            background: #000000;
            transform: translateY(-1px);
        }
        
        .generate-btn:active {
            transform: translateY(0);
        }
        
        .generate-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            background: #cccccc;
            color: #666666;
        }
        
        .btn-text {
            transition: opacity 0.3s ease;
        }
        
        .btn-text.processing {
            opacity: 0;
        }
        
        /* Loading animation with organic dots */
        .loading-dots {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            gap: 8px;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .loading-dots.show {
            opacity: 1;
        }
        
        .dot {
            width: 12px;
            height: 12px;
            background: #ffffff;
            border-radius: 50%;
            animation: brutalistBounce 1.4s ease-in-out infinite both;
        }
        
        .dot:nth-child(1) { 
            animation-delay: -0.32s;
            border-radius: 0%;
        }
        .dot:nth-child(2) { 
            animation-delay: -0.16s;
            border-radius: 30%;
        }
        .dot:nth-child(3) { 
            animation-delay: 0;
            border-radius: 50%;
        }
        
        @keyframes brutalistBounce {
            0%, 80%, 100% {
                transform: scale(0) rotate(0deg);
            } 
            40% {
                transform: scale(1.2) rotate(180deg);
            }
        }
        
        /* Results section */
        .results-section {
            background: #f8f8f8;
            padding: 3rem;
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.6s cubic-bezier(0.23, 1, 0.320, 1);
            position: relative;
        }
        
        .results-section::before {
            content: 'OUTPUT.ZONE';
            position: absolute;
            top: 10px;
            right: 20px;
            font-size: 0.7rem;
            color: #666666;
            font-weight: 700;
            letter-spacing: 0.2em;
        }
        
        .results-section.show {
            opacity: 1;
            transform: translateY(0);
        }
        
        .caption-result {
            background: #ffffff;
            border: 4px solid #1a1a1a;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .caption-result::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 8px;
            background: linear-gradient(90deg, #1a1a1a, #666666, #1a1a1a);
            background-size: 200% 100%;
            animation: sweep 3s linear infinite;
        }
        
        @keyframes sweep {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .result-title {
            font-size: 1.2rem;
            font-weight: 800;
            color: #1a1a1a;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        .copy-btn {
            background: #666666;
            color: #ffffff;
            border: none;
            padding: 0.8rem 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            text-transform: uppercase;
            cursor: pointer;
            transition: all 0.2s ease;
            clip-path: polygon(0% 0%, 90% 0%, 100% 100%, 10% 100%);
        }
        
        .copy-btn:hover {
            background: #1a1a1a;
            color: #ffffff;
            transform: scale(1.1);
        }
        
        .copy-btn:active {
            transform: scale(0.95);
        }
        
        .caption-text {
            color: #1a1a1a;
            font-size: 1rem;
            line-height: 1.6;
            font-weight: 400;
            border-left: 4px solid #666666;
            padding-left: 1rem;
        }100% 100%, 10% 100%);
        }
        
        .copy-btn:hover {
            background: #ffffff;
            color: #000000;
            transform: scale(1.1);
        }
        
        .copy-btn:active {
            transform: scale(0.95);
        }
        
        .caption-text {
            color: #ffffff;
            font-size: 1rem;
            line-height: 1.6;
            font-weight: 400;
            border-left: 4px solid #e91e63;
            padding-left: 1rem;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .header {
                padding: 1rem;
            }
            
            .input-section,
            .results-section {
                padding: 1.5rem;
            }
            
            .generate-btn {
                padding: 1.5rem;
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="fluid-bg">
        <div class="fluid-shape"></div>
        <div class="fluid-shape"></div>
        <div class="fluid-shape"></div>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>CAPTION<br>GENERATOR<br>AI</h1>
            <p>UPLOAD → DESCRIBE → GENERATE</p>
        </div>
        
        <div class="caption-card">
            <div class="input-section" id="inputSection">
                <div class="upload-area" id="uploadArea">
                    <div class="upload-content">
                        <svg class="upload-icon" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
                        </svg>
                        <div class="upload-text">DROP IMAGE HERE</div>
                        <div class="upload-subtext">OR CLICK TO BROWSE</div>
                        <img class="image-preview" id="imagePreview" alt="Preview" />
                    </div>
                </div>
                
                <textarea 
                    class="text-input" 
                    id="descriptionInput"
                    placeholder="DESCRIBE YOUR CONTENT HERE..."
                    rows="4"
                ></textarea>
                
                <button class="generate-btn" id="generateBtn">
                    <span class="btn-text" id="btnText">GENERATE CAPTION</span>
                    <div class="loading-dots" id="loadingDots">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </button>
            </div>
            
            <div class="organic-divider"></div>
            
            <div class="results-section" id="resultsSection">
                <div class="caption-result">
                    <div class="result-header">
                        <div class="result-title">AI OUTPUT</div>
                        <button class="copy-btn" onclick="copyCaption()">COPY</button>
                    </div>
                    <div class="caption-text" id="captionText"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let hasImage = false;
        let isProcessing = false;
        
        const uploadArea = document.getElementById('uploadArea');
        const imagePreview = document.getElementById('imagePreview');
        const descriptionInput = document.getElementById('descriptionInput');
        const generateBtn = document.getElementById('generateBtn');
        const btnText = document.getElementById('btnText');
        const loadingDots = document.getElementById('loadingDots');
        const inputSection = document.getElementById('inputSection');
        const resultsSection = document.getElementById('resultsSection');
        const captionText = document.getElementById('captionText');
        
        const sampleCaptions = [
            "CRUSHING IT IN THE MORNING! 💪 That post-workout energy hits different when you start early. Every rep brings you closer to your goals. NO EXCUSES, JUST RESULTS. #MorningGrind #FitnessLife",
            
            "5AM CLUB MEMBER ✅ Another session complete ✅ The gym doesn't lie - it only responds to effort. Started from the bottom, now we're stronger. #EarlyBird #StrengthJourney",
            
            "SWEAT IS JUST WEAKNESS LEAVING THE BODY 🔥 Every morning I choose to invest in myself. The hardest part? Showing up. Everything else is momentum. #NoExcuses #GymLife"
        ];
        
        // File upload handling
        uploadArea.addEventListener('click', () => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = handleFileSelect;
            input.click();
        });
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect({ target: { files } });
            }
        });
        
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith('image/')) {
                hasImage = true;
                uploadArea.classList.add('has-image');
                
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagePreview.src = e.target.result;
                    imagePreview.classList.add('show');
                    updateGenerateButton();
                };
                reader.readAsDataURL(file);
            }
        }
        
        descriptionInput.addEventListener('input', updateGenerateButton);
        
        function updateGenerateButton() {
            const hasText = descriptionInput.value.trim().length > 0;
            generateBtn.disabled = !hasImage || !hasText || isProcessing;
        }
        
        generateBtn.addEventListener('click', generateCaption);
        
        async function generateCaption() {
            if (isProcessing) return;
            
            isProcessing = true;
            updateGenerateButton();
            
            btnText.style.opacity = '0';
            loadingDots.classList.add('show');
            
            await new Promise(resolve => setTimeout(resolve, 3000));
            
            const randomCaption = sampleCaptions[Math.floor(Math.random() * sampleCaptions.length)];
            showResults(randomCaption);
            
            isProcessing = false;
            btnText.style.opacity = '1';
            loadingDots.classList.remove('show');
            updateGenerateButton();
        }
        
        function showResults(caption) {
            captionText.textContent = '';
            resultsSection.classList.add('show');
            
            let i = 0;
            const typeWriter = () => {
                if (i < caption.length) {
                    captionText.textContent += caption.charAt(i);
                    i++;
                    setTimeout(typeWriter, 25);
                }
            };
            
            setTimeout(typeWriter, 300);
        }
        
        function copyCaption() {
            const text = captionText.textContent;
            const copyBtn = document.querySelector('.copy-btn');
            
            navigator.clipboard.writeText(text).then(() => {
                copyBtn.textContent = 'COPIED!';
                copyBtn.style.background = '#4caf50';
                
                setTimeout(() => {
                    copyBtn.textContent = 'COPY';
                    copyBtn.style.background = '#e91e63';
                }, 2000);
            });
        }
        
        updateGenerateButton();
    </script>
</body>
</html>