/**
 * Base Pages JS - Hero Page Mode functionality
 * Digər səhifələr üçün scroll və layout idarəetməsi
 */

(function() {
  'use strict';

  // ====================================
  // VARIABLES & CONSTANTS
  // ====================================
  
  let headerHeight = 72; // default
  let isHeroPageMode = false;
  let scrollContainer = null;

  // ====================================
  // UTILITY FUNCTIONS
  // ====================================

  /**
   * Header hündürlüyünü dinamik hesabla və CSS variable-a təyin et
   */
  function setHeaderHeightVar() {
    const header = document.querySelector('.floating-header');
    if (header) {
      headerHeight = header.getBoundingClientRect().height;
      document.documentElement.style.setProperty('--header-height', `${Math.round(headerHeight)}px`);
    }
  }

  /**
   * Body scroll-u kilid və hero page mode-u aktivləşdir
   */
  function enableHeroPageMode() {
    if (document.body.classList.contains('hero-page-mode')) {
      isHeroPageMode = true;
      
      // Body scroll kilidlə
      document.documentElement.style.overflow = 'hidden';
      document.body.style.overflow = 'hidden';
      document.body.style.position = 'fixed';
      document.body.style.width = '100%';
      document.body.style.height = '100vh';
      
      // Scroll container-i tap
      scrollContainer = document.querySelector('.hero-scroll-container');
      
      console.log('🎯 Hero Page Mode activated');
    }
  }

  // Legacy pages-mode removed
  function enableLegacyPagesMode() {}

  /**
   * Anchor linklər üçün smooth scroll (hero container daxilində)
   */
  function initInHeroAnchors() {
    if (!scrollContainer) return;

    document.addEventListener('click', (e) => {
      const anchor = e.target.closest('a[href^="#"]');
      if (!anchor) return;

      const href = anchor.getAttribute('href');
      if (href === '#') return;

      const targetId = href.slice(1);
      const target = document.getElementById(targetId);
      
      if (target) {
        e.preventDefault();
        
        // Target element-in scroll container daxilindəki mövqeyini hesabla
        const containerRect = scrollContainer.getBoundingClientRect();
        const targetRect = target.getBoundingClientRect();
        const offsetTop = targetRect.top - containerRect.top + scrollContainer.scrollTop - 20;
        
        scrollContainer.scrollTo({
          top: Math.max(0, offsetTop),
          behavior: 'smooth'
        });
        
        console.log(`🔗 Smooth scroll to: ${targetId}`);
      }
    });
  }

  /**
   * Scroll container üçün custom scroll events
   */
  function initScrollEvents() {
    if (!scrollContainer) return;

    let scrollTimeout;
    
    scrollContainer.addEventListener('scroll', () => {
      // Scroll zamanı header-ə class əlavə et
      if (scrollContainer.scrollTop > 50) {
        document.querySelector('.floating-header')?.classList.add('scrolled');
      } else {
        document.querySelector('.floating-header')?.classList.remove('scrolled');
      }
      
      // Scroll bitdikdə event fire et
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const event = new CustomEvent('heroScrollEnd', {
          detail: { scrollTop: scrollContainer.scrollTop }
        });
        document.dispatchEvent(event);
      }, 150);
    });

    // Scroll to top button functionality
    const scrollToTopBtn = document.querySelector('.scroll-to-top');
    if (scrollToTopBtn) {
      scrollToTopBtn.addEventListener('click', () => {
        scrollContainer.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }
  }

  /**
   * Keyboard navigation dəstəyi
   */
  function initKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      if (!isHeroPageMode || !scrollContainer) return;

      switch (e.key) {
        case 'Home':
          if (e.ctrlKey) {
            e.preventDefault();
            scrollContainer.scrollTo({ top: 0, behavior: 'smooth' });
          }
          break;
        case 'End':
          if (e.ctrlKey) {
            e.preventDefault();
            scrollContainer.scrollTo({ 
              top: scrollContainer.scrollHeight, 
              behavior: 'smooth' 
            });
          }
          break;
        case 'PageUp':
          e.preventDefault();
          scrollContainer.scrollBy({ 
            top: -scrollContainer.clientHeight * 0.8, 
            behavior: 'smooth' 
          });
          break;
        case 'PageDown':
          e.preventDefault();
          scrollContainer.scrollBy({ 
            top: scrollContainer.clientHeight * 0.8, 
            behavior: 'smooth' 
          });
          break;
      }
    });
  }

  /**
   * Resize events - responsive behavior
   */
  function initResizeHandler() {
    let resizeTimeout;
    
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        setHeaderHeightVar();
        
        // Mobile orientation change handling
        if (isHeroPageMode) {
          const vh = window.innerHeight * 0.01;
          document.documentElement.style.setProperty('--vh', `${vh}px`);
        }
        
        console.log('📱 Resize handled');
      }, 100);
    });
  }

  /**
   * Performance optimization - lazy loading
   */
  function initLazyLoading() {
    if (!scrollContainer) return;

    const lazyElements = scrollContainer.querySelectorAll('[data-lazy]');
    if (lazyElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const element = entry.target;
          const src = element.dataset.lazy;
          
          if (element.tagName === 'IMG') {
            element.src = src;
          } else {
            element.style.backgroundImage = `url(${src})`;
          }
          
          element.removeAttribute('data-lazy');
          observer.unobserve(element);
        }
      });
    }, {
      root: scrollContainer,
      rootMargin: '50px'
    });

    lazyElements.forEach(el => observer.observe(el));
  }

  // ====================================
  // INITIALIZATION
  // ====================================

  /**
   * Əsas initialization function
   */
  function init() {
    console.log('🚀 Base Pages JS initializing...');
    
    // Header height hesabla
    setHeaderHeightVar();
    
    // Page mode-u müəyyən et və aktivləşdir
    enableHeroPageMode();
    enableLegacyPagesMode();
    
    // Funksionallıqları aktivləşdir
    initInHeroAnchors();
    initScrollEvents();
    initKeyboardNavigation();
    initResizeHandler();
    initLazyLoading();
    
    // Mobile viewport height fix
    if (isHeroPageMode) {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    console.log('✅ Base Pages JS ready');
  }

  // ====================================
  // EVENT LISTENERS
  // ====================================

  // DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Page visibility change
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && isHeroPageMode) {
      // Page visible olduqda header height-i yenidən hesabla
      setTimeout(setHeaderHeightVar, 100);
    }
  });

  // ====================================
  // PUBLIC API
  // ====================================

  // Global object üçün API
  window.dropAzHeroPages = {
    scrollToTop: () => {
      if (scrollContainer) {
        scrollContainer.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },
    scrollToElement: (selector) => {
      if (!scrollContainer) return;
      const element = document.querySelector(selector);
      if (element) {
        const containerRect = scrollContainer.getBoundingClientRect();
        const elementRect = element.getBoundingClientRect();
        const offsetTop = elementRect.top - containerRect.top + scrollContainer.scrollTop - 20;
        
        scrollContainer.scrollTo({
          top: Math.max(0, offsetTop),
          behavior: 'smooth'
        });
      }
    },
    getScrollPosition: () => {
      return scrollContainer ? scrollContainer.scrollTop : 0;
    },
    isHeroMode: () => isHeroPageMode
  };

})();
