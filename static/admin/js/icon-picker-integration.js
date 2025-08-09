/* catalog/static/admin/js/icon-picker-integration.js - COMPLETE FIXED VERSION */

(function($) {
    'use strict';

    // Professional Icon Database
    const ICON_DATABASE = {
        solid: [
            'heart', 'star', 'home', 'user', 'search', 'envelope', 'phone', 'calendar', 'clock', 'map-marker-alt',
            'laptop', 'mobile-alt', 'desktop', 'keyboard', 'mouse', 'headphones', 'tv', 'camera', 'video', 'microphone',
            'tshirt', 'shoe-prints', 'hat-cowboy', 'glasses', 'ring', 'gem', 'crown', 'mask', 'umbrella', 'backpack',
            'car', 'truck', 'motorcycle', 'bicycle', 'plane', 'train', 'bus', 'taxi', 'ship', 'rocket',
            'book', 'graduation-cap', 'pencil-alt', 'pen', 'bookmark', 'newspaper', 'file-alt', 'folder', 'archive', 'clipboard',
            'gamepad', 'dice', 'chess', 'puzzle-piece', 'robot', 'magic', 'wand-magic-sparkles', 'gift', 'birthday-cake', 'balloon',
            'utensils', 'coffee', 'wine-bottle', 'beer', 'pizza-slice', 'hamburger', 'ice-cream', 'apple-alt', 'carrot', 'fish',
            'heartbeat', 'user-md', 'pills', 'syringe', 'first-aid', 'stethoscope', 'thermometer', 'band-aid', 'tooth', 'eye',
            'hammer', 'wrench', 'screwdriver', 'paint-roller', 'brush', 'toolbox', 'hard-hat', 'bolt', 'cog', 'gear',
            'tree', 'leaf', 'seedling', 'flower', 'sun', 'moon', 'cloud', 'rainbow', 'snowflake', 'fire',
            'music', 'volume-up', 'play', 'pause', 'stop', 'forward', 'backward', 'random', 'repeat', 'microphone-alt',
            'shield-alt', 'lock', 'key', 'fingerprint', 'user-secret', 'eye-slash', 'unlock', 'safe', 'vault',
            'shopping-cart', 'credit-card', 'money-bill', 'coins', 'chart-bar', 'chart-line', 'percentage', 'dollar-sign',
            'wifi', 'bluetooth', 'usb', 'hard-drive', 'memory', 'microchip', 'plug', 'battery-full', 'charging-station',
            'bell', 'flag', 'star-of-life', 'bomb', 'anchor', 'fire-extinguisher', 'rocket', 'helicopter', 'parachute-box'
        ],
        regular: [
            'heart', 'star', 'bookmark', 'calendar', 'clock', 'envelope', 'file', 'folder', 'user', 'comment',
            'bell', 'flag', 'thumbs-up', 'thumbs-down', 'smile', 'frown', 'meh', 'angry', 'surprise', 'kiss',
            'eye', 'eye-slash', 'lightbulb', 'moon', 'sun', 'snowflake', 'gem', 'diamond', 'circle', 'square',
            'hand-paper', 'hand-rock', 'hand-scissors', 'handshake', 'paper-plane', 'save', 'edit', 'copy',
            'trash-alt', 'address-book', 'chart-bar', 'building', 'clipboard', 'images', 'keyboard', 'life-ring'
        ],
        brands: [
            'apple', 'google', 'microsoft', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin', 'github', 'whatsapp',
            'telegram', 'discord', 'slack', 'zoom', 'skype', 'spotify', 'netflix', 'amazon', 'paypal', 'visa',
            'android', 'chrome', 'firefox', 'safari', 'edge', 'opera', 'wordpress', 'drupal', 'joomla', 'shopify',
            'react', 'vue', 'angular', 'node-js', 'python', 'java', 'js-square', 'html5', 'css3', 'bootstrap',
            'git-alt', 'npm', 'yarn', 'docker', 'ubuntu', 'windows', 'apple', 'playstation', 'xbox', 'steam'
        ]
    };

    class ProfessionalIconPicker {
        constructor() {
            this.selectedIcon = null;
            this.currentField = null;
            this.allIcons = [];
            this.filteredIcons = [];
            this.currentFilter = 'all';
            
            this.init();
        }

        init() {
            this.buildIconDatabase();
            this.attachEventListeners();
            this.createModal();
        }

        buildIconDatabase() {
            this.allIcons = [];
            
            // Add solid icons
            ICON_DATABASE.solid.forEach(icon => {
                this.allIcons.push({
                    name: icon,
                    class: `fas fa-${icon}`,
                    category: 'solid',
                    displayName: this.formatIconName(icon)
                });
            });

            // Add regular icons
            ICON_DATABASE.regular.forEach(icon => {
                this.allIcons.push({
                    name: icon,
                    class: `far fa-${icon}`,
                    category: 'regular',
                    displayName: this.formatIconName(icon)
                });
            });

            // Add brand icons
            ICON_DATABASE.brands.forEach(icon => {
                this.allIcons.push({
                    name: icon,
                    class: `fab fa-${icon}`,
                    category: 'brands',
                    displayName: this.formatIconName(icon)
                });
            });

            this.filteredIcons = [...this.allIcons];
        }

        formatIconName(name) {
            return name.replace(/-/g, ' ')
                      .replace(/\b\w/g, l => l.toUpperCase());
        }

        attachEventListeners() {
            $(document).on('click', '.icon-picker-btn', (e) => {
                e.preventDefault();
                const fieldName = $(e.target).closest('.icon-picker-btn').data('target');
                this.openPicker(fieldName);
            });

            $(document).on('input', 'input[name*="icon_class"]', (e) => {
                this.updatePreview($(e.target));
            });
        }

        createModal() {
            const modalHtml = `
                <div id="iconPickerModal" class="icon-picker-modal">
                    <div class="icon-picker-modal-content">
                        <div class="picker-header">
                            <h2>🎨 Professional Icon Picker</h2>
                            <p>FontAwesome 6.5.0 - ${this.allIcons.length}+ Professional Icons</p>
                        </div>

                        <div class="picker-controls">
                            <div class="search-box">
                                <i class="fas fa-search search-icon"></i>
                                <input type="text" class="search-input" placeholder="İcon axtarın... (məs: heart, laptop, car)" id="modalSearchInput">
                                <button class="clear-search" style="display: none; position: absolute; right: 45px; top: 50%; transform: translateY(-50%); background: none; border: none; color: #6c757d; cursor: pointer; z-index: 5;">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                            
                            <div class="category-filter" id="modalCategoryFilter">
                                <div class="filter-btn active" data-category="all">
                                    <i class="fas fa-th"></i> Hamısı
                                </div>
                                <div class="filter-btn" data-category="solid">
                                    <i class="fas fa-circle"></i> Solid
                                </div>
                                <div class="filter-btn" data-category="regular">
                                    <i class="far fa-circle"></i> Regular
                                </div>
                                <div class="filter-btn" data-category="brands">
                                    <i class="fab fa-font-awesome"></i> Brands
                                </div>
                            </div>
                        </div>

                        <div class="selected-preview" id="modalSelectedPreview" style="display: none;">
                            <div class="selected-icon" id="modalSelectedIcon">
                                <i class="fas fa-folder"></i>
                            </div>
                            <div class="selected-info">
                                <div class="selected-class" id="modalSelectedClass">Heç bir icon seçilməyib</div>
                                <div class="selected-name" id="modalSelectedName">Icon seçin</div>
                            </div>
                        </div>

                        <div class="icons-grid" id="modalIconsGrid">
                            <div class="loading-indicator">
                                <i class="fas fa-spinner fa-spin"></i>
                                <div>İconlar yüklənir...</div>
                            </div>
                        </div>

                        <div class="stats-bar">
                            <span id="modalStatsText">İconlar yüklənir...</span>
                            <span>Professional Icon Picker v2.0</span>
                        </div>

                        <div class="action-buttons">
                            <button type="button" class="btn btn-secondary" id="modalClearBtn">
                                <i class="fas fa-trash"></i> Təmizlə
                            </button>
                            <button type="button" class="btn btn-secondary" id="modalCancelBtn">
                                <i class="fas fa-times"></i> Ləğv et
                            </button>
                            <button type="button" class="btn btn-primary" id="modalSelectBtn" disabled>
                                <i class="fas fa-check"></i> Seç və Tətbiq et
                            </button>
                        </div>
                    </div>
                </div>
            `;
            
            if ($('#iconPickerModal').length === 0) {
                $('body').append(modalHtml);
                this.attachModalEventListeners();
            }
        }

        attachModalEventListeners() {
            const modal = $('#iconPickerModal');
            
            // Search functionality with real-time update
            $('#modalSearchInput').on('input', (e) => {
                const query = e.target.value;
                this.handleSearch(query);
                this.toggleClearButton(query);
            });

            // Clear search button
            modal.on('click', '.clear-search', () => {
                $('#modalSearchInput').val('');
                this.handleSearch('');
                this.toggleClearButton('');
                $('#modalSearchInput').focus();
            });

            // Category filter
            $('#modalCategoryFilter').on('click', '.filter-btn', (e) => {
                this.handleCategoryFilter($(e.currentTarget));
            });

            // Icon selection with improved handling
            modal.on('click', '.icon-item', (e) => {
                const iconElement = $(e.currentTarget);
                this.selectModalIcon(iconElement);
            });

            // Action buttons
            $('#modalSelectBtn').on('click', () => this.applySelection());
            $('#modalClearBtn').on('click', () => this.clearSelection());
            $('#modalCancelBtn').on('click', () => this.closeModal());

            // Close on overlay click
            modal.on('click', (e) => {
                if ($(e.target).is('#iconPickerModal')) {
                    this.closeModal();
                }
            });

            // Enhanced keyboard shortcuts
            $(document).on('keydown', (e) => {
                if (modal.hasClass('active')) {
                    switch(e.key) {
                        case 'Escape':
                            this.closeModal();
                            break;
                        case 'Enter':
                            if (this.selectedIcon && !$('#modalSelectBtn').prop('disabled')) {
                                this.applySelection();
                            }
                            break;
                        case '/':
                            if (e.ctrlKey || e.metaKey) {
                                e.preventDefault();
                                $('#modalSearchInput').focus();
                            }
                            break;
                    }
                }
            });
        }

        openPicker(fieldName) {
            this.currentField = fieldName;
            
            // Show modal with animation
            const modal = $('#iconPickerModal');
            modal.addClass('active');
            
            // Load all icons initially
            setTimeout(() => {
                this.renderIcons(this.allIcons);
                this.updateModalStats(this.allIcons.length, this.allIcons.length);
            }, 100);
            
            // Focus search input after animation
            setTimeout(() => {
                $('#modalSearchInput').focus();
            }, 400);
        }

        closeModal() {
            $('#iconPickerModal').removeClass('active');
            this.selectedIcon = null;
            this.currentField = null;
            $('#modalSearchInput').val('');
            $('.filter-btn').removeClass('active');
            $('.filter-btn[data-category="all"]').addClass('active');
            this.currentFilter = 'all';
            this.clearModalSelection();
        }

        renderIcons(icons) {
            const grid = $('#modalIconsGrid');
            
            if (icons.length === 0) {
                grid.html(`
                    <div class="no-results">
                        <i class="fas fa-search-minus"></i>
                        <h3>Nəticə tapılmadı</h3>
                        <p>Axtarış kriteriyalarını dəyişin və ya bütün kateqoriyaları yoxlayın</p>
                    </div>
                `);
                return;
            }
            
            // Group icons by category for better organization
            const groupedIcons = this.groupIconsByCategory(icons);
            let iconsHtml = '';
            
            if (this.currentFilter === 'all' && $('#modalSearchInput').val().trim() === '') {
                // Show category sections
                Object.entries(groupedIcons).forEach(([category, categoryIcons]) => {
                    if (categoryIcons.length > 0) {
                        iconsHtml += `
                            <div class="category-section">
                                <h4 class="category-title">
                                    ${this.getCategoryIcon(category)} ${this.getCategoryTitle(category)} 
                                    <span class="count">(${categoryIcons.length})</span>
                                </h4>
                                <div class="category-icons">
                                    ${categoryIcons.map(icon => this.getIconHTML(icon)).join('')}
                                </div>
                            </div>
                        `;
                    }
                });
            } else {
                // Show flat grid for search results or single category
                iconsHtml = icons.map(icon => this.getIconHTML(icon)).join('');
            }
            
            grid.html(iconsHtml);
            
            // Add staggered animation to icons
            this.addIconAnimations();
        }

        groupIconsByCategory(icons) {
            return icons.reduce((groups, icon) => {
                const category = icon.category;
                if (!groups[category]) {
                    groups[category] = [];
                }
                groups[category].push(icon);
                return groups;
            }, {});
        }

        getCategoryIcon(category) {
            const icons = {
                'solid': '<i class="fas fa-circle"></i>',
                'regular': '<i class="far fa-circle"></i>',
                'brands': '<i class="fab fa-font-awesome"></i>'
            };
            return icons[category] || '<i class="fas fa-folder"></i>';
        }

        getCategoryTitle(category) {
            const titles = {
                'solid': 'Solid Icons',
                'regular': 'Regular Icons', 
                'brands': 'Brand Icons'
            };
            return titles[category] || category;
        }

        getIconHTML(icon) {
            return `
                <div class="icon-item" 
                     data-icon="${icon.class}" 
                     data-name="${icon.displayName}"
                     data-category="${icon.category}"
                     title="${icon.displayName} (${icon.class})">
                    <div class="category-badge">${icon.category}</div>
                    <i class="${icon.class}"></i>
                    <div class="icon-info">
                        <span class="icon-name">${icon.displayName}</span>
                        <small class="icon-class">${icon.class}</small>
                    </div>
                </div>
            `;
        }

        addIconAnimations() {
            $('.icon-item').each(function(index) {
                $(this).css('animation-delay', `${(index % 20) * 0.05}s`);
            });
        }

        handleSearch(query) {
            const searchTerm = query.toLowerCase().trim();
            let filtered = this.allIcons;
            
            if (searchTerm) {
                filtered = this.allIcons.filter(icon => 
                    icon.name.toLowerCase().includes(searchTerm) || 
                    icon.displayName.toLowerCase().includes(searchTerm) ||
                    icon.class.toLowerCase().includes(searchTerm)
                );
            }
            
            // Apply category filter if not "all"
            if (this.currentFilter !== 'all') {
                filtered = filtered.filter(icon => icon.category === this.currentFilter);
            }
            
            this.renderIcons(filtered);
            this.updateModalStats(filtered.length, this.allIcons.length);
            
            // Update search results indicator
            if (searchTerm && filtered.length > 0) {
                this.showSearchResults(searchTerm, filtered.length);
            }
        }

        showSearchResults(query, count) {
            // You can add a search results indicator here if needed
            console.log(`Search "${query}" found ${count} results`);
        }

        toggleClearButton(query) {
            const clearBtn = $('.clear-search');
            if (query.trim()) {
                clearBtn.show();
            } else {
                clearBtn.hide();
            }
        }

        handleCategoryFilter($filterBtn) {
            $('.filter-btn').removeClass('active');
            $filterBtn.addClass('active');
            
            this.currentFilter = $filterBtn.data('category');
            
            const searchQuery = $('#modalSearchInput').val().toLowerCase().trim();
            let filtered = this.allIcons;
            
            // Apply search filter first
            if (searchQuery) {
                filtered = filtered.filter(icon => 
                    icon.name.toLowerCase().includes(searchQuery) || 
                    icon.displayName.toLowerCase().includes(searchQuery) ||
                    icon.class.toLowerCase().includes(searchQuery)
                );
            }
            
            // Apply category filter
            if (this.currentFilter !== 'all') {
                filtered = filtered.filter(icon => icon.category === this.currentFilter);
            }
            
            this.renderIcons(filtered);
            this.updateModalStats(filtered.length, this.allIcons.length);
        }

        selectModalIcon($iconElement) {
            // Remove previous selections
            $('.icon-item').removeClass('selected');
            
            // Select current
            $iconElement.addClass('selected');
            
            const iconClass = $iconElement.data('icon');
            const iconName = $iconElement.data('name');
            
            this.selectedIcon = { class: iconClass, name: iconName };
            
            // Update preview
            $('#modalSelectedPreview').show();
            $('#modalSelectedIcon i').attr('class', iconClass);
            $('#modalSelectedClass').text(iconClass);
            $('#modalSelectedName').text(iconName);
            
            // Enable select button
            $('#modalSelectBtn').prop('disabled', false);
            
            // Add selection feedback with pulse animation
            $iconElement.addClass('pulse-once');
            setTimeout(() => $iconElement.removeClass('pulse-once'), 600);
        }

        clearModalSelection() {
            $('.icon-item').removeClass('selected');
            $('#modalSelectedPreview').hide();
            $('#modalSelectBtn').prop('disabled', true);
            this.selectedIcon = null;
        }

        clearSelection() {
            this.applyIcon('');
            this.closeModal();
        }

        applySelection() {
            if (!this.selectedIcon || !this.currentField) return;
            
            this.applyIcon(this.selectedIcon.class);
            this.showSuccessMessage(`✅ Icon seçildi: ${this.selectedIcon.class}`);
            this.closeModal();
        }

        applyIcon(iconClass) {
            const inputField = $(`input[name="${this.currentField}"]`);
            const previewElement = $(`#icon-preview-${this.currentField}`);
            
            if (inputField.length) {
                inputField.val(iconClass);
                inputField.trigger('change');
                
                // Update preview
                this.updatePreview(inputField);
                
                // Update current selection display
                const currentSelectionElement = inputField.closest('.icon-picker-widget').find('.current-icon-code');
                if (currentSelectionElement.length) {
                    currentSelectionElement.text(iconClass || 'Heç bir icon seçilməyib');
                }
                
                // Update icon details
                this.updateIconDetails(inputField, iconClass);
            }
        }

        updatePreview($inputField) {
            const fieldName = $inputField.attr('name');
            const iconClass = $inputField.val();
            const previewElement = $(`#icon-preview-${fieldName}`);
            
            if (previewElement.length) {
                const iconElement = previewElement.find('i');
                if (iconClass && iconClass.includes('fa-')) {
                    iconElement.attr('class', iconClass);
                    
                    // Update color indicator if available
                    const colorElement = previewElement.find('small');
                    if (colorElement.length) {
                        colorElement.text(`#${iconClass.replace(/\s+/g, '').toLowerCase()}`);
                    }
                } else {
                    iconElement.attr('class', 'fas fa-folder');
                    const colorElement = previewElement.find('small');
                    if (colorElement.length) {
                        colorElement.text('#default');
                    }
                }
            }
        }

        updateIconDetails($inputField, iconClass) {
            const widget = $inputField.closest('.icon-picker-widget');
            const iconDetailsElement = widget.find('.icon-details');
            
            if (iconDetailsElement.length && iconClass) {
                // Update the main icon in current selection
                const mainIconElement = widget.find('.current-icon-display > i');
                if (mainIconElement.length) {
                    mainIconElement.attr('class', iconClass);
                }
                
                // Update icon type info
                this.updateIconTypeInfo(widget, iconClass);
            }
        }

        updateIconTypeInfo($widget, iconClass) {
            const iconTypeInfoElement = $widget.find('.icon-type-info');
            
            if (iconTypeInfoElement.length && iconClass) {
                let iconType, typeColor, typeDescription;
                
                if (iconClass.startsWith('fab')) {
                    iconType = 'Brand';
                    typeColor = '#fd7e14';
                    typeDescription = 'Brand/Logo Icon';
                } else if (iconClass.startsWith('far')) {
                    iconType = 'Regular';
                    typeColor = '#6f42c1';
                    typeDescription = 'Outline Style Icon';
                } else {
                    iconType = 'Solid';
                    typeColor = '#007bff';
                    typeDescription = 'Filled Style Icon';
                }
                
                const cleanName = iconClass.replace(/^(fas|far|fab)\s+fa-/, '');
                const formattedName = cleanName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                
                iconTypeInfoElement.html(`
                    <span class="icon-type" style="background: ${typeColor};">${iconType}</span>
                    <span class="icon-name">${formattedName}</span>
                    <small style="color: #6c757d; font-size: 10px; font-style: italic;">(${typeDescription})</small>
                `);
            }
        }

        updateModalStats(showing, total) {
            $('#modalStatsText').text(`${showing} / ${total} icon göstərilir`);
        }

        showSuccessMessage(message) {
            // Remove existing messages
            $('.icon-picker-success').remove();
            
            // Create new success message
            const messageElement = $(`
                <div class="icon-picker-success">
                    ${message}
                </div>
            `);
            
            $('body').append(messageElement);
            
            // Auto remove after 3 seconds
            setTimeout(() => {
                messageElement.fadeOut(400, function() {
                    $(this).remove();
                });
            }, 3000);
        }
    }

    // Quick Actions functionality
    class QuickActions {
        static init() {
            this.attachQuickActionListeners();
        }

        static attachQuickActionListeners() {
            // Clear icon quick action
            $(document).on('click', '.quick-action-btn.clear-icon', function(e) {
                e.preventDefault();
                const fieldName = $(this).data('field');
                QuickActions.clearIcon(fieldName);
            });

            // Random icon quick action
            $(document).on('click', '.quick-action-btn.random-icon', function(e) {
                e.preventDefault();
                const fieldName = $(this).data('field');
                QuickActions.selectRandomIcon(fieldName);
            });

            // Popular icons quick action
            $(document).on('click', '.quick-action-btn.popular-icons', function(e) {
                e.preventDefault();
                const fieldName = $(this).data('field');
                QuickActions.selectPopularIcon(fieldName);
            });
        }

        static clearIcon(fieldName) {
            const inputField = $(`input[name="${fieldName}"]`);
            const widget = inputField.closest('.icon-picker-widget');
            
            inputField.val('');
            inputField.trigger('change');
            
            // Update preview
            const previewElement = widget.find('.icon-preview i');
            if (previewElement.length) {
                previewElement.attr('class', 'fas fa-folder');
            }
            
            // Update current selection
            const currentIconCode = widget.find('.current-icon-code');
            if (currentIconCode.length) {
                currentIconCode.text('Heç bir icon seçilməyib');
            }
            
            // Update main display icon
            const mainIcon = widget.find('.current-icon-display > i');
            if (mainIcon.length) {
                mainIcon.attr('class', 'fas fa-folder');
            }
            
            // Clear icon type info
            const iconTypeInfo = widget.find('.icon-type-info');
            if (iconTypeInfo.length) {
                iconTypeInfo.html('<span class="no-icon" style="color: #6c757d; font-size: 12px; font-style: italic;">Icon seçilməyib</span>');
            }
            
            QuickActions.showMessage('🗑️ Icon təmizləndi');
        }

        static selectRandomIcon(fieldName) {
            const allIcons = [
                ...ICON_DATABASE.solid.map(icon => `fas fa-${icon}`),
                ...ICON_DATABASE.regular.map(icon => `far fa-${icon}`),
                ...ICON_DATABASE.brands.map(icon => `fab fa-${icon}`)
            ];
            
            const randomIcon = allIcons[Math.floor(Math.random() * allIcons.length)];
            QuickActions.applyIconToField(fieldName, randomIcon);
            QuickActions.showMessage(`🎲 Təsadüfi icon: ${randomIcon}`);
        }

        static selectPopularIcon(fieldName) {
            const popularIcons = [
                'fas fa-heart', 'fas fa-star', 'fas fa-home', 'fas fa-user', 
                'fas fa-envelope', 'fas fa-phone', 'fas fa-search', 'fas fa-cog',
                'fas fa-shopping-cart', 'fas fa-calendar', 'fas fa-camera', 'fas fa-music'
            ];
            
            const randomPopular = popularIcons[Math.floor(Math.random() * popularIcons.length)];
            QuickActions.applyIconToField(fieldName, randomPopular);
            QuickActions.showMessage(`⭐ Populyar icon: ${randomPopular}`);
        }

        static applyIconToField(fieldName, iconClass) {
            const inputField = $(`input[name="${fieldName}"]`);
            const widget = inputField.closest('.icon-picker-widget');
            
            inputField.val(iconClass);
            inputField.trigger('change');
            
            // Update all UI elements
            if (window.iconPicker) {
                window.iconPicker.updatePreview(inputField);
                window.iconPicker.updateIconDetails(inputField, iconClass);
            }
        }

        static showMessage(message) {
            $('.icon-picker-success').remove();
            
            const messageElement = $(`
                <div class="icon-picker-success">
                    ${message}
                </div>
            `);
            
            $('body').append(messageElement);
            
            setTimeout(() => {
                messageElement.fadeOut(400, function() {
                    $(this).remove();
                });
            }, 2500);
        }
    }

    // Enhanced initialization with better error handling
    function initializeIconPicker() {
        try {
            window.iconPicker = new ProfessionalIconPicker();
            QuickActions.init();
            
            // Add CSS for pulse animation if not exists
            if (!$('#icon-picker-animations').length) {
                $('head').append(`
                    <style id="icon-picker-animations">
                        .pulse-once {
                            animation: pulseOnce 0.6s ease-out !important;
                        }
                        
                        @keyframes pulseOnce {
                            0% { transform: scale(1); }
                            50% { transform: scale(1.1); box-shadow: 0 8px 25px rgba(0,123,255,0.4); }
                            100% { transform: scale(1); }
                        }
                        
                        .icon-item {
                            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                        }
                        
                        .icon-item:hover {
                            transform: translateY(-3px) scale(1.02);
                        }
                        
                        .icon-item.selected {
                            transform: translateY(-3px) scale(1.05);
                        }
                        
                        .clear-search {
                            transition: all 0.2s ease;
                        }
                        
                        .clear-search:hover {
                            color: #dc3545 !important;
                            transform: scale(1.1);
                        }
                    </style>
                `);
            }
            
            console.log('🎨 Professional Icon Picker v2.0 initialized successfully!');
            console.log(`📊 Total icons available: ${window.iconPicker.allIcons.length}`);
            console.log(`🔍 Categories: Solid (${ICON_DATABASE.solid.length}), Regular (${ICON_DATABASE.regular.length}), Brands (${ICON_DATABASE.brands.length})`);
            
        } catch (error) {
            console.error('❌ Icon Picker initialization failed:', error);
            
            // Fallback functionality
            $(document).on('click', '.icon-picker-btn', function(e) {
                e.preventDefault();
                alert('⚠️ Icon Picker yüklənmədi. Səhifəni yeniləyin və ya admin ilə əlaqə saxlayın.');
            });
        }
    }

    // Initialize when Django admin is ready
    $(document).ready(function() {
        // Wait for Django admin to fully load
        if (typeof django !== 'undefined' && django.jQuery) {
            // Django admin environment
            setTimeout(initializeIconPicker, 500);
        } else {
            // Standalone environment
            setTimeout(initializeIconPicker, 100);
        }
    });

    // Also initialize on page load as backup
    $(window).on('load', function() {
        if (!window.iconPicker) {
            console.log('🔄 Backup initialization triggered');
            initializeIconPicker();
        }
    });

    // Handle dynamic content loading (for inline formsets, etc.)
    $(document).on('DOMNodeInserted', function(e) {
        if ($(e.target).find('.icon-picker-btn').length > 0) {
            console.log('🔄 Dynamic content detected, reinitializing...');
            setTimeout(initializeIconPicker, 100);
        }
    });

})(django.jQuery || jQuery);