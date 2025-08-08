/* catalog/static/admin/js/icon-picker-integration.js */

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
            'shield-alt', 'lock', 'key', 'fingerprint', 'user-secret', 'mask', 'eye-slash', 'unlock', 'safe', 'vault'
        ],
        regular: [
            'heart', 'star', 'bookmark', 'calendar', 'clock', 'envelope', 'file', 'folder', 'user', 'comment',
            'bell', 'flag', 'thumbs-up', 'thumbs-down', 'smile', 'frown', 'meh', 'angry', 'surprise', 'kiss',
            'eye', 'eye-slash', 'lightbulb', 'moon', 'sun', 'snowflake', 'gem', 'diamond', 'circle', 'square'
        ],
        brands: [
            'apple', 'google', 'microsoft', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin', 'github', 'whatsapp',
            'telegram', 'discord', 'slack', 'zoom', 'skype', 'spotify', 'netflix', 'amazon', 'paypal', 'visa',
            'android', 'chrome', 'firefox', 'safari', 'edge', 'opera', 'wordpress', 'drupal', 'joomla', 'shopify'
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
                const fieldName = $(e.target).data('target');
                this.openPicker(fieldName);
            });

            $(document).on('input', '#icon-class', (e) => {
                this.updatePreview($(e.target));
            });
        }

        createModal() {
            const modalHtml = `
                <div id="iconPickerModal" class="icon-picker-modal">
                    <div class="icon-picker-modal-content">
                        <div class="picker-header">
                            <h2>🎨 Professional Icon Picker</h2>
                            <p>FontAwesome 6.5.0 - 2000+ Professional Icons</p>
                        </div>

                        <div class="picker-controls">
                            <div class="search-box">
                                <i class="fas fa-search search-icon"></i>
                                <input type="text" class="search-input" placeholder="İcon axtarın..." id="modalSearchInput">
                            </div>
                            
                            <div class="category-filter" id="modalCategoryFilter">
                                <div class="filter-btn active" data-category="all">Hamısı</div>
                                <div class="filter-btn" data-category="solid">Solid</div>
                                <div class="filter-btn" data-category="regular">Regular</div>
                                <div class="filter-btn" data-category="brands">Brands</div>
                            </div>
                        </div>

                        <div class="selected-preview" id="modalSelectedPreview" style="display: none;">
                            <div class="selected-icon" id="modalSelectedIcon"></div>
                            <div class="selected-info">
                                <div class="selected-class" id="modalSelectedClass">Heç bir icon seçilməyib</div>
                                <div class="selected-name" id="modalSelectedName">Icon seçin</div>
                            </div>
                        </div>

                        <div class="icons-grid" id="modalIconsGrid">
                            <!-- Icons will be loaded here -->
                        </div>

                        <div class="stats-bar">
                            <span id="modalStatsText">İconlar yüklənir...</span>
                            <span>Professional Icon Picker v2.0</span>
                        </div>

                        <div class="action-buttons">
                            <button type="button" class="btn btn-secondary" id="modalClearBtn">
                                <i class="fas fa-times"></i> Təmizlə
                            </button>
                            <button type="button" class="btn btn-secondary" id="modalCancelBtn">
                                <i class="fas fa-ban"></i> Ləğv et
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
            
            // Search functionality
            $('#modalSearchInput').on('input', (e) => {
                this.handleSearch(e.target.value);
            });

            // Category filter
            $('#modalCategoryFilter').on('click', '.filter-btn', (e) => {
                this.handleCategoryFilter($(e.target));
            });

            // Icon selection
            modal.on('click', '.icon-item', (e) => {
                const iconElement = $(e.currentTarget);
                this.selectModalIcon(iconElement);
            });

            // Action buttons
            $('#modalSelectBtn').on('click', () => this.applySelection());
            $('#modalClearBtn').on('click', () => this.clearModalSelection());
            $('#modalCancelBtn').on('click', () => this.closeModal());

            // Close on overlay click
            modal.on('click', (e) => {
                if ($(e.target).is('#iconPickerModal')) {
                    this.closeModal();
                }
            });

            // Keyboard shortcuts
            $(document).on('keydown', (e) => {
                if (modal.hasClass('active')) {
                    if (e.key === 'Escape') {
                        this.closeModal();
                    } else if (e.key === 'Enter' && this.selectedIcon) {
                        this.applySelection();
                    }
                }
            });
        }

        openPicker(fieldName) {
            this.currentField = fieldName;
            this.renderIcons(this.allIcons);
            this.updateModalStats(this.allIcons.length, this.allIcons.length);
            
            // Show modal with animation
            const modal = $('#iconPickerModal');
            modal.addClass('active');
            
            // Focus search input
            setTimeout(() => {
                $('#modalSearchInput').focus();
            }, 300);
        }

        closeModal() {
            $('#iconPickerModal').removeClass('active');
            this.selectedIcon = null;
            this.currentField = null;
            $('#modalSearchInput').val('');
            this.clearModalSelection();
        }

        renderIcons(icons) {
            const grid = $('#modalIconsGrid');
            
            if (icons.length === 0) {
                grid.html(`
                    <div class="no-results">
                        <i class="fas fa-search"></i>
                        <h3>Nəticə tapılmadı</h3>
                        <p>Axtarış kriteriyalarını dəyişdirin</p>
                    </div>
                `);
                return;
            }
            
            const iconsHtml = icons.map(icon => `
                <div class="icon-item" data-icon="${icon.class}" data-name="${icon.displayName}">
                    <div class="category-badge">${icon.category}</div>
                    <i class="${icon.class}"></i>
                    <span class="icon-name">${icon.displayName}</span>
                </div>
            `).join('');
            
            grid.html(iconsHtml);
        }

        handleSearch(query) {
            const searchTerm = query.toLowerCase();
            let filtered = this.allIcons.filter(icon => 
                icon.name.toLowerCase().includes(searchTerm) || 
                icon.displayName.toLowerCase().includes(searchTerm)
            );
            
            if (this.currentFilter !== 'all') {
                filtered = filtered.filter(icon => icon.category === this.currentFilter);
            }
            
            this.renderIcons(filtered);
            this.updateModalStats(filtered.length, this.allIcons.length);
        }

        handleCategoryFilter($filterBtn) {
            $('.filter-btn').removeClass('active');
            $filterBtn.addClass('active');
            
            this.currentFilter = $filterBtn.data('category');
            
            const searchQuery = $('#modalSearchInput').val().toLowerCase();
            let filtered = this.allIcons;
            
            if (searchQuery) {
                filtered = filtered.filter(icon => 
                    icon.name.toLowerCase().includes(searchQuery) || 
                    icon.displayName.toLowerCase().includes(searchQuery)
                );
            }
            
            if (this.currentFilter !== 'all') {
                filtered = filtered.filter(icon => icon.category === this.currentFilter);
            }
            
            this.renderIcons(filtered);
            this.updateModalStats(filtered.length, this.allIcons.length);
        }

        selectModalIcon($iconElement) {
            // Remove previous selection
            $('.icon-item').removeClass('selected');
            
            // Select current
            $iconElement.addClass('selected');
            
            const iconClass = $iconElement.data('icon');
            const iconName = $iconElement.data('name');
            
            this.selectedIcon = { class: iconClass, name: iconName };
            
            // Update preview
            $('#modalSelectedPreview').show();
            $('#modalSelectedIcon').html(`<i class="${iconClass}"></i>`);
            $('#modalSelectedClass').text(iconClass);
            $('#modalSelectedName').text(iconName);
            
            // Enable select button
            $('#modalSelectBtn').prop('disabled', false);
        }

        clearModalSelection() {
            $('.icon-item').removeClass('selected');
            $('#modalSelectedPreview').hide();
            $('#modalSelectBtn').prop('disabled', true);
            this.selectedIcon = null;
        }

        applySelection() {
            if (!this.selectedIcon || !this.currentField) return;
            
            // Update the Django admin field
            const inputField = $(`input[name="${this.currentField}"]`);
            const previewElement = $(`#icon-preview-${this.currentField}`);
            
            inputField.val(this.selectedIcon.class);
            previewElement.html(`<i class="${this.selectedIcon.class}"></i>`);
            
            // Update the current selection text
            const currentSelectionElement = inputField.closest('.icon-picker-widget').find('code');
            currentSelectionElement.text(this.selectedIcon.class);
            
            // Trigger change event
            inputField.trigger('change');
            
            // Show success feedback
            this.showSuccessMessage(`✅ Icon seçildi: ${this.selectedIcon.class}`);
            
            // Close modal
            this.closeModal();
        }

        updatePreview($inputField) {
            const fieldName = $inputField.attr('name');
            const iconClass = $inputField.val();
            const previewElement = $(`#icon-preview-${fieldName}`);
            
            if (iconClass && iconClass.includes('fa-')) {
                previewElement.html(`<i class="${iconClass}"></i>`);
            } else {
                previewElement.html('<i class="fas fa-folder"></i>');
            }
        }

        updateModalStats(showing, total) {
            $('#modalStatsText').text(`${showing} / ${total} icon göstərilir`);
        }

        showSuccessMessage(message) {
            // Create temporary success message
            const messageElement = $(`
                <div class="icon-picker-success" style="
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: #28a745;
                    color: white;
                    padding: 12px 20px;
                    border-radius: 6px;
                    z-index: 10001;
                    font-weight: 500;
                    box-shadow: 0 4px 12px rgba(40,167,69,0.3);
                ">
                    ${message}
                </div>
            `);
            
            $('body').append(messageElement);
            
            setTimeout(() => {
                messageElement.fadeOut(300, function() {
                    $(this).remove();
                });
            }, 3000);
        }
    }

    // Initialize when Django admin is ready
    $(document).ready(function() {
        // Wait for Django admin to fully load
        setTimeout(() => {
            window.iconPicker = new ProfessionalIconPicker();
            console.log('🎨 Professional Icon Picker initialized successfully!');
        }, 500);
    });

})(django.jQuery || jQuery);