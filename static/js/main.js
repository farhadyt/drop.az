// =================================
// ENHANCED JAVASCRIPT FOR DROP.AZ PLATFORM
// Ultra Fast, Performance Optimized & Clean
// =================================

// =================================
// GLOBAL VARIABLES & CONSTANTS
// =================================
let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
let favoriteItems = JSON.parse(localStorage.getItem('favoriteItems')) || [];
let recentSearches = JSON.parse(localStorage.getItem('recentSearches')) || [];

// State management
const appState = {
    isSearchOpen: false,
    isMobileMenuOpen: false,
    isAccountMenuOpen: false,
    isLoading: true
};

// Performance optimizations
let scrollTimeout;
let resizeTimeout;
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };

// =================================
// MAIN APP INITIALIZATION
// =================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 drop.az platform initializing...');
    
    // Initialize all core modules
    initializeApp();
    
    console.log('✅ drop.az platform ready!');
});

// =================================
// CORE APP INITIALIZATION
// =================================
function initializeApp() {
    // Initialize loading screen first
    initializeLoadingScreen();
    
    // Initialize core components
    initializeHeader();
    initializeMobileMenu();
    initializeSearch();
    initializeCart();
    initializeFavorites();
    initializeAccountMenu();
    initializeScrollEffects();
    initializeBackToTop();
    initializeNewsletter();
    initializeProductInteractions();
    initializeProductFilters();
    
    // Update UI
    updateCartCounter();
    updateFavoritesCounter();
    updateRecentSearches();
    
    // Initialize performance monitoring
    initializePerformanceMonitoring();
}

// =================================
// LOADING SCREEN - FAST
// =================================
function initializeLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (!loadingScreen) return;
    
    // Fast loading simulation
    setTimeout(() => {
        loadingScreen.classList.add('hidden');
        appState.isLoading = false;
        
        // Remove from DOM after transition
        setTimeout(() => {
            loadingScreen?.remove();
            document.body.classList.add('loaded');
        }, 500);
    }, 800); // Reduced from 1200ms
}

// =================================
// HEADER FUNCTIONALITY - OPTIMIZED
// =================================
function initializeHeader() {
    const header = document.querySelector('.floating-header');
    if (!header) return;

    let lastScrollTop = 0;
    let ticking = false;

    function updateHeader() {
        const scrollTop = window.pageYOffset;
        
        // Add/remove scrolled class
        header.classList.toggle('scrolled', scrollTop > 30);
        
        lastScrollTop = scrollTop;
        ticking = false;
    }

    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(updateHeader);
            ticking = true;
        }
    }

    // Throttled scroll event
    window.addEventListener('scroll', onScroll, { passive: true });
    
    // Initial call
    updateHeader();
}

// =================================
// MOBILE MENU - SIMPLIFIED
// =================================
function initializeMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-nav-menu');
    const mobileClose = document.querySelector('.mobile-nav-close');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    
    if (!mobileToggle || !mobileMenu) return;

    function toggleMobileMenu() {
        appState.isMobileMenuOpen = !appState.isMobileMenuOpen;
        
        mobileMenu.classList.toggle('active', appState.isMobileMenuOpen);
        mobileToggle.classList.toggle('active', appState.isMobileMenuOpen);
        document.body.style.overflow = appState.isMobileMenuOpen ? 'hidden' : '';
    }

    function closeMobileMenu() {
        appState.isMobileMenuOpen = false;
        mobileMenu.classList.remove('active');
        mobileToggle.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Event listeners
    mobileToggle.addEventListener('click', toggleMobileMenu);
    mobileClose?.addEventListener('click', closeMobileMenu);

    // Close menu when clicking on links
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && appState.isMobileMenuOpen) {
            closeMobileMenu();
        }
    });

    // Close menu on window resize (desktop)
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (window.innerWidth > 768 && appState.isMobileMenuOpen) {
                closeMobileMenu();
            }
        }, 100);
    });
}

// =================================
// ACCOUNT MENU - FAST
// =================================
function initializeAccountMenu() {
    const accountToggle = document.querySelector('.account-toggle');
    const accountDropdown = document.querySelector('.account-dropdown');
    
    if (!accountToggle || !accountDropdown) return;

    function toggleAccountMenu(e) {
        e.stopPropagation();
        appState.isAccountMenuOpen = !appState.isAccountMenuOpen;
        accountDropdown.classList.toggle('active', appState.isAccountMenuOpen);
    }

    function closeAccountMenu() {
        appState.isAccountMenuOpen = false;
        accountDropdown.classList.remove('active');
    }

    // Event listeners
    accountToggle.addEventListener('click', toggleAccountMenu);
    
    // Close when clicking outside
    document.addEventListener('click', (e) => {
        if (appState.isAccountMenuOpen && !accountDropdown.contains(e.target)) {
            closeAccountMenu();
        }
    });

    // Close on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && appState.isAccountMenuOpen) {
            closeAccountMenu();
        }
    });
}

// =================================
// SEARCH FUNCTIONALITY - OPTIMIZED
// =================================
function initializeSearch() {
    const searchToggle = document.querySelector('.search-toggle');
    const searchOverlay = document.querySelector('.search-overlay');
    const searchClose = document.querySelector('.search-close');
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');
    const suggestionTags = document.querySelectorAll('.suggestion-tag');

    if (!searchToggle || !searchOverlay) return;

    function openSearch() {
        appState.isSearchOpen = true;
        searchOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus on input with delay
        setTimeout(() => searchInput?.focus(), 200);
    }

    function closeSearch() {
        appState.isSearchOpen = false;
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
        
        // Clear search input
        if (searchInput) searchInput.value = '';
    }

    function performSearch(query) {
        if (!query.trim()) return;
        
        console.log('Searching for:', query);
        
        // Add to recent searches
        addToRecentSearches(query);
        
        showNotification(`"${query}" üçün axtarış edilir...`, 'info');
        
        // Simulate search
        setTimeout(() => {
            const resultCount = Math.floor(Math.random() * 50) + 1;
            showNotification(`"${query}" üçün ${resultCount} nəticə tapıldı!`, 'success');
        }, 800);
        
        closeSearch();
    }

    function addToRecentSearches(query) {
        // Remove if already exists
        recentSearches = recentSearches.filter(search => search !== query);
        // Add to beginning
        recentSearches.unshift(query);
        // Keep only last 5 searches
        recentSearches = recentSearches.slice(0, 5);
        localStorage.setItem('recentSearches', JSON.stringify(recentSearches));
        updateRecentSearches();
    }

    // Event listeners
    searchToggle.addEventListener('click', (e) => {
        e.preventDefault();
        openSearch();
    });

    searchClose?.addEventListener('click', closeSearch);

    // Close search on overlay click
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) closeSearch();
    });

    // Search form submission
    searchForm?.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = searchInput?.value || '';
        performSearch(query);
    });

    // Suggestion tags
    suggestionTags.forEach(tag => {
        tag.addEventListener('click', () => {
            const query = tag.textContent;
            if (searchInput) searchInput.value = query;
            performSearch(query);
        });
    });

    // Real-time search suggestions (debounced)
    if (searchInput) {
        searchInput.addEventListener('input', debounce((e) => {
            const query = e.target.value;
            if (query.length > 2) {
                console.log('Getting suggestions for:', query);
            }
        }, 300));
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Open search with Ctrl+K or Cmd+K
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            openSearch();
        }
        
        // Close search with Escape
        if (e.key === 'Escape' && appState.isSearchOpen) {
            closeSearch();
        }
    });
}

function updateRecentSearches() {
    const recentContainer = document.querySelector('.recent-searches');
    if (!recentContainer) return;
    
    recentContainer.innerHTML = '';
    
    if (recentSearches.length === 0) {
        recentContainer.innerHTML = '<p class="no-recent">Son axtarışınız yoxdur</p>';
        return;
    }
    
    recentSearches.forEach(search => {
        const searchItem = document.createElement('span');
        searchItem.className = 'recent-search-item';
        searchItem.textContent = search;
        searchItem.addEventListener('click', () => {
            const searchInput = document.querySelector('.search-input');
            if (searchInput) searchInput.value = search;
            performSearch(search);
        });
        recentContainer.appendChild(searchItem);
    });
}

// =================================
// CART FUNCTIONALITY - EFFICIENT
// =================================
function initializeCart() {
    const cartLink = document.querySelector('.cart-link');
    
    if (!cartLink) return;

    cartLink.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Add click animation
        cartLink.style.transform = 'scale(0.95)';
        setTimeout(() => {
            cartLink.style.transform = 'scale(1)';
        }, 100);
        
        // Show cart
        if (cartItems.length === 0) {
            showNotification('Səbətiniz boşdur', 'info');
        } else {
            showNotification(`Səbətdə ${getTotalCartItems()} məhsul var`, 'success');
        }
    });
}

function addToCart(productId) {
    // Check if product already exists in cart
    const existingItem = cartItems.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
        showNotification('Məhsulun sayı artırıldı! 📈', 'success');
    } else {
        const newItem = {
            id: productId,
            quantity: 1,
            addedAt: new Date().toISOString()
        };
        cartItems.push(newItem);
        showNotification('Məhsul səbətə əlavə edildi! 🛒', 'success');
    }
    
    // Save to localStorage
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    
    // Update counter with animation
    updateCartCounter();
    animateCartIcon();
}

function removeFromCart(productId) {
    const initialLength = cartItems.length;
    cartItems = cartItems.filter(item => item.id !== productId);
    
    if (cartItems.length < initialLength) {
        localStorage.setItem('cartItems', JSON.stringify(cartItems));
        updateCartCounter();
        showNotification('Məhsul səbətdən silindi', 'info');
    }
}

function updateCartCounter() {
    const cartCount = document.querySelector('.cart-count');
    if (!cartCount) return;
    
    const totalItems = getTotalCartItems();
    cartCount.textContent = totalItems;
    cartCount.classList.toggle('active', totalItems > 0);
}

function getTotalCartItems() {
    return cartItems.reduce((sum, item) => sum + item.quantity, 0);
}

function animateCartIcon() {
    const cartLink = document.querySelector('.cart-link');
    if (!cartLink) return;
    
    cartLink.style.animation = 'none';
    cartLink.offsetHeight; // Trigger reflow
    cartLink.style.animation = 'cartBounce 0.4s ease';
    
    setTimeout(() => {
        cartLink.style.animation = '';
    }, 400);
}

// =================================
// FAVORITES FUNCTIONALITY - FAST
// =================================
function initializeFavorites() {
    const favoritesLink = document.querySelector('.favorites-link');
    
    if (!favoritesLink) return;

    favoritesLink.addEventListener('click', (e) => {
        e.preventDefault();
        
        if (favoriteItems.length === 0) {
            showNotification('Sevimlilər siyahınız boşdur 💙', 'info');
        } else {
            showNotification(`${favoriteItems.length} sevimli məhsul var 💙`, 'success');
        }
    });
}

function toggleFavorite(productId) {
    const existingIndex = favoriteItems.findIndex(item => item.id === productId);
    
    if (existingIndex > -1) {
        // Remove from favorites
        favoriteItems.splice(existingIndex, 1);
        showNotification('Məhsul sevimlilərdən silindi 💔', 'info');
        
        // Update button state
        const favoriteBtn = document.querySelector(`[data-product-id="${productId}"].favorite-btn`);
        favoriteBtn?.classList.remove('active');
    } else {
        // Add to favorites
        const newFavorite = {
            id: productId,
            addedAt: new Date().toISOString()
        };
        favoriteItems.push(newFavorite);
        showNotification('Məhsul sevimlilərə əlavə edildi! 💙', 'success');
        
        // Update button state
        const favoriteBtn = document.querySelector(`[data-product-id="${productId}"].favorite-btn`);
        if (favoriteBtn) {
            favoriteBtn.classList.add('active');
            animateFavoriteIcon(favoriteBtn);
        }
    }
    
    // Save to localStorage
    localStorage.setItem('favoriteItems', JSON.stringify(favoriteItems));
    
    // Update counter
    updateFavoritesCounter();
}

function updateFavoritesCounter() {
    const favoritesCount = document.querySelector('.favorites-count');
    if (!favoritesCount) return;
    
    const totalFavorites = favoriteItems.length;
    favoritesCount.textContent = totalFavorites;
    favoritesCount.classList.toggle('active', totalFavorites > 0);
}

function animateFavoriteIcon(button) {
    button.style.animation = 'heartBeat 0.6s ease';
    setTimeout(() => {
        button.style.animation = '';
    }, 600);
}

// =================================
// PRODUCT INTERACTIONS - OPTIMIZED
// =================================
function initializeProductInteractions() {
    // Use event delegation for better performance
    document.addEventListener('click', (e) => {
        const target = e.target.closest('[data-product-id]');
        if (!target) return;
        
        const productId = parseInt(target.getAttribute('data-product-id'));
        
        if (target.classList.contains('add-to-cart-btn')) {
            e.preventDefault();
            addToCart(productId);
        } else if (target.classList.contains('favorite-btn')) {
            e.preventDefault();
            toggleFavorite(productId);
        } else if (target.classList.contains('quick-view-btn')) {
            e.preventDefault();
            quickView(productId);
        } else if (target.classList.contains('share-btn')) {
            e.preventDefault();
            shareProduct(productId);
        }
    });

    // Initialize favorite button states
    document.querySelectorAll('.favorite-btn').forEach(button => {
        const productId = parseInt(button.getAttribute('data-product-id'));
        const isFavorite = favoriteItems.some(item => item.id === productId);
        button.classList.toggle('active', isFavorite);
    });

    // Load more button
    const loadMoreBtn = document.querySelector('.load-more-btn');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<div class="spinner-small"></div> Yüklənir...';
            
            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = 'Daha çox məhsul yüklə';
                showNotification('Daha çox məhsul yükləndi! 📦', 'success');
            }, 1500);
        });
    }
}

function quickView(productId) {
    console.log('Quick view for product:', productId);
    showNotification('Məhsul haqqında ətraflı məlumat yüklənir... 👀', 'info');
    
    setTimeout(() => {
        showNotification('Tez baxış funksiyası tezliklə əlavə ediləcək! 🔜', 'info');
    }, 1000);
}

function shareProduct(productId) {
    const productName = `Məhsul #${productId}`;
    const shareData = {
        title: `${productName} - drop.az`,
        text: `Bu məhsula baxın: ${productName}`,
        url: `${window.location.origin}#product-${productId}`
    };

    if (navigator.share) {
        navigator.share(shareData)
            .then(() => showNotification('Məhsul paylaşıldı! 📤', 'success'))
            .catch(() => showNotification('Paylaşma xətası baş verdi', 'error'));
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(shareData.url)
            .then(() => showNotification('Link panoya kopyalandı! 📋', 'success'))
            .catch(() => showNotification('Kopyalama xətası', 'error'));
    }
}

// =================================
// PRODUCT FILTERS - FAST
// =================================
function initializeProductFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const productCards = document.querySelectorAll('.product-card');

    if (filterBtns.length === 0) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active class from all buttons
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');

            const filter = this.getAttribute('data-filter');
            
            let visibleCount = 0;
            
            productCards.forEach(card => {
                const category = card.getAttribute('data-category');
                const shouldShow = filter === 'all' || category === filter;
                
                if (shouldShow) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Show notification
            showNotification(`${visibleCount} məhsul göstərilir`, 'info');
        });
    });
}

// =================================
// SCROLL EFFECTS - MINIMAL
// =================================
function initializeScrollEffects() {
    // Simple intersection observer for fade-in effects
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.product-card, .feature-card, .stat-item');
    animateElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

// =================================
// BACK TO TOP - SIMPLE
// =================================
function initializeBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;

    let ticking = false;

    function toggleBackToTop() {
        backToTopBtn.classList.toggle('visible', window.pageYOffset > 300);
        ticking = false;
    }

    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    // Throttled scroll event
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(toggleBackToTop);
            ticking = true;
        }
    }, { passive: true });
    
    // Click event
    backToTopBtn.addEventListener('click', scrollToTop);
}

// =================================
// NEWSLETTER - OPTIMIZED
// =================================
function initializeNewsletter() {
    const newsletterForm = document.querySelector('.newsletter-form');
    const newsletterInput = document.querySelector('.newsletter-input');
    const newsletterBtn = document.querySelector('.newsletter-btn');
    
    if (!newsletterForm) return;

    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const email = newsletterInput.value.trim();
        
        if (!email) {
            showNotification('E-mail ünvanını daxil edin', 'warning');
            newsletterInput.focus();
            return;
        }
        
        if (!isValidEmail(email)) {
            showNotification('Düzgün e-mail ünvanı daxil edin', 'warning');
            newsletterInput.focus();
            return;
        }
        
        // Disable button and show loading
        newsletterBtn.disabled = true;
        newsletterBtn.innerHTML = '<div class="spinner-small"></div> Göndərilir...';
        
        // Simulate API call
        setTimeout(() => {
            showNotification('Uğurla abunə oldunuz! 🎉📧', 'success');
            newsletterInput.value = '';
            
            // Reset button
            newsletterBtn.disabled = false;
            newsletterBtn.innerHTML = `
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="18" height="18">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                </svg>
                Abunə ol
            `;
        }, 1500);
    });
}

// =================================
// NOTIFICATION SYSTEM - FAST
// =================================
function showNotification(message, type = 'success') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    // Add icon based on type
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    notification.innerHTML = `
        <span class="notification-icon">${icons[type] || icons.info}</span>
        <span class="notification-message">${message}</span>
        <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    // Style the notification
    const colors = {
        success: '#48bb78',
        error: '#f56565',
        warning: '#ed8936',
        info: '#4299e1'
    };
    
    Object.assign(notification.style, {
        position: 'fixed',
        top: '100px',
        right: '20px',
        background: colors[type] || colors.info,
        color: 'white',
        padding: '1rem 1.5rem',
        borderRadius: '12px',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
        zIndex: '10000',
        transform: 'translateX(400px)',
        transition: 'all 0.3s ease',
        fontSize: '0.9rem',
        fontWeight: '500',
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        maxWidth: '350px',
        wordBreak: 'break-word'
    });
    
    // Style close button
    const closeBtn = notification.querySelector('.notification-close');
    Object.assign(closeBtn.style, {
        background: 'none',
        border: 'none',
        color: 'white',
        fontSize: '1.2rem',
        cursor: 'pointer',
        padding: '0',
        marginLeft: 'auto',
        opacity: '0.7',
        transition: 'opacity 0.2s ease'
    });
    
    closeBtn.addEventListener('mouseenter', () => closeBtn.style.opacity = '1');
    closeBtn.addEventListener('mouseleave', () => closeBtn.style.opacity = '0.7');
    
    document.body.appendChild(notification);
    
    // Stack notifications
    const existingNotifications = document.querySelectorAll('.notification');
    if (existingNotifications.length > 1) {
        notification.style.top = `${100 + (existingNotifications.length - 1) * 70}px`;
    }
    
    // Animate in
    requestAnimationFrame(() => {
        notification.style.transform = 'translateX(0)';
    });
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, 4000);
    
    // Click to dismiss
    notification.addEventListener('click', (e) => {
        if (e.target !== closeBtn) {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    });
}

// =================================
// PERFORMANCE MONITORING
// =================================
function initializePerformanceMonitoring() {
    // Performance metrics
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const navigationTiming = performance.getEntriesByType('navigation')[0];
            if (navigationTiming) {
                const loadTime = navigationTiming.loadEventEnd - navigationTiming.loadEventStart;
                console.log(`Page load time: ${loadTime}ms`);
                
                // Show performance notification for developers
                if (loadTime > 3000) {
                    console.warn('Page load time is high:', loadTime + 'ms');
                }
            }
        });
    }
    
    // Memory usage monitoring (for development)
    if ('memory' in performance) {
        setInterval(() => {
            const memInfo = performance.memory;
            if (memInfo.usedJSHeapSize / memInfo.jsHeapSizeLimit > 0.9) {
                console.warn('High memory usage detected');
            }
        }, 30000); // Check every 30 seconds
    }
}

// =================================
// UTILITY FUNCTIONS - OPTIMIZED
// =================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function formatPrice(price) {
    return new Intl.NumberFormat('az-AZ', {
        style: 'currency',
        currency: 'AZN',
        minimumFractionDigits: 2
    }).format(price);
}

// Device detection
function isMobile() {
    return window.innerWidth <= 768;
}

function isTablet() {
    return window.innerWidth > 768 && window.innerWidth <= 1024;
}

function isDesktop() {
    return window.innerWidth > 1024;
}

// =================================
// SMOOTH SCROLLING - SIMPLE
// =================================
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const headerHeight = document.querySelector('.floating-header')?.offsetHeight || 0;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize smooth scrolling when DOM is ready
document.addEventListener('DOMContentLoaded', initializeSmoothScrolling);

// =================================
// KEYBOARD NAVIGATION - OPTIMIZED
// =================================
document.addEventListener('keydown', (e) => {
    // Escape key - close all overlays
    if (e.key === 'Escape') {
        if (appState.isSearchOpen) {
            document.querySelector('.search-overlay')?.classList.remove('active');
            document.body.style.overflow = '';
            appState.isSearchOpen = false;
        }
        
        if (appState.isMobileMenuOpen) {
            document.querySelector('.mobile-nav-menu')?.classList.remove('active');
            document.querySelector('.mobile-menu-toggle')?.classList.remove('active');
            document.body.style.overflow = '';
            appState.isMobileMenuOpen = false;
        }
        
        if (appState.isAccountMenuOpen) {
            document.querySelector('.account-dropdown')?.classList.remove('active');
            appState.isAccountMenuOpen = false;
        }
    }
});

// =================================
// ERROR HANDLING - SIMPLIFIED
// =================================
window.addEventListener('error', function(e) {
    console.error('JavaScript error occurred:', e.error);
    showNotification('Bir xəta baş verdi. Səhifəni yeniləyin.', 'error');
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    showNotification('Bağlantı xətası. Yenidən cəhd edin.', 'error');
});

// =================================
// GLOBAL FUNCTIONS - FAST ACCESS
// =================================
window.addToCart = addToCart;
window.toggleFavorite = toggleFavorite;
window.quickView = quickView;
window.shareProduct = shareProduct;

// Utils object for external access
window.dropAzUtils = {
    showNotification,
    addToCart,
    removeFromCart,
    toggleFavorite,
    quickView,
    shareProduct,
    isMobile,
    isTablet,
    isDesktop,
    debounce,
    throttle,
    formatPrice,
    isValidEmail
};

// =================================
// CSS ANIMATIONS FOR JS
// =================================
const additionalStyles = document.createElement('style');
additionalStyles.textContent = `
    @keyframes cartBounce {
        0% { transform: scale(1); }
        50% { transform: scale(1.15); }
        100% { transform: scale(1); }
    }
    
    @keyframes heartBeat {
        0% { transform: scale(1); }
        25% { transform: scale(1.1); }
        50% { transform: scale(1.15); }
        75% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .favorite-btn.active svg {
        fill: #f56565;
        stroke: #f56565;
    }
    
    .notification {
        cursor: pointer;
    }
    
    .notification:hover {
        transform: translateX(-5px) !important;
    }
    
    .recent-search-item {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(79, 172, 254, 0.1);
        color: #4facfe;
        border-radius: 20px;
        font-size: 0.85rem;
        cursor: pointer;
        margin: 0.25rem;
        transition: all 0.2s ease;
        border: 1px solid rgba(79, 172, 254, 0.2);
    }
    
    .recent-search-item:hover {
        background: #4facfe;
        color: white;
        transform: translateY(-1px);
    }
    
    .no-recent {
        color: #718096;
        font-style: italic;
        font-size: 0.9rem;
        text-align: center;
        padding: 1rem;
    }
    
    .fade-in {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .fade-in.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
`;
document.head.appendChild(additionalStyles);

// =================================
// FINAL INITIALIZATION LOG
// =================================
console.log('🎉 drop.az Enhanced JavaScript loaded successfully!');
console.log('Performance optimizations active 🚀');
console.log('Ready for user interactions ✨');