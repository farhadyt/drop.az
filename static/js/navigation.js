// =================================
// ENHANCED MEGA MENU - DROP.AZ
// 3-Level Navigation System - Full Width
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

            // Mobile elements
            mobileMenu: document.querySelector('.mobile-nav-menu'),
            mobileCategoryToggle: document.querySelector('.mobile-category-toggle'),
            mobileSubcategories: document.getElementById('mobile-categories-list')
        };

        if (!this.elements.dropdown && !this.elements.mobileCategoryToggle) {
            console.warn('Mega Menu elements not found. Aborting initialization.');
            return;
        }

        this.state = {
            isOpen: false,
            isMobile: window.innerWidth < 768,
            isTablet: window.innerWidth >= 768 && window.innerWidth < 992,
            activeCategoryId: null,
            activeSubcategoryId: null,
            closeTimer: null,
            mobileMenuOpen: false,
            mobileCategoriesOpen: false
        };

        this.init();
    }

    init() {
        this.setupCategoryIcons();
        this.bindEvents();
        this.handleResize();
        this.adjustMenuPosition();
        console.log('✅ Full Width 3-Level Mega Menu Initialized');
    }

    adjustMenuPosition() {
        // Ensure menu is positioned correctly relative to viewport
        if (this.elements.menu) {
            const headerHeight = document.querySelector('.floating-header')?.offsetHeight || 80;
            this.elements.menu.style.top = `${headerHeight}px`;
        }
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
        // Desktop/Tablet/Mobile detection and event binding
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

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (this.state.isOpen && 
                this.elements.dropdown &&
                !this.elements.dropdown.contains(e.target) && 
                !this.elements.menu.contains(e.target)) {
                this.closeMenu();
            }
        });

        // Window resize handler
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize();
            this.adjustMenuPosition();
        }, 200));

        // Scroll handler to adjust menu position
        window.addEventListener('scroll', () => {
            if (this.state.isOpen && !this.state.isMobile) {
                this.adjustMenuPosition();
            }
        });
    }

    bindDesktopEvents() {
        if (!this.elements.trigger) return;

        // Open on click and hover for full parity across templates
        this.elements.trigger.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleMenu();
        });
        this.elements.trigger.addEventListener('mouseenter', () => {
            this.openMenu();
        });

        // Keep menu open when hovering inside menu
        if (this.elements.menu) {
            this.elements.menu.addEventListener('mouseenter', () => {
                clearTimeout(this.state.closeTimer);
            });

            this.elements.menu.addEventListener('mouseleave', () => {
                this.startCloseTimer();
            });
        }

        // Level 1: Main category hover events — bind to link for reliability
        this.elements.categoryItems.forEach(item => {
            const link = item.querySelector('.category-dropdown-link') || item;
            link.addEventListener('mouseenter', () => {
                const categoryId = item.dataset.categoryId;
                this.showSubcategories(categoryId);
            });
        });

        // Level 2: Subcategory hover events (desktop only) — bind to link
        if (!this.state.isTablet) {
            this.elements.subcategoryItems.forEach(item => {
                const link = item.querySelector('.subcategory-link') || item;
                link.addEventListener('mouseenter', () => {
                    const subcategoryId = item.dataset.subcategoryId;
                    this.showThirdLevel(subcategoryId);
                });
            });
        }
    }

    bindMobileEvents() {
        if (!this.elements.trigger) return;

        // Mobile trigger click
        this.elements.trigger.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleMenu();
        });

        // Mobile category accordion
        this.elements.categoryItems.forEach(item => {
            const link = item.querySelector('.category-dropdown-link');
            if (link) {
                link.addEventListener('click', (e) => this.handleMobileCategoryClick(e, item));
            }
        });

        // Mobile subcategory accordion
        this.elements.subcategoryItems.forEach(item => {
            const link = item.querySelector('.subcategory-link');
            if (link) {
                link.addEventListener('click', (e) => this.handleMobileSubcategoryClick(e, item));
            }
        });
    }

    // =================================
    // DESKTOP MENU LOGIC
    // =================================
    toggleMenu() {
        this.state.isOpen ? this.closeMenu() : this.openMenu();
    }

    openMenu() {
        if (!this.elements.dropdown || !this.elements.menu) return;
        
        if (this.state.isOpen) {
            clearTimeout(this.state.closeTimer);
            return;
        }
        
        this.state.isOpen = true;
        this.elements.dropdown.classList.add('open');
        this.elements.trigger.setAttribute('aria-expanded', 'true');
        
        // Adjust position for full width
        this.adjustMenuPosition();
        
        // Show panels on desktop/tablet
        if (!this.state.isMobile) {
            if (this.elements.subcategoriesPanel) {
                this.elements.subcategoriesPanel.style.display = 'block';
            }
            if (this.elements.thirdLevelPanel && !this.state.isTablet) {
                this.elements.thirdLevelPanel.style.display = 'block';
            }
            
            this.showSubcategoriesPlaceholder();
            if (!this.state.isTablet) {
                this.showThirdLevelPlaceholder();
            }
        }

        // Add backdrop on mobile
        if (this.state.isMobile) {
            this.createBackdrop();
            document.body.style.overflow = 'hidden';
        }
    }

    closeMenu() {
        if (!this.state.isOpen) return;
        
        this.state.isOpen = false;
        if (this.elements.dropdown) {
            this.elements.dropdown.classList.remove('open');
        }
        if (this.elements.trigger) {
            this.elements.trigger.setAttribute('aria-expanded', 'false');
        }

        // Reset all states
        this.resetAllStates();

        // Remove backdrop on mobile
        if (this.state.isMobile) {
            this.removeBackdrop();
            document.body.style.overflow = '';
        }
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

        // Reset third level when switching main categories (only on desktop)
        if (!this.state.isTablet) {
            this.resetThirdLevel();
            this.showThirdLevelPlaceholder();
        }
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
        if (this.state.isMobile || this.state.isTablet || this.state.activeSubcategoryId === subcategoryId) return;
        
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
    handleMobileCategoryClick(e, item) {
        // Check if it has subcategories
        const hasSubcategories = document.querySelector(`[id^="sub-${item.dataset.categoryId}"]`);
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
        const subPanel = item.querySelector('[id^="sub-"], [id^="third-"]');
        if (subPanel) {
            subPanel.style.maxHeight = subPanel.scrollHeight + "px";
            subPanel.style.display = 'block';
        }
    }

    closeMobilePanel(item) {
        const subPanel = item.querySelector('[id^="sub-"], [id^="third-"]');
        if (subPanel) {
            subPanel.style.maxHeight = null;
            setTimeout(() => {
                if (!item.classList.contains('expanded')) {
                    subPanel.style.display = 'none';
                }
            }, 300);
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
        
        // Show placeholders on desktop
        if (!this.state.isMobile) {
            this.showSubcategoriesPlaceholder();
            if (!this.state.isTablet) {
                this.showThirdLevelPlaceholder();
            }
        }
    }

    handleResize() {
        const wasMobile = this.state.isMobile;
        const wasTablet = this.state.isTablet;
        
        this.state.isMobile = window.innerWidth < 768;
        this.state.isTablet = window.innerWidth >= 768 && window.innerWidth < 992;

        if (wasMobile !== this.state.isMobile || wasTablet !== this.state.isTablet) {
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
        backdrop.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1040;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        document.body.appendChild(backdrop);
        
        requestAnimationFrame(() => {
            backdrop.style.opacity = '1';
            backdrop.classList.add('active');
        });
        
        backdrop.addEventListener('click', () => this.closeMenu());
    }

    removeBackdrop() {
        const backdrop = document.querySelector('.mobile-backdrop');
        if (backdrop) {
            backdrop.style.opacity = '0';
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

// =================================
// ENHANCED MOBILE MENU INTEGRATION - İKİ AYRI BUTON SİSTEMİ
// =================================
class MobileMenuIntegration {
    constructor() {
        this.elements = {
            mobileMenuToggle: document.querySelector('.mobile-menu-toggle'),
            mobileMenu: document.querySelector('.mobile-nav-menu'),
            mobileCategoryToggle: document.querySelector('.mobile-category-toggle-btn'),
            mobileSubcategories: document.getElementById('mobile-categories-list'),
            mobileCategoryMainLink: document.querySelector('.mobile-category-main-link')
        };

        this.state = {
            isOpen: false,
            categoriesOpen: false
        };

        this.init();
    }

    init() {
        if (!this.elements.mobileMenuToggle || !this.elements.mobileMenu) {
            console.warn('Mobile menu elements not found');
            return;
        }

        this.bindEvents();
        console.log('✅ Enhanced Mobile Menu Integration initialized');
    }

    bindEvents() {
        // Mobile menu toggle
        this.elements.mobileMenuToggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.toggleMobileMenu();
        });

        // Ana kategori linki - sayfaya git
        if (this.elements.mobileCategoryMainLink) {
            this.elements.mobileCategoryMainLink.addEventListener('click', (e) => {
                // Allow normal navigation - don't prevent default
                const categoryName = this.elements.mobileCategoryMainLink.textContent.trim();
                if (window.dropAzUtils && window.dropAzUtils.showNotification) {
                    window.dropAzUtils.showNotification(`"${categoryName}" açılıyor...`, 'info');
                }
                
                // Close menu after short delay
                setTimeout(() => {
                    this.closeMobileMenu();
                }, 300);
            });
        }

        // Toggle butonu - alt menüyü aç/kapat
        if (this.elements.mobileCategoryToggle) {
            this.elements.mobileCategoryToggle.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleMobileCategories();
            });
        }

        // Alt kategori linklerine dokunma - direkt sayfaya git
        const subcategoryLinks = document.querySelectorAll('.mobile-subcategory-link');
        subcategoryLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                // Allow normal navigation - don't prevent default
                const categoryName = link.textContent.trim();
                if (window.dropAzUtils && window.dropAzUtils.showNotification) {
                    window.dropAzUtils.showNotification(`"${categoryName}" seçildi`, 'info');
                }
                
                // Close menu after selection
                setTimeout(() => {
                    this.closeMobileMenu();
                }, 500);
            });
        });

        // Alt kategori toggle butonları - + işareti
        const subcategoryToggles = document.querySelectorAll('.mobile-subcategory-toggle');
        subcategoryToggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.toggleMobileThirdLevel(toggle);
            });
        });

        // Üçüncü seviye linkler - sayfaya git
        const thirdLevelLinks = document.querySelectorAll('.mobile-third-level-link');
        thirdLevelLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                // Allow normal navigation - don't prevent default
                const categoryName = link.querySelector('span').textContent.trim();
                if (window.dropAzUtils && window.dropAzUtils.showNotification) {
                    window.dropAzUtils.showNotification(`"${categoryName}" seçildi`, 'info');
                }
                
                // Close menu after selection
                setTimeout(() => {
                    this.closeMobileMenu();
                }, 500);
            });
        });

        // Close on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.state.isOpen) {
                this.closeMobileMenu();
            }
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (this.state.isOpen && !this.elements.mobileMenu.contains(e.target) && 
                !this.elements.mobileMenuToggle.contains(e.target)) {
                this.closeMobileMenu();
            }
        });

        // Mobile nav close button
        const mobileNavClose = document.querySelector('.mobile-nav-close');
        if (mobileNavClose) {
            mobileNavClose.addEventListener('click', (e) => {
                e.preventDefault();
                this.closeMobileMenu();
            });
        }
    }

    toggleMobileMenu() {
        this.state.isOpen = !this.state.isOpen;
        
        this.elements.mobileMenu.classList.toggle('active', this.state.isOpen);
        this.elements.mobileMenuToggle.classList.toggle('active', this.state.isOpen);
        
        // Prevent body scroll when menu is open
        document.body.style.overflow = this.state.isOpen ? 'hidden' : '';
        
        // Update ARIA attributes
        this.elements.mobileMenuToggle.setAttribute('aria-expanded', this.state.isOpen);
        this.elements.mobileMenu.setAttribute('aria-hidden', !this.state.isOpen);

        console.log('Mobile menu toggled:', this.state.isOpen);
    }

    toggleMobileCategories() {
        if (!this.elements.mobileSubcategories || !this.elements.mobileCategoryToggle) return;

        this.state.categoriesOpen = !this.state.categoriesOpen;
        const arrow = this.elements.mobileCategoryToggle.querySelector('.mobile-nav-arrow');
        
        // Toggle active classes
        this.elements.mobileCategoryToggle.classList.toggle('active', this.state.categoriesOpen);
        this.elements.mobileSubcategories.classList.toggle('active', this.state.categoriesOpen);
        
        // Animate arrow
        if (arrow) {
            arrow.style.transform = this.state.categoriesOpen ? 'rotate(180deg)' : 'rotate(0deg)';
        }
        
        // Animate height
        if (this.state.categoriesOpen) {
            this.elements.mobileSubcategories.style.maxHeight = this.elements.mobileSubcategories.scrollHeight + 'px';
            this.elements.mobileSubcategories.style.opacity = '1';
            
            if (window.dropAzUtils && window.dropAzUtils.showNotification) {
                window.dropAzUtils.showNotification('Kateqoriyalar açıldı 📂', 'info');
            }
        } else {
            this.elements.mobileSubcategories.style.maxHeight = '0';
            this.elements.mobileSubcategories.style.opacity = '0';
        }
        
        // Update ARIA
        this.elements.mobileCategoryToggle.setAttribute('aria-expanded', this.state.categoriesOpen);
        this.elements.mobileSubcategories.setAttribute('aria-hidden', !this.state.categoriesOpen);

        console.log('Mobile categories toggled:', this.state.categoriesOpen);
    }

    toggleMobileThirdLevel(toggle) {
        const categoryId = toggle.dataset.category;
        const thirdLevelMenu = document.getElementById(`mobile-sub-${categoryId}`);
        
        if (!thirdLevelMenu) return;
        
        const isActive = toggle.classList.contains('active');
        
        // Diğer tüm third level menüleri kapat
        document.querySelectorAll('.mobile-subcategory-toggle.active').forEach(otherToggle => {
            if (otherToggle !== toggle) {
                otherToggle.classList.remove('active');
                otherToggle.setAttribute('aria-expanded', 'false');
                
                const otherCategoryId = otherToggle.dataset.category;
                const otherMenu = document.getElementById(`mobile-sub-${otherCategoryId}`);
                if (otherMenu) {
                    otherMenu.classList.remove('active');
                    otherMenu.style.maxHeight = '0';
                    otherMenu.setAttribute('aria-hidden', 'true');
                }
            }
        });
        
        // Şu anki menüyü toggle et
        if (isActive) {
            // Kapat
            toggle.classList.remove('active');
            toggle.setAttribute('aria-expanded', 'false');
            thirdLevelMenu.classList.remove('active');
            thirdLevelMenu.style.maxHeight = '0';
            thirdLevelMenu.setAttribute('aria-hidden', 'true');
        } else {
            // Aç
            toggle.classList.add('active');
            toggle.setAttribute('aria-expanded', 'true');
            thirdLevelMenu.classList.add('active');
            thirdLevelMenu.style.maxHeight = thirdLevelMenu.scrollHeight + 'px';
            thirdLevelMenu.setAttribute('aria-hidden', 'false');
            
            // AUTO SCROLL - YENİ EKLENEN
            setTimeout(() => {
                thirdLevelMenu.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'nearest',
                    inline: 'nearest'
                });
            }, 200);
            
            // Notification göster
            if (window.dropAzUtils && window.dropAzUtils.showNotification) {
                const categoryName = toggle.closest('.mobile-subcategory-row')
                    .querySelector('.mobile-subcategory-link span').textContent;
                window.dropAzUtils.showNotification(`${categoryName} alt kateqoriyaları açıldı`, 'info');
            }
        }
        
        console.log('Third level toggled:', categoryId, !isActive);
    }

    closeMobileMenu() {
        this.state.isOpen = false;
        this.elements.mobileMenu.classList.remove('active');
        this.elements.mobileMenuToggle.classList.remove('active');
        document.body.style.overflow = '';
        
        // Also close categories
        if (this.state.categoriesOpen) {
            this.toggleMobileCategories();
        }
        
        // Close all third level menus
        document.querySelectorAll('.mobile-subcategory-toggle.active').forEach(toggle => {
            const categoryId = toggle.dataset.category;
            const thirdLevelMenu = document.getElementById(`mobile-sub-${categoryId}`);
            
            toggle.classList.remove('active');
            toggle.setAttribute('aria-expanded', 'false');
            
            if (thirdLevelMenu) {
                thirdLevelMenu.classList.remove('active');
                thirdLevelMenu.style.maxHeight = '0';
                thirdLevelMenu.setAttribute('aria-hidden', 'true');
            }
        });
        
        // Update ARIA
        this.elements.mobileMenuToggle.setAttribute('aria-expanded', 'false');
        this.elements.mobileMenu.setAttribute('aria-hidden', 'true');

        console.log('Mobile menu closed');
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize desktop mega menu
    window.megaMenu = new MegaMenu();
    
    // Initialize mobile menu integration
    window.mobileMenuIntegration = new MobileMenuIntegration();
    
    console.log('🎯 Enhanced Navigation System Ready!');
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Close all menus when page becomes hidden
        if (window.megaMenu && window.megaMenu.state.isOpen) {
            window.megaMenu.closeMenu();
        }
        if (window.mobileMenuIntegration && window.mobileMenuIntegration.state.isOpen) {
            window.mobileMenuIntegration.closeMobileMenu();
        }
    }
});