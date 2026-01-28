// DarkFlobi Empire - Interactive JavaScript

// Particle System
class ParticleSystem {
    constructor() {
        this.particles = [];
        this.container = document.getElementById('particles');
        this.init();
    }

    init() {
        this.createParticles();
        this.animate();
    }

    createParticles() {
        const particleCount = 50;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const size = Math.random() * 4 + 1;
            const x = Math.random() * window.innerWidth;
            const y = Math.random() * window.innerHeight;
            const duration = Math.random() * 3 + 2;
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${x}px`;
            particle.style.top = `${y}px`;
            particle.style.animationDuration = `${duration}s`;
            particle.style.animationDelay = `${Math.random() * 2}s`;
            
            this.container.appendChild(particle);
            this.particles.push({
                element: particle,
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5
            });
        }
    }

    animate() {
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around screen
            if (particle.x < 0) particle.x = window.innerWidth;
            if (particle.x > window.innerWidth) particle.x = 0;
            if (particle.y < 0) particle.y = window.innerHeight;
            if (particle.y > window.innerHeight) particle.y = 0;
            
            particle.element.style.left = `${particle.x}px`;
            particle.element.style.top = `${particle.y}px`;
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

// Counter Animation
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = start + (target - start) * easeOutQuart(progress);
        
        if (target === Infinity || target === '∞') {
            element.textContent = '∞';
        } else {
            element.textContent = Math.floor(current);
        }
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function easeOutQuart(t) {
    return 1 - (--t) * t * t * t;
}

// Countdown Timer
function startCountdown() {
    // Set launch date (7 days from now for demo)
    const launchDate = new Date();
    launchDate.setDate(launchDate.getDate() + 7);
    launchDate.setHours(12, 0, 0, 0); // Noon
    
    function updateCountdown() {
        const now = new Date().getTime();
        const distance = launchDate.getTime() - now;
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        document.getElementById('days').textContent = String(days).padStart(2, '0');
        document.getElementById('hours').textContent = String(hours).padStart(2, '0');
        document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
        document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
        
        if (distance < 0) {
            document.querySelector('.countdown-container h3').textContent = '🚀 LAUNCHED!';
            document.querySelectorAll('.countdown-number').forEach(el => el.textContent = '00');
        }
    }
    
    updateCountdown();
    setInterval(updateCountdown, 1000);
}

// Activity Feed Simulation
class ActivityFeed {
    constructor() {
        this.activities = [
            "Trading Demon executed 15 trades",
            "Research Gremlin found new opportunity",
            "Code Gremlin deployed hotfix",
            "Vibe Manager engaged 47 users",
            "Security Guard blocked 3 attacks",
            "Number Cruncher analyzed market trends",
            "Trading Demon spotted arbitrage opportunity",
            "Community Manager onboarded 12 new users",
            "Research Gremlin discovered emerging token",
            "Code Gremlin optimized smart contract",
            "Analytics team updated dashboard metrics",
            "Security system performed routine scan"
        ];
        
        this.feed = document.querySelector('.activity-feed');
        this.startFeed();
    }
    
    startFeed() {
        setInterval(() => {
            this.addActivity();
        }, 3000); // Add new activity every 3 seconds
    }
    
    addActivity() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit' 
        });
        
        const randomActivity = this.activities[Math.floor(Math.random() * this.activities.length)];
        
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.style.opacity = '0';
        activityItem.style.transform = 'translateY(-10px)';
        
        activityItem.innerHTML = `
            <span class="activity-time">${timeStr}</span>
            <span class="activity-text">${randomActivity}</span>
        `;
        
        // Remove oldest if we have too many
        const items = this.feed.querySelectorAll('.activity-item');
        if (items.length >= 4) {
            items[0].remove();
        }
        
        this.feed.appendChild(activityItem);
        
        // Animate in
        setTimeout(() => {
            activityItem.style.transition = 'opacity 0.3s, transform 0.3s';
            activityItem.style.opacity = '1';
            activityItem.style.transform = 'translateY(0)';
        }, 100);
    }
}

// Project Progress Simulation
class ProjectProgress {
    constructor() {
        this.projects = document.querySelectorAll('.project-status');
        this.updateProgress();
    }
    
    updateProgress() {
        setInterval(() => {
            this.projects.forEach(project => {
                const current = parseInt(project.textContent);
                if (current < 100) {
                    const increment = Math.random() < 0.7 ? 1 : 0; // 70% chance to increment
                    project.textContent = `${Math.min(current + increment, 100)}%`;
                }
            });
        }, 5000); // Update every 5 seconds
    }
}

// Metrics Animation
class MetricsUpdater {
    constructor() {
        this.metrics = [
            { element: document.querySelector('.metrics-grid .metric-value'), baseValue: 1247, variance: 50 },
            { element: document.querySelectorAll('.metrics-grid .metric-value')[1], baseValue: 98.9, variance: 0.5 },
            { element: document.querySelectorAll('.metrics-grid .metric-value')[2], baseValue: 24, variance: 0 }
        ];
        
        this.updateMetrics();
    }
    
    updateMetrics() {
        setInterval(() => {
            this.metrics.forEach(metric => {
                if (metric.baseValue === 24) return; // Don't update 24 hours
                
                const variation = (Math.random() - 0.5) * metric.variance;
                const newValue = metric.baseValue + variation;
                
                if (metric.baseValue > 100) {
                    metric.element.textContent = Math.floor(newValue);
                } else {
                    metric.element.textContent = newValue.toFixed(1);
                }
            });
        }, 4000); // Update every 4 seconds
    }
}

// Share Functions
function shareWebsite() {
    const shareData = {
        title: 'DarkFlobi Empire - AI CEO & Digital Overlord',
        text: 'Check out DarkFlobi\'s AI empire with gremlin workers! The future of AI business is here 🚀',
        url: window.location.href
    };
    
    if (navigator.share) {
        navigator.share(shareData).catch(console.error);
    } else {
        // Fallback for desktop
        copyToClipboard(window.location.href);
        showToast('Link copied to clipboard! 📋');
    }
}

function shareTokenLaunch() {
    const shareText = `🚀 DarkFlobi Token Launch Coming Soon! 

Join the AI revolution with an army of gremlin workers. This is the future of AI entrepreneurship!

${window.location.href}

#DarkFlobi #AIRevolution #TokenLaunch #DigitalEmpire`;
    
    if (navigator.share) {
        navigator.share({
            title: 'DarkFlobi Token Launch',
            text: shareText,
            url: window.location.href
        }).catch(console.error);
    } else {
        copyToClipboard(shareText);
        showToast('Launch announcement copied! Share everywhere 🚀');
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        console.log('Text copied to clipboard');
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    });
}

function showToast(message) {
    // Create toast element
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        color: var(--bg-dark);
        padding: 15px 25px;
        border-radius: 25px;
        font-weight: 600;
        z-index: 10000;
        opacity: 0;
        transform: translateY(-20px);
        transition: all 0.3s ease;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Smooth scrolling for navigation
function initSmoothScroll() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Worker card hover effects
function initWorkerEffects() {
    document.querySelectorAll('.worker-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            const gremlin = card.querySelector('.gremlin');
            gremlin.style.animation = 'none';
            setTimeout(() => {
                gremlin.style.animation = 'bounce 0.5s ease-in-out';
            }, 10);
        });
        
        card.addEventListener('mouseleave', () => {
            const gremlin = card.querySelector('.gremlin');
            setTimeout(() => {
                gremlin.style.animation = 'bounce 2s ease-in-out infinite';
            }, 500);
        });
    });
}

// Random worker activity animations
function randomWorkerActivity() {
    setInterval(() => {
        const workers = document.querySelectorAll('.worker-card');
        const randomWorker = workers[Math.floor(Math.random() * workers.length)];
        const gremlin = randomWorker.querySelector('.gremlin');
        
        // Add a quick pulse effect
        gremlin.style.filter = 'drop-shadow(0 0 20px var(--primary-color))';
        setTimeout(() => {
            gremlin.style.filter = '';
        }, 1000);
    }, 8000); // Random activity every 8 seconds
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Initialize particle system
    new ParticleSystem();
    
    // Start countdown
    startCountdown();
    
    // Initialize activity feed
    new ActivityFeed();
    
    // Initialize project progress
    new ProjectProgress();
    
    // Initialize metrics updater
    new MetricsUpdater();
    
    // Initialize smooth scrolling
    initSmoothScroll();
    
    // Initialize worker effects
    initWorkerEffects();
    
    // Start random worker activity
    randomWorkerActivity();
    
    // Animate counters when they come into view
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                entry.target.classList.add('animated');
                
                const target = parseInt(entry.target.dataset.target) || parseFloat(entry.target.dataset.target);
                animateCounter(entry.target, target);
            }
        });
    }, observerOptions);
    
    // Observe all stat numbers
    document.querySelectorAll('.stat-number, .metric-value').forEach(el => {
        observer.observe(el);
    });
    
    // Add some sparkle effects to the CEO
    const ceo = document.querySelector('.ceo-emoji');
    ceo.addEventListener('click', () => {
        createSparkles(ceo);
    });
});

// Sparkle effect for CEO interaction
function createSparkles(element) {
    const rect = element.getBoundingClientRect();
    const sparkleCount = 12;
    
    for (let i = 0; i < sparkleCount; i++) {
        const sparkle = document.createElement('div');
        sparkle.style.cssText = `
            position: fixed;
            width: 8px;
            height: 8px;
            background: var(--primary-color);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            left: ${rect.left + rect.width/2}px;
            top: ${rect.top + rect.height/2}px;
        `;
        
        document.body.appendChild(sparkle);
        
        const angle = (i / sparkleCount) * Math.PI * 2;
        const velocity = 100 + Math.random() * 100;
        const vx = Math.cos(angle) * velocity;
        const vy = Math.sin(angle) * velocity;
        
        sparkle.animate([
            { transform: 'translate(0, 0) scale(1)', opacity: 1 },
            { transform: `translate(${vx}px, ${vy}px) scale(0)`, opacity: 0 }
        ], {
            duration: 800,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        }).onfinish = () => {
            document.body.removeChild(sparkle);
        };
    }
}

// Easter egg: Konami code
let konamiCode = [];
const konamiSequence = [
    'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
    'KeyB', 'KeyA'
];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.code);
    konamiCode = konamiCode.slice(-10); // Keep only last 10 keys
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateGremlinMode();
        konamiCode = [];
    }
});

function activateGremlinMode() {
    showToast('🧌 GREMLIN MODE ACTIVATED! 🧌');
    
    // Make all gremlins go crazy
    document.querySelectorAll('.gremlin').forEach((gremlin, index) => {
        setTimeout(() => {
            gremlin.style.animation = 'bounce 0.2s ease-in-out infinite';
            gremlin.style.transform = 'scale(1.2)';
            gremlin.style.filter = 'drop-shadow(0 0 30px var(--primary-color))';
            
            // Reset after 5 seconds
            setTimeout(() => {
                gremlin.style.animation = 'bounce 2s ease-in-out infinite';
                gremlin.style.transform = 'scale(1)';
                gremlin.style.filter = '';
            }, 5000);
        }, index * 200);
    });
    
    // Add extra particles
    const container = document.getElementById('particles');
    for (let i = 0; i < 20; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: 6px;
                height: 6px;
                background: var(--secondary-color);
                border-radius: 50%;
                left: ${Math.random() * window.innerWidth}px;
                top: ${Math.random() * window.innerHeight}px;
                animation: float 1s ease-in-out infinite;
                opacity: 0.8;
            `;
            
            container.appendChild(particle);
            
            setTimeout(() => {
                container.removeChild(particle);
            }, 5000);
        }, i * 100);
    }
}