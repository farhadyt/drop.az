// =================================
// GLOBAL VARIABLES & CONSTANTS
// =================================
let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
let favoriteItems = JSON.parse(localStorage.getItem('favoriteItems')) || [];
let recentSearches = JSON.parse(localStorage.getItem('recentSearches')) || [];
let isSearchOpen = false;
let isMobileMenuOpen = false;
let isAccountMenuOpen = false;

// Performance optimizations
let scrollTimeout;
let resizeTimeout;

// =================================
// MAIN APP INITIALIZATION
// =================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 drop.az platform initializing...');
    
    // Initialize loading screen
    initializeLoadingScreen();
    
    // Initialize all components
    initializeHeader();
    initializeMobileMenu();
    initializeSearch();
    initializeCart();
    initializeFavorites();
    initializeAccountMenu();
    initializeAnimations();
    initializeBackToTop();
    initializeNewsletter();
    initializeProductInteractions();
    initializeProductFilters();
    initializeScrollEffects();
    
    // Update counters on page load
    updateCartCounter();
    updateFavoritesCounter();
    updateRecentSearches();
    
    console.log('✅ drop.az platform initialized successfully!');
});

// =================================
// LOADING SCREEN
// =================================
function initializeLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        // Simulated loading time
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
            setTimeout(() => {
                loadingScreen.remove();
                // Trigger enter animations
                document.body.classList.add('loaded');
            }, 500);
        }, 1200);
    }
}

// =================================
// HEADER FUNCTIONALITY
// =================================
function initializeHeader() {
    const header = document.querySelector('.floating-header');
    if (!header) return;

    let lastScrollTop = 0;
    let isScrolling = false;

    function updateHeader() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add/remove scrolled class
        if (scrollTop > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        // Optional: Header hide/show on scroll
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            // Scrolling down - could hide header
            // header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up - show header
            // header.style.transform = 'translateY(0)';
        }

        lastScrollTop = scrollTop;
        isScrolling = false;
    }

    function onScroll() {
        if (!isScrolling) {
            requestAnimationFrame(updateHeader);
            isScrolling = true;
        }
    }

    // Throttled scroll event
    window.addEventListener('scroll', onScroll, { passive: true });
    
    // Initial call
    updateHeader();
}

// =================================
// MOBILE MENU FUNCTIONALITY
// =================================
function initializeMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-nav-menu');
    const mobileClose = document.querySelector('.mobile-nav-close');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
    
    if (!mobileToggle || !mobileMenu) return;

    function toggleMobileMenu() {
        isMobileMenuOpen = !isMobileMenuOpen;
        
        if (isMobileMenuOpen) {
            openMobileMenu();
        } else {
            closeMobileMenu();
        }
    }

    function openMobileMenu() {
        mobileMenu.classList.add('active');
        mobileToggle.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Animate menu items
        const menuItems = mobileMenu.querySelectorAll('.mobile-nav-link');
        menuItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-30px)';
            
            setTimeout(() => {
                item.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, index * 80);
        });
    }

    function closeMobileMenu() {
        mobileMenu.classList.remove('active');
        mobileToggle.classList.remove('active');
        document.body.style.overflow = '';
        isMobileMenuOpen = false;
    }

    // Event listeners
    mobileToggle.addEventListener('click', toggleMobileMenu);
    
    if (mobileClose) {
        mobileClose.addEventListener('click', closeMobileMenu);
    }

    // Close menu when clicking on links
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });

    // Close menu on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isMobileMenuOpen) {
            closeMobileMenu();
        }
    });

    // Close menu on window resize
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (window.innerWidth > 768 && isMobileMenuOpen) {
                closeMobileMenu();
            }
        }, 150);
    });
}

// =================================
// ACCOUNT MENU FUNCTIONALITY
// =================================
function initializeAccountMenu() {
    const accountToggle = document.querySelector('.account-toggle');
    const accountDropdown = document.querySelector('.account-dropdown');
    const accountMenu = document.querySelector('.account-menu');
    
    if (!accountToggle || !accountDropdown) return;

    function toggleAccountMenu(e) {
        e.stopPropagation();
        isAccountMenuOpen = !isAccountMenuOpen;
        accountDropdown.classList.toggle('active', isAccountMenuOpen);
    }

    function closeAccountMenu() {
        isAccountMenuOpen = false;
        accountDropdown.classList.remove('active');
    }

    // Event listeners
    accountToggle.addEventListener('click', toggleAccountMenu);
    
    // Close when clicking outside
    document.addEventListener('click', (e) => {
        if (isAccountMenuOpen && !accountDropdown.contains(e.target)) {
            closeAccountMenu();
        }
    });

    // Close on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isAccountMenuOpen) {
            closeAccountMenu();
        }
    });
}

// =================================
// SEARCH FUNCTIONALITY
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
        isSearchOpen = true;
        searchOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus on input with delay for animation
        setTimeout(() => {
            if (searchInput) {
                searchInput.focus();
            }
        }, 300);
    }

    function closeSearch() {
        isSearchOpen = false;
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
        
        // Clear search input
        if (searchInput) {
            searchInput.value = '';
        }
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
        }, 1200);
        
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

    if (searchClose) {
        searchClose.addEventListener('click', closeSearch);
    }

    // Close search on overlay click
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) {
            closeSearch();
        }
    });

    // Search form submission
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const query = searchInput ? searchInput.value : '';
            performSearch(query);
        });
    }

    // Suggestion tags
    suggestionTags.forEach(tag => {
        tag.addEventListener('click', () => {
            const query = tag.textContent;
            if (searchInput) {
                searchInput.value = query;
            }
            performSearch(query);
        });
    });

    // Real-time search suggestions (debounced)
    if (searchInput) {
        searchInput.addEventListener('input', debounce((e) => {
            const query = e.target.value;
            if (query.length > 2) {
                // Show search suggestions
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
        if (e.key === 'Escape' && isSearchOpen) {
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
            document.querySelector('.search-input').value = search;
            performSearch(search);
        });
        recentContainer.appendChild(searchItem);
    });
}

// =================================
// CART FUNCTIONALITY
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
        }, 150);
        
        // Show cart
        if (cartItems.length === 0) {
            showNotification('Səbətiniz boşdur', 'info');
        } else {
            showNotification(`Səbətdə ${getTotalCartItems()} məhsul var`, 'success');
            // Here you would open cart modal or navigate to cart page
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
    
    if (totalItems > 0) {
        cartCount.classList.add('active');
        cartCount.style.display = 'flex';
    } else {
        cartCount.classList.remove('active');
        cartCount.style.display = 'none';
    }
}

function getTotalCartItems() {
    return cartItems.reduce((sum, item) => sum + item.quantity, 0);
}

function animateCartIcon() {
    const cartLink = document.querySelector('.cart-link');
    if (!cartLink) return;
    
    cartLink.style.animation = 'none';
    setTimeout(() => {
        cartLink.style.animation = 'cartBounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
    }, 10);
    
    setTimeout(() => {
        cartLink.style.animation = '';
    }, 600);
}

// =================================
// FAVORITES FUNCTIONALITY
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
        if (favoriteBtn) {
            favoriteBtn.classList.remove('active');
        }
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
    
    if (totalFavorites > 0) {
        favoritesCount.classList.add('active');
        favoritesCount.style.display = 'flex';
    } else {
        favoritesCount.classList.remove('active');
        favoritesCount.style.display = 'none';
    }
}

function animateFavoriteIcon(button) {
    button.style.animation = 'heartBeat 0.8s ease';
    setTimeout(() => {
        button.style.animation = '';
    }, 800);
}

// =================================
// PRODUCT INTERACTIONS
// =================================
function initializeProductInteractions() {
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.getAttribute('data-product-id'));
            addToCart(productId);
        });
    });

    // Favorite buttons
    document.querySelectorAll('.favorite-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.getAttribute('data-product-id'));
            toggleFavorite(productId);
        });
        
        // Initialize favorite button state
        const productId = parseInt(button.getAttribute('data-product-id'));
        const isFavorite = favoriteItems.some(item => item.id === productId);
        if (isFavorite) {
            button.classList.add('active');
        }
    });

    // Quick view buttons
    document.querySelectorAll('.quick-view-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.getAttribute('data-product-id'));
            quickView(productId);
        });
    });

    // Share buttons
    document.querySelectorAll('.share-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = parseInt(this.getAttribute('data-product-id'));
            shareProduct(productId);
        });
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
            }, 2000);
        });
    }
}

function quickView(productId) {
    console.log('Quick view for product:', productId);
    showNotification('Məhsul haqqında ətraflı məlumat yüklənir... 👀', 'info');
    
    // Here you would implement quick view modal
    setTimeout(() => {
        showNotification('Tez baxış funksiyası tezliklə əlavə ediləcək! 🔜', 'info');
    }, 1500);
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
// PRODUCT FILTERS
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
            
            productCards.forEach((card, index) => {
                const category = card.getAttribute('data-category');
                const shouldShow = filter === 'all' || category === filter;
                
                if (shouldShow) {
                    card.style.display = 'block';
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    
                    setTimeout(() => {
                        card.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, index * 50);
                } else {
                    card.style.transition = 'all 0.3s ease';
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(-20px)';
                    
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });

            // Show notification
            const visibleCount = Array.from(productCards).filter(card => {
                const category = card.getAttribute('data-category');
                return filter === 'all' || category === filter;
            }).length;
            
            showNotification(`${visibleCount} məhsul göstərilir`, 'info');
        });
    });
}

// =================================
// SCROLL EFFECTS & ANIMATIONS
// =================================
function initializeScrollEffects() {
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

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
        observer.observe(el);
    });
}

function initializeAnimations() {
    // Parallax effect for hero elements (optional)
    const heroElements = document.querySelectorAll('.floating-element');
    
    if (heroElements.length === 0) return;

    function updateParallax() {
        const scrolled = window.pageYOffset;
        
        heroElements.forEach((element, index) => {
            const speed = (index + 1) * 0.3;
            const yPos = -(scrolled * speed);
            element.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });
    }

    // Throttled scroll event
    let ticking = false;
    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateParallax();
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
}

// =================================
// BACK TO TOP FUNCTIONALITY
// =================================
function initializeBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;

    function toggleBackToTop() {
        if (window.pageYOffset > 500) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    }

    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    // Show/hide button on scroll
    window.addEventListener('scroll', throttle(toggleBackToTop, 100), { passive: true });
    
    // Click event
    backToTopBtn.addEventListener('click', scrollToTop);
}

// =================================
// NEWSLETTER FUNCTIONALITY
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
        }, 2000);
    });
}

// =================================
// NOTIFICATION SYSTEM
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
        success: '#38a169',
        error: '#e53e3e',
        warning: '#d69e2e',
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
        transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        fontSize: '0.9rem',
        fontWeight: '500',
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        maxWidth: '350px',
        wordBreak: 'break-word',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)'
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
        notification.style.top = `${100 + (existingNotifications.length - 1) * 80}px`;
    }
    
    // Animate in
    requestAnimationFrame(() => {
        notification.style.transform = 'translateX(0)';
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 400);
        }
    }, 5000);
    
    // Click to dismiss
    notification.addEventListener('click', (e) => {
        if (e.target !== closeBtn) {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 400);
        }
    });
}

// =================================
// UTILITY FUNCTIONS
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
// SMOOTH SCROLLING
// =================================
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const headerHeight = document.querySelector('.floating-header').offsetHeight;
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
// KEYBOARD NAVIGATION & ACCESSIBILITY
// =================================
document.addEventListener('keydown', (e) => {
    // Escape key - close all overlays
    if (e.key === 'Escape') {
        if (isSearchOpen) {
            document.querySelector('.search-overlay').classList.remove('active');
            document.body.style.overflow = '';
            isSearchOpen = false;
        }
        
        if (isMobileMenuOpen) {
            document.querySelector('.mobile-nav-menu').classList.remove('active');
            document.querySelector('.mobile-menu-toggle').classList.remove('active');
            document.body.style.overflow = '';
            isMobileMenuOpen = false;
        }
        
        if (isAccountMenuOpen) {
            document.querySelector('.account-dropdown').classList.remove('active');
            isAccountMenuOpen = false;
        }
    }
});

// =================================
// PERFORMANCE MONITORING
// =================================
window.addEventListener('load', function() {
    // Performance metrics
    if ('performance' in window) {
        const navigationTiming = performance.getEntriesByType('navigation')[0];
        console.log('Page load time:', navigationTiming.loadEventEnd - navigationTiming.loadEventStart, 'ms');
    }
});

// =================================
// ERROR HANDLING
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
// EXPORT GLOBAL FUNCTIONS
// =================================
window.addToCart = addToCart;
window.toggleFavorite = toggleFavorite;
window.quickView = quickView;
window.shareProduct = shareProduct;

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
// CSS ANIMATIONS
// =================================
const style = document.createElement('style');
style.textContent = `
    @keyframes cartBounce {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    @keyframes heartBeat {
        0% { transform: scale(1); }
        25% { transform: scale(1.1); }
        50% { transform: scale(1.2); }
        75% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .favorite-btn.active svg {
        fill: #e53e3e;
        stroke: #e53e3e;
    }
    
    .notification {
        cursor: pointer;
    }
    
    .notification:hover {
        transform: translateX(-5px) !important;
    }
    
    .spinner-small {
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255,255,255,0.3);
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        display: inline-block;
    }
    
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    .recent-search-item {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(66, 153, 225, 0.1);
        color: #4299e1;
        border-radius: 20px;
        font-size: 0.85rem;
        cursor: pointer;
        margin: 0.25rem;
        transition: all 0.2s ease;
        border: 1px solid rgba(66, 153, 225, 0.2);
    }
    
    .recent-search-item:hover {
        background: #4299e1;
        color: white;
        transform: translateY(-1px);
    }
    
    .no-recent {
        color: #718096;
        font-style: italic;
        font-size: 0.9rem;
    }
`;
document.head.appendChild(style);

console.log('🎉 drop.az Enhanced JavaScript loaded successfully!');