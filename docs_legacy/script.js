// Language Toggle Logic
function toggleLanguage() {
    const body = document.body;
    const currentLang = body.classList.contains('lang-pt') ? 'pt' : 'en';
    
    if (currentLang === 'pt') {
        body.classList.remove('lang-pt');
        body.classList.add('lang-en');
        localStorage.setItem('pspFreeShop-lang', 'en');
        document.documentElement.lang = 'en';
    } else {
        body.classList.remove('lang-en');
        body.classList.add('lang-pt');
        localStorage.setItem('pspFreeShop-lang', 'pt');
        document.documentElement.lang = 'pt-br';
    }
}

// Persist Language Preference
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('pspFreeShop-lang');
    if (savedLang === 'en') {
        document.body.classList.remove('lang-pt');
        document.body.classList.add('lang-en');
        document.documentElement.lang = 'en';
    }
});

// Scroll Reveal Animation
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Vanilla Tilt 3D Effect
function initTiltEffect() {
    const tiltElements = document.querySelectorAll('.tilt-element');
    
    tiltElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within the element
            const y = e.clientY - rect.top;  // y position within the element
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Max rotation 10 degrees, reduce denominator to increase tilt
            const tiltX = (y - centerY) / centerY * -8;
            const tiltY = (x - centerX) / centerX * 8;
            
            el.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        el.addEventListener('mouseleave', () => {
            el.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        });
    });
}

// Initialize Animations and Effects
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.animate-up');
    animatedElements.forEach(el => observer.observe(el));
    
    // Initialize 3D Tilt Array
    initTiltEffect();
});

// Subtle Parallax for BG Symbols and Dynamic Blob Movement on Mouse
document.addEventListener('mousemove', (e) => {
    const symbols = document.querySelector('.bg-symbols');
    const blob1 = document.querySelector('.blob-1');
    const blob2 = document.querySelector('.blob-2');
    
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    if (symbols) {
        symbols.style.transform = `translate(${x * 20}px, ${y * 20}px)`;
    }
    
    // Move blobs slightly away from mouse
    if (blob1) {
        blob1.style.transform = `translate(${x * -40}px, ${y * -40}px) scale(1.05)`;
    }
    if (blob2) {
        blob2.style.transform = `translate(${x * 30}px, ${y * 30}px) scale(0.95)`;
    }
});

// Glass Nav Scroll Effect
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.glass-nav');
    if (window.scrollY > 50) {
        nav.style.padding = '0.5rem 0';
        nav.style.background = 'rgba(10, 5, 20, 0.7)';
        nav.style.boxShadow = '0 10px 30px rgba(0,0,0,0.5), inset 0 -1px 0 rgba(255,255,255,0.05)';
    } else {
        nav.style.padding = '0';
        nav.style.background = 'rgba(15, 10, 25, 0.4)';
        nav.style.boxShadow = 'inset 0 -1px 0 rgba(255, 255, 255, 0.05)';
    }
});
