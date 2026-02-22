export class Navbar extends HTMLElement {
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
        <button class="md:hidden text-white">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </nav>
      <!-- Spacer to prevent content from hiding behind fixed nav -->
      <div class="h-20"></div>
    `;
  }
}

customElements.define('app-navbar', Navbar);
