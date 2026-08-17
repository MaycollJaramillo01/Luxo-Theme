(() => {
  const normalizePath = (pathname) => pathname.replace(/\/+$/, '') || '/';

  const markCurrentLinks = (header) => {
    const currentPath = normalizePath(window.location.pathname);

    header.querySelectorAll('a[href]').forEach((link) => {
      let url;

      try {
        url = new URL(link.href, window.location.origin);
      } catch (_error) {
        return;
      }

      if (url.origin !== window.location.origin || normalizePath(url.pathname) !== currentPath) return;

      link.setAttribute('aria-current', 'page');
      if (link.classList.contains('luxo-header__link')) link.classList.add('is-active');
    });
  };

  const initHeader = (header) => {
    if (!header || header.dataset.luxoReady === 'true') return;
    header.dataset.luxoReady = 'true';

    markCurrentLinks(header);

    const menu = header.querySelector('.luxo-mobile-menu');
    const toggle = menu?.querySelector(':scope > summary');

    if (!menu || !toggle) return;

    const syncMenuState = () => {
      const isOpen = menu.open;
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.setAttribute('aria-label', isOpen ? 'Cerrar menú' : 'Abrir menú');
      document.body.classList.toggle('luxo-menu-open', isOpen);
    };

    const closeMenu = ({ restoreFocus = false } = {}) => {
      if (!menu.open) return;
      menu.open = false;
      syncMenuState();
      if (restoreFocus) toggle.focus();
    };

    menu.addEventListener('toggle', syncMenuState);
    menu.querySelectorAll('.luxo-mobile-menu__panel a').forEach((link) => {
      link.addEventListener('click', () => closeMenu());
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menu.open) {
        event.preventDefault();
        closeMenu({ restoreFocus: true });
      }
    });

    window.matchMedia('(min-width: 900px)').addEventListener('change', (event) => {
      if (event.matches) closeMenu();
    });

    syncMenuState();
  };

  const init = (root = document) => {
    root.querySelectorAll('[data-luxo-header]').forEach(initHeader);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => init());
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', (event) => init(event.target));
})();
