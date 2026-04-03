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
            // Stop observing once visible
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Initialize Animations
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.animate-up');
    animatedElements.forEach(el => observer.observe(el));
});

// Subtle Parallax for BG Symbols
document.addEventListener('mousemove', (e) => {
    const symbols = document.querySelector('.bg-symbols');
    if (!symbols) return;
    
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    symbols.style.transform = `translate(${x * 15}px, ${y * 15}px)`;
});

// Glass Nav Scroll Effect
window.addEventListener('scroll', () => {
    const nav = document.querySelector('.glass-nav');
    if (window.scrollY > 50) {
        nav.style.padding = '0.5rem 0';
        nav.style.boxShadow = '0 10px 30px rgba(0,0,0,0.3)';
    } else {
        nav.style.padding = '0';
        nav.style.boxShadow = 'none';
    }
});
