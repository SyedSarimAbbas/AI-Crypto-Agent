/**
 * AI Crypto Agent - 3D Experience Logic
 */

// --- Constants & Config ---
const API_BASE_URL = ''; // Use relative path for reliability

// --- Three.js Scene Setup ---
let scene, camera, renderer, particles;

function initThree() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // Add Stars / Particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 5000;
    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 10;
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.005,
        color: 0x6366f1,
        transparent: true,
        opacity: 0.8
    });

    particles = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particles);

    camera.position.z = 3;

    // Mouse movement effect
    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth - 0.5;
        const mouseY = e.clientY / window.innerHeight - 0.5;
        gsap.to(particles.rotation, {
            y: mouseX * 0.5,
            x: -mouseY * 0.5,
            duration: 2
        });
    });

    animate();

    // Hide loader
    gsap.to('#loader', {
        opacity: 0,
        duration: 1,
        onComplete: () => {
            document.getElementById('loader').style.display = 'none';
        }
    });
}

function animate() {
    requestAnimationFrame(animate);
    particles.rotation.y += 0.001;
    renderer.render(scene, camera);
}

// --- Navigation Logic ---
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('main section');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const sectionId = link.getAttribute('data-section');

            // Update active link
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Switch sections
            const activeSection = document.querySelector('section.active-section');
            const nextSection = document.getElementById(`${sectionId}-section`);

            if (activeSection === nextSection) return;

            if (typeof gsap !== 'undefined') {
                gsap.to(activeSection, {
                    opacity: 0,
                    duration: 0.3,
                    onComplete: () => {
                        activeSection.classList.remove('active-section');
                        nextSection.classList.add('active-section');
                        gsap.fromTo(nextSection, { opacity: 0 }, { opacity: 1, duration: 0.5 });
                    }
                });
            } else {
                activeSection.classList.remove('active-section');
                nextSection.classList.add('active-section');
            }
        });
    });
}

// --- Chat Logic ---
function initChat() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    async function handleSend() {
        const prompt = chatInput.value.trim();
        if (!prompt) return;

        // Add user message
        addMessage(prompt, 'user');
        chatInput.value = '';

        // --- Simulated Thinking Experience ---
        const thinkingId = showThinkingIndicator("Analyzing query...");

        try {
            // Configurable artificial delay for "thinking" (1-3 seconds)
            const thinkingDelay = Math.floor(Math.random() * 2000) + 1000;
            const startTime = Date.now();

            const response = await fetch(`${API_BASE_URL}/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) throw new Error('API Error');
            const data = await response.json();

            // Transition status text half-way through the delay
            setTimeout(() => {
                updateThinkingStatus(thinkingId, "Generating response...");
            }, thinkingDelay / 2);

            // Ensure we wait for the total thinking delay
            const elapsed = Date.now() - startTime;
            if (elapsed < thinkingDelay) {
                await new Promise(resolve => setTimeout(resolve, thinkingDelay - elapsed));
            }

            removeThinkingIndicator(thinkingId);
            addMessage(data.response, 'assistant', data.icon_url, true);

        } catch (error) {
            removeThinkingIndicator(thinkingId);
            addMessage("Error: Could not connect to the AI Agent backend. Make sure the FastAPI server is running.", 'assistant');
        }
    }

    function showThinkingIndicator(initialStatus) {
        const id = 'thinking-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = `message assistant thinking-container`;
        msgDiv.id = id;

        msgDiv.innerHTML = `
            <div class="avatar"><i class="fas fa-robot"></i></div>
            <div class="bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <span class="thinking-status">${initialStatus}</span>
                </div>
            </div>
        `;

        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function updateThinkingStatus(id, newStatus) {
        const el = document.getElementById(id);
        if (el) {
            const statusEl = el.querySelector('.thinking-status');
            if (statusEl) statusEl.textContent = newStatus;
        }
    }

    function removeThinkingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function addMessage(text, role, iconUrl = "", animateTyping = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;

        let iconHtml = `<div class="avatar"><i class="fas ${role === 'user' ? 'fa-user' : 'fa-robot'}"></i></div>`;
        let bubbleStyles = '';

        if (role === 'assistant' && iconUrl) {
            iconHtml = `<div class="avatar coin-avatar"><img src="${iconUrl}" alt="coin"></div>`;
            bubbleStyles = `style="background-image: linear-gradient(rgba(15, 23, 42, 0.92), rgba(15, 23, 42, 0.92)), url('${iconUrl}'); background-size: 80px; background-position: right 10px bottom 10px; background-repeat: no-repeat;"`;
        }

        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'bubble';
        if (bubbleStyles) bubbleDiv.setAttribute('style', bubbleStyles.match(/style="([^"]+)"/)[1]);

        msgDiv.appendChild(document.createRange().createContextualFragment(iconHtml));
        msgDiv.appendChild(bubbleDiv);
        chatMessages.appendChild(msgDiv);

        if (animateTyping && role === 'assistant') {
            typeEffect(bubbleDiv, text);
        } else {
            bubbleDiv.innerHTML = text.replace(/\n/g, '<br>');
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;

        if (typeof gsap !== 'undefined') {
            gsap.from(msgDiv, {
                opacity: 0,
                x: role === 'user' ? 20 : -20,
                duration: 0.5
            });
        }
    }

    function typeEffect(element, text) {
        let i = 0;
        const speed = 15; // ms per character
        element.innerHTML = "";

        const textWithBreaks = text.replace(/\n/g, '<br>');
        // Simple regex to split text while keeping <br> tags intact
        const parts = textWithBreaks.split(/(<br>)/g);

        let currentPartIndex = 0;
        let currentCharIndex = 0;

        function type() {
            if (currentPartIndex < parts.length) {
                const part = parts[currentPartIndex];
                if (part === '<br>') {
                    element.innerHTML += '<br>';
                    currentPartIndex++;
                    setTimeout(type, speed);
                } else {
                    if (currentCharIndex < part.length) {
                        element.innerHTML += part.charAt(currentCharIndex);
                        currentCharIndex++;
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                        setTimeout(type, speed);
                    } else {
                        currentPartIndex++;
                        currentCharIndex = 0;
                        setTimeout(type, speed);
                    }
                }
            }
        }
        type();
    }

    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
}



// --- Window Resize ---
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initThree();
    initNavigation();
    initChat();
});
