// =================================
// ENHANCED MEGA MENU - DROP.AZ
// 3-Level Navigation System like TAP.AZ
// =================================

class MegaMenu {
    constructor() {
        this.elements = {
            dropdown: document.querySelector('.nav-categories-dropdown'),
            trigger: document.querySelector('.categories-nav-link'),
            menu: document.querySelector('.categories-dropdown-menu'),
            
            // Level 1: Main categories
            categoryItems: document.querySelectorAll('.category-dropdown-item'),
            
            // Level 2: Subcategories
            subcategoriesPanel: document.querySelector('.subcategories-panel'),
            subcategoryGroups: document.querySelectorAll('.subcategory-group'),
            subcategoryItems: document.querySelectorAll('.subcategory-list-item'),
            subcategoriesPlaceholder: document.querySelector('.subcategory-group-placeholder'),
            
            // Level 3: Third level categories
            thirdLevelPanel: document.querySelector('.third-level-panel'),
            thirdLevelGroups: document.querySelectorAll('.third-level-group'),
            thirdLevelItems: document.querySelectorAll('.third-level-item'),
            thirdLevelPlaceholder: document.querySelector('.third-level-group-placeholder'),
        };

        if (!this.elements.dropdown) {
            console.warn('Mega Menu not found. Aborting initialization.');
            return;
        }

        this.state = {
            isOpen: false,
            isMobile: window.innerWidth < 768,
            activeCategoryId: null,
            activeSubcategoryId: null,
            closeTimer: null,
        };

        this.init();
    }

    init() {
        this.setupCategoryIcons();
        this.bindEvents();
        console.log('✅ 3-Level Mega Menu Initialized (TAP.AZ Style)');
    }

    setupCategoryIcons() {
        const icons = {
            // Main categories
            'elektronika': '💻', 'telefon': '📱', 'kompüter': '🖥️', 'audio': '🎧', 'tv': '📺', 'oyun': '🎮',
            'nəqliyyat': '🚗', 'avtomobil': '🚙', 'ev': '🏠', 'mebel': '🛋️', 'geyim': '👕', 'ayaqqabı': '👟',
            'idman': '⚽', 'kitab': '📚', 'uşaq': '👶', 'oyuncaq': '🧸', 'heyvanlar': '🐾', 'qida': '🍔',
            'hobbi': '🎨', 'biznes': '💼', 'xidmətlər': '🛠️', 'sağlamlıq': '❤️', 'gözəllik': '💄',
            
            // Subcategories
            'smartphone': '📱', 'laptop': '💻', 'tablet': '📟', 'kamera': '📷', 'qulaqlıq': '🎧',
            'televizor': '📺', 'saat': '⌚', 'aksesuar': '🔌', 'oyun konsolu': '🎮', 'printer': '🖨️',
            
            'default': '📦'
        };

        // Main category icons
        this.elements.categoryItems.forEach(item => {
            const nameEl = item.querySelector('.category-name');
            const iconEl = item.querySelector('.category-icon');
            if (nameEl && iconEl) {
                const name = nameEl.textContent.trim().toLowerCase();
                let iconFound = false;
                
                for (const [key, value] of Object.entries(icons)) {
                    if (name.includes(key)) {
                        iconEl.textContent = value;
                        iconFound = true;
                        break;
                    }
                }
                if (!iconFound) {
                    iconEl.textContent = icons.default;
                }
            }
        });

        // Subcategory icons
        this.elements.subcategoryItems.forEach(item => {
            const nameEl = item.querySelector('.subcategory-name');
            const iconEl = item.querySelector('.subcategory-icon');
            if (nameEl && iconEl) {
                const name = nameEl.textContent.trim().toLowerCase();
                let iconFound = false;
                
                for (const [key, value] of Object.entries(icons)) {
                    if (name.includes(key)) {
                        iconEl.textContent = value;
                        iconFound = true;
                        break;
                    }
                }
                if (!iconFound) {
                    iconEl.textContent = icons.default;
                }
            }
        });

        // Third level icons
        this.elements.thirdLevelItems.forEach(item => {
            const nameEl = item.querySelector('.third-level-name');
            const iconEl = item.querySelector('.third-level-icon');
            if (nameEl && iconEl) {
                const name = nameEl.textContent.trim().toLowerCase();
                let iconFound = false;
                
                for (const [key, value] of Object.entries(icons)) {
                    if (name.includes(key)) {
                        iconEl.textContent = value;
                        iconFound = true;
                        break;
                    }
                }
                if (!iconFound) {
                    iconEl.textContent = '📄'; // Different default for 3rd level
                }
            }
        });
    }

    bindEvents() {
        // Desktop/Mobile detection and event binding
        if (this.state.isMobile) {
            this.bindMobileEvents();
        } else {
            this.bindDesktopEvents();
        }

        // Global events
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.state.isOpen) {
                this.closeMenu();
            }
        });

        window.addEventListener('resize', this.debounce(this.handleResize.bind(this), 200));
    }

    bindDesktopEvents() {
        // Trigger events (hover for desktop)
        this.elements.dropdown.addEventListener('mouseenter', this.openMenu.bind(this));
        this.elements.dropdown.addEventListener('mouseleave', this.startCloseTimer.bind(this));

        // Level 1: Main category hover events
        this.elements.categoryItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                const categoryId = item.dataset.categoryId;
                this.showSubcategories(categoryId);
            });
        });

        // Level 2: Subcategory hover events
        this.elements.subcategoryItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                const subcategoryId = item.dataset.subcategoryId;
                this.showThirdLevel(subcategoryId);
            });
        });
    }

    bindMobileEvents() {
        // Mobile trigger click
        this.elements.trigger.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMenu();
        });

        // Mobile category accordion
        this.elements.categoryItems.forEach(item => {
            const link = item.querySelector('.category-dropdown-link');
            link.addEventListener('click', (e) => this.handleMobileCategoryClick(e, item));
        });

        // Mobile subcategory accordion
        this.elements.subcategoryItems.forEach(item => {
            const link = item.querySelector('.subcategory-link');
            link.addEventListener('click', (e) => this.handleMobileSubcategoryClick(e, item));
        });
    }

    // =================================
    // DESKTOP MENU LOGIC
    // =================================
    openMenu() {
        if (this.state.isOpen) {
            clearTimeout(this.state.closeTimer);
            return;
        }
        
        this.state.isOpen = true;
        this.elements.dropdown.classList.add('open');
        this.elements.trigger.setAttribute('aria-expanded', 'true');
        
        // Show subcategories panel but keep placeholder visible initially
        this.elements.subcategoriesPanel.style.display = 'block';
        this.elements.thirdLevelPanel.style.display = 'block';
        
        this.showSubcategoriesPlaceholder();
        this.showThirdLevelPlaceholder();
    }

    closeMenu() {
        if (!this.state.isOpen) return;
        
        this.state.isOpen = false;
        this.elements.dropdown.classList.remove('open');
        this.elements.trigger.setAttribute('aria-expanded', 'false');

        // Reset all states
        this.resetAllStates();
    }

    startCloseTimer() {
        this.state.closeTimer = setTimeout(() => {
            this.closeMenu();
        }, 300);
    }

    // =================================
    // LEVEL 2: SUBCATEGORIES LOGIC
    // =================================
    showSubcategories(categoryId) {
        if (this.state.isMobile || this.state.activeCategoryId === categoryId) return;
        
        this.state.activeCategoryId = categoryId;
        
        // Update active states for level 1
        this.elements.categoryItems.forEach(item => {
            item.classList.toggle('active', item.dataset.categoryId === categoryId);
        });

        // Hide placeholder and show the correct subcategory group
        this.hideSubcategoriesPlaceholder();
        
        let hasSubcategories = false;
        this.elements.subcategoryGroups.forEach(group => {
            if (group.id === `sub-${categoryId}`) {
                group.style.display = 'block';
                hasSubcategories = true;
            } else {
                group.style.display = 'none';
            }
        });
        
        if (!hasSubcategories) {
            this.showSubcategoriesPlaceholder();
        }

        // Reset third level when switching main categories
        this.resetThirdLevel();
        this.showThirdLevelPlaceholder();
    }

    showSubcategoriesPlaceholder() {
        if (this.elements.subcategoriesPlaceholder) {
            this.elements.subcategoryGroups.forEach(group => group.style.display = 'none');
            this.elements.subcategoriesPlaceholder.style.display = 'flex';
        }
    }

    hideSubcategoriesPlaceholder() {
        if (this.elements.subcategoriesPlaceholder) {
            this.elements.subcategoriesPlaceholder.style.display = 'none';
        }
    }

    // =================================
    // LEVEL 3: THIRD LEVEL LOGIC
    // =================================
    showThirdLevel(subcategoryId) {
        if (this.state.isMobile || this.state.activeSubcategoryId === subcategoryId) return;
        
        this.state.activeSubcategoryId = subcategoryId;
        
        // Update active states for level 2
        this.elements.subcategoryItems.forEach(item => {
            item.classList.toggle('active', item.dataset.subcategoryId === subcategoryId);
        });

        // Hide placeholder and show the correct third level group
        this.hideThirdLevelPlaceholder();
        
        let hasThirdLevel = false;
        this.elements.thirdLevelGroups.forEach(group => {
            if (group.id === `third-${subcategoryId}`) {
                group.style.display = 'block';
                hasThirdLevel = true;
            } else {
                group.style.display = 'none';
            }
        });
        
        if (!hasThirdLevel) {
            this.showThirdLevelPlaceholder();
        }
    }

    showThirdLevelPlaceholder() {
        if (this.elements.thirdLevelPlaceholder) {
            this.elements.thirdLevelGroups.forEach(group => group.style.display = 'none');
            this.elements.thirdLevelPlaceholder.style.display = 'flex';
        }
    }

    hideThirdLevelPlaceholder() {
        if (this.elements.thirdLevelPlaceholder) {
            this.elements.thirdLevelPlaceholder.style.display = 'none';
        }
    }

    resetThirdLevel() {
        this.state.activeSubcategoryId = null;
        this.elements.subcategoryItems.forEach(item => item.classList.remove('active'));
        this.elements.thirdLevelGroups.forEach(group => group.style.display = 'none');
    }

    // =================================
    // MOBILE MENU LOGIC
    // =================================
    toggleMenu() {
        this.state.isOpen ? this.closeMenu() : this.openMenu();
    }

    handleMobileCategoryClick(e, item) {
        // Check if it has subcategories
        const hasSubcategories = item.querySelector('[id^="sub-"]');
        if (hasSubcategories) {
            e.preventDefault();
            this.toggleMobileSubcategories(item);
        }
        // If no subcategories, allow navigation (don't prevent default)
    }

    handleMobileSubcategoryClick(e, item) {
        // Check if it has third level categories
        const hasThirdLevel = document.querySelector(`[id^="third-${item.dataset.subcategoryId}"]`);
        if (hasThirdLevel) {
            e.preventDefault();
            this.toggleMobileThirdLevel(item);
        }
        // If no third level, allow navigation
    }

    toggleMobileSubcategories(item) {
        const isExpanded = item.classList.contains('expanded');

        // Close all other main categories
        this.elements.categoryItems.forEach(otherItem => {
            if (otherItem !== item) {
                otherItem.classList.remove('expanded');
                this.closeMobilePanel(otherItem);
            }
        });

        // Toggle the clicked one
        item.classList.toggle('expanded');
        if (item.classList.contains('expanded')) {
            this.openMobilePanel(item);
        } else {
            this.closeMobilePanel(item);
        }
    }

    toggleMobileThirdLevel(item) {
        const isExpanded = item.classList.contains('expanded');

        // Close all other subcategories in the same group
        const parentGroup = item.closest('.subcategory-group');
        if (parentGroup) {
            parentGroup.querySelectorAll('.subcategory-list-item').forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('expanded');
                    this.closeMobilePanel(otherItem);
                }
            });
        }

        // Toggle the clicked one
        item.classList.toggle('expanded');
        if (item.classList.contains('expanded')) {
            this.openMobilePanel(item);
        } else {
            this.closeMobilePanel(item);
        }
    }

    openMobilePanel(item) {
        const subPanel = item.querySelector('[class*="panel"], [id^="sub-"], [id^="third-"]');
        if (subPanel) {
            subPanel.style.maxHeight = subPanel.scrollHeight + "px";
            subPanel.style.display = 'block';
        }
    }

    closeMobilePanel(item) {
        const subPanel = item.querySelector('[class*="panel"], [id^="sub-"], [id^="third-"]');
        if (subPanel) {
            subPanel.style.maxHeight = null;
            subPanel.style.display = 'none';
        }
    }

    // =================================
    // UTILITY METHODS
    // =================================
    resetAllStates() {
        this.state.activeCategoryId = null;
        this.state.activeSubcategoryId = null;
        
        // Reset level 1
        this.elements.categoryItems.forEach(item => item.classList.remove('active', 'expanded'));
        
        // Reset level 2
        this.elements.subcategoryItems.forEach(item => item.classList.remove('active', 'expanded'));
        this.elements.subcategoryGroups.forEach(group => group.style.display = 'none');
        
        // Reset level 3
        this.elements.thirdLevelItems.forEach(item => item.classList.remove('active'));
        this.elements.thirdLevelGroups.forEach(group => group.style.display = 'none');
        
        // Show placeholders
        this.showSubcategoriesPlaceholder();
        this.showThirdLevelPlaceholder();
        
        // Hide panels on mobile
        if (this.state.isMobile) {
            document.body.style.overflow = '';
            this.removeBackdrop();
        }
    }

    handleResize() {
        const wasMobile = this.state.isMobile;
        this.state.isMobile = window.innerWidth < 768;

        if (wasMobile !== this.state.isMobile) {
            this.closeMenu();
            this.resetAllStates();
            
            // Re-bind events for the new mode
            this.bindEvents();
        }
    }

    createBackdrop() {
        if (document.querySelector('.mobile-backdrop')) return;
        
        const backdrop = document.createElement('div');
        backdrop.className = 'mobile-backdrop';
        document.body.appendChild(backdrop);
        
        requestAnimationFrame(() => backdrop.classList.add('active'));
        backdrop.addEventListener('click', () => this.closeMenu());
    }

    removeBackdrop() {
        const backdrop = document.querySelector('.mobile-backdrop');
        if (backdrop) {
            backdrop.classList.remove('active');
            setTimeout(() => backdrop.remove(), 300);
        }
    }
    
    debounce(func, delay) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.megaMenu = new MegaMenu();
    console.log('🎯 TAP.AZ Style 3-Level Mega Menu Ready!');
});