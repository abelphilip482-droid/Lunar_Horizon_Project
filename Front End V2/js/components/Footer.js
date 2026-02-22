export class Footer extends HTMLElement {
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

customElements.define('app-footer', Footer);
