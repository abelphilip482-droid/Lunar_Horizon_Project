/* 
   Main JavaScript Entry Point
   Consolidated to include components directly to avoid module loading issues on local file:// protocol 
*/

// --- Components ---

class Navbar extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.render();
    }

    render() {
        const activePage = this.getAttribute('active') || 'home';

        // Helper to conditionally set active class
        const isActive = (page) => activePage === page ? 'text-blue-400 font-semibold' : 'text-gray-300 hover:text-blue-400 hover:glow-text transition-all duration-300';

        this.innerHTML = `
      <nav class="glass-nav fixed top-0 w-full z-50 px-6 py-4 flex justify-between items-center transition-all duration-300">
        <a href="index.html" class="flex items-center gap-3 group">
          <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-cyan-400 shadow-[0_0_15px_rgba(96,165,250,0.6)] group-hover:scale-110 transition-transform duration-300"></div>
          <h1 class="font-['Orbitron'] text-lg tracking-wide group-hover:text-blue-300 transition-colors">
            Lunar Horizon <span class="text-blue-400">Mapper</span>
          </h1>
        </a>

        <ul class="flex gap-4 md:gap-8 font-['Inter'] text-sm tracking-wide">
          <li><a href="index.html" class="${isActive('home')}">Home</a></li>
          <li><a href="calculator.html" class="${isActive('calculator')}">Calculator</a></li>
          <li><a href="rover.html" class="${isActive('rover')}">Rover</a></li>
          <li><a href="about.html" class="${isActive('about')}">About</a></li>
        </ul>

        <!-- Mobile Menu Button (Placeholder for future implementation) -->
        <button class="md:hidden text-white" aria-label="Menu">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </nav>
      <!-- Spacer to prevent content from hiding behind fixed nav -->
      <div class="h-20"></div>
    `;
    }
}

class Footer extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.render();
    }

    render() {
        this.innerHTML = `
      <footer class="glass-panel mt-auto py-8 text-center border-t border-gray-800">
        <div class="max-w-6xl mx-auto px-6">
          <p class="text-gray-500 text-sm font-light">
            © 2026 Lunar Horizon Mapper — <span class="text-blue-400">Front-end Prototype</span>
          </p>
          <div class="flex justify-center gap-4 mt-4 text-xs text-gray-600">
             <a href="#" class="hover:text-blue-400 transition-colors">Privacy</a>
             <span class="text-gray-800">|</span>
             <a href="#" class="hover:text-blue-400 transition-colors">Documentation</a>
          </div>
        </div>
      </footer>
    `;
    }
}

// Define Custom Elements safely
if (!customElements.get('app-navbar')) {
    customElements.define('app-navbar', Navbar);
}
if (!customElements.get('app-footer')) {
    customElements.define('app-footer', Footer);
}

// --- Global Logic & Animations ---

document.addEventListener('DOMContentLoaded', () => {
    // Reveal Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-on-scroll').forEach(el => {
        el.style.opacity = '0'; // Initial state ensuring elements are hidden before animation
        observer.observe(el);
    });
});
