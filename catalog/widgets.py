# catalog/widgets.py - Professional Icon Picker Widget Enhanced

from django import forms
from django.forms.widgets import Widget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.conf import settings


class IconPickerWidget(forms.TextInput):
    """
    Professional Icon Picker Widget for FontAwesome Icons
    Enhanced with comprehensive icon database and advanced features
    """
    
    
    
    # Comprehensive icon database with categories
    ICON_DATABASE = {
        'Səhiyyə': [
            'heartbeat', 'user-md', 'pills', 'syringe', 'first-aid', 'stethoscope', 
            'thermometer', 'tooth', 'eye', 'hospital', 'ambulance', 'band-aid',
            'dna', 'x-ray', 'brain', 'lungs', 'heart', 'bone', 'wheelchair',
            'medical-kit', 'virus', 'shield-virus'
        ],
        'Elektronika': [
            'laptop', 'mobile-alt', 'desktop', 'tablet', 'keyboard', 'mouse', 
            'headphones', 'tv', 'camera', 'video', 'microphone', 'usb',
            'wifi', 'bluetooth', 'hard-drive', 'memory', 'microchip', 'plug',
            'battery-full', 'charging-station', 'satellite', 'router', 'server'
        ],
        'Geyim & Moda': [
            'tshirt', 'shoe-prints', 'hat-cowboy', 'glasses', 'ring', 'gem', 
            'crown', 'mask', 'umbrella', 'backpack', 'handbag', 'shopping-bag',
            'dress', 'vest', 'mitten', 'socks', 'hat-wizard', 'user-tie',
            'bow-tie', 'female', 'male'
        ],
        'Nəqliyyat': [
            'car', 'truck', 'motorcycle', 'bicycle', 'plane', 'train', 'bus', 
            'taxi', 'ship', 'rocket', 'helicopter', 'subway', 'car-side',
            'truck-loading', 'shipping-fast', 'anchor', 'route', 'gas-pump',
            'traffic-light', 'road', 'parking'
        ],
        'Təhsil': [
            'book', 'graduation-cap', 'pencil-alt', 'pen', 'bookmark', 'newspaper', 
            'file-alt', 'folder', 'archive', 'clipboard', 'calculator', 'ruler',
            'school', 'university', 'blackboard', 'student', 'teacher', 'library',
            'diploma', 'award', 'medal', 'trophy'
        ],
        'Əyləncə & İdman': [
            'gamepad', 'dice', 'chess', 'puzzle-piece', 'magic', 'gift', 
            'birthday-cake', 'balloon', 'party-horn', 'fireworks', 'ticket-alt',
            'running', 'dumbbell', 'futbol', 'basketball-ball', 'tennis-ball',
            'volleyball-ball', 'table-tennis', 'golf-ball', 'hockey-puck', 'swimming-pool'
        ],
        'Yemək & İçki': [
            'utensils', 'coffee', 'wine-bottle', 'beer', 'pizza-slice', 'hamburger', 
            'ice-cream', 'apple-alt', 'carrot', 'fish', 'bread-slice', 'cheese',
            'cookie', 'birthday-cake', 'cocktail', 'glass-whiskey', 'mug-hot',
            'pepper-hot', 'seedling', 'lemon', 'candy-cane'
        ],
        'Alətlər & Texnika': [
            'hammer', 'wrench', 'screwdriver', 'paint-roller', 'brush', 'toolbox', 
            'hard-hat', 'bolt', 'cog', 'gear', 'cut', 'magnet',
            'drill', 'saw', 'level', 'measuring-tape', 'pliers', 'wrench-alt',
            'construction', 'crane', 'bulldozer'
        ],
        'Təbiət & Hava': [
            'tree', 'leaf', 'seedling', 'flower', 'sun', 'moon', 'cloud', 
            'rainbow', 'snowflake', 'fire', 'mountain', 'water',
            'wind', 'tornado', 'lightning', 'thermometer-half', 'icicles',
            'volcano', 'desert', 'forest', 'park'
        ],
        'Musiqi & Səs': [
            'music', 'volume-up', 'play', 'pause', 'stop', 'forward', 'backward', 
            'random', 'repeat', 'guitar', 'drum', 'violin',
            'piano', 'trumpet', 'saxophone', 'headphones-alt', 'radio',
            'compact-disc', 'vinyl', 'microphone-alt', 'speaker'
        ],
        'Təhlükəsizlik': [
            'shield-alt', 'lock', 'key', 'fingerprint', 'user-secret', 'mask', 
            'eye-slash', 'unlock', 'safe', 'vault', 'crown', 'badge',
            'id-card', 'passport', 'certificate', 'security', 'guard',
            'camera-security', 'alarm', 'fire-extinguisher'
        ],
        'Ev & Yaşayış': [
            'home', 'couch', 'bed', 'chair', 'door-open', 'lightbulb', 'plug', 
            'shower', 'toilet', 'kitchen-set', 'stairs', 'window-maximize',
            'lamp', 'fan', 'air-conditioner', 'heater', 'refrigerator',
            'washing-machine', 'vacuum', 'broom', 'key-house'
        ],
        'İş & Biznes': [
            'briefcase', 'building', 'city', 'industry', 'store', 'warehouse', 
            'handshake', 'chart-bar', 'presentation', 'calculator', 'balance-scale',
            'money-bill', 'coins', 'credit-card', 'receipt', 'invoice',
            'contract', 'signature', 'stamp', 'fax', 'printer'
        ],
        'Sosial & Ünsiyyət': [
            'users', 'user-friends', 'user-plus', 'comments', 'share-alt', 
            'thumbs-up', 'thumbs-down', 'heart', 'star', 'fire', 'trophy',
            'chat', 'message', 'envelope', 'phone', 'video-call',
            'handshake-alt', 'people-group', 'network'
        ],
        'Brendlər': [
            'apple', 'google', 'microsoft', 'facebook', 'twitter', 'instagram', 
            'youtube', 'linkedin', 'github', 'whatsapp', 'telegram', 'discord',
            'spotify', 'netflix', 'amazon', 'paypal', 'visa', 'mastercard',
            'android', 'chrome', 'firefox', 'safari', 'edge', 'opera'
        ]
    }
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'icon-picker-input',
            'placeholder': 'FontAwesome icon class daxil edin... (məs: fas fa-heart)'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the enhanced icon picker widget"""
        if attrs is None:
            attrs = {}
        
        attrs = {**self.attrs, **attrs}
        
        # Base input field
        input_html = super().render(name, value, attrs, renderer)
        
        # Icon preview
        icon_preview = self.get_icon_preview(value)
        
        # Current icon info
        current_icon_info = self.get_icon_info(value)
        
        # Total icons count
        total_icons = sum(len(icons) for icons in self.ICON_DATABASE.values())
        
        # Widget wrapper with enhanced functionality
        widget_html = format_html('''
            <div class="icon-picker-widget enhanced" data-field-name="{}">
                <div class="icon-input-group">
                    {}
                    <div class="icon-preview enhanced" id="icon-preview-{}" title="Icon önizləməsi">
                        {}
                        <small class="icon-count">{}</small>
                    </div>
                    <button type="button" class="icon-picker-btn enhanced" data-target="{}">
                        <i class="fas fa-palette"></i> 
                        <span>Professional Icon Picker</span>
                        <small>({} icon)</small>
                    </button>
                </div>
                
                <div class="current-selection enhanced">
                    <div class="selection-info">
                        <div class="current-icon-display">
                            {}
                            <div class="icon-details">
                                <strong>Hazırki Icon:</strong> 
                                <code class="current-icon-code">{}</code>
                                {}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="quick-actions">
                    <button type="button" class="quick-action-btn clear-icon" data-field="{}">
                        <i class="fas fa-times"></i> Təmizlə
                    </button>
                    <button type="button" class="quick-action-btn random-icon" data-field="{}">
                        <i class="fas fa-random"></i> Təsadüfi
                    </button>
                    <button type="button" class="quick-action-btn popular-icons" data-field="{}">
                        <i class="fas fa-star"></i> Populyar
                    </button>
                </div>
            </div>
            
            <script>
            {}
            </script>
        ''', 
            name,
            input_html,
            name,
            icon_preview,
            f"#{value.replace(' ', '').lower()}" if value else "#default",
            name,
            total_icons,
            icon_preview,
            value if value else '',
            current_icon_info,
            name,
            name,
            name,
            self.get_widget_script(name, total_icons)
        )
        
        return mark_safe(widget_html)
    
    def get_icon_preview(self, value):
        """Generate enhanced icon preview HTML"""
        if value and 'fa-' in value:
            return format_html('<i class="{}" style="font-size: 24px; color: #007bff;"></i>', value)
        else:
            return '<i class="fas fa-folder" style="font-size: 24px; color: #6c757d;"></i>'
    
    def get_icon_info(self, value):
        """Get detailed icon information"""
        if not value or 'fa-' not in value:
            return ""
        
        # Determine icon type
        if value.startswith('fab'):
            icon_type = 'Brand'
            type_color = '#fd7e14'
        elif value.startswith('far'):
            icon_type = 'Regular'  
            type_color = '#6f42c1'
        else:
            icon_type = 'Solid'
            type_color = '#007bff'
        
        # Clean icon name
        clean_name = value.replace('fas fa-', '').replace('far fa-', '').replace('fab fa-', '')
        formatted_name = clean_name.replace('-', ' ').title()
        
        return format_html('''
            <div class="icon-type-info">
                <span class="icon-type" style="background: {}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;">
                    {}
                </span>
                <span class="icon-name">{}</span>
            </div>
        ''', type_color, icon_type, formatted_name)
    
    def get_widget_script(self, field_name, total_icons):
        """Generate enhanced JavaScript for the widget"""
        # Convert Python dict to JavaScript object
        icon_db_js = self.python_dict_to_js(self.ICON_DATABASE)
        
        return format_html('''
            (function() {{
                // Enhanced namespace for field {}
                window.enhancedIconPicker_{} = {{
                    fieldName: '{}',
                    iconDatabase: {},
                    totalIcons: {},
                    
                    init: function() {{
                        this.attachEventListeners();
                        this.loadRecentIcons();
                        this.initQuickActions();
                    }},
                    
                    attachEventListeners: function() {{
                        const btn = document.querySelector('[data-target="{}"]');
                        if (btn) {{
                            btn.addEventListener('click', (e) => {{
                                e.preventDefault();
                                this.openEnhancedPicker();
                            }});
                        }}
                        
                        // Input change listener
                        const input = document.querySelector('input[name="{}"]');
                        if (input) {{
                            input.addEventListener('input', (e) => {{
                                this.updatePreview(e.target.value);
                                this.validateIcon(e.target.value);
                            }});
                        }}
                    }},
                    
                    openEnhancedPicker: function() {{
                        this.createEnhancedModal();
                    }},
                    
                    createEnhancedModal: function() {{
                        // Remove existing modal
                        const existingModal = document.getElementById('enhancedIconModal_{}');
                        if (existingModal) existingModal.remove();
                        
                        const modal = document.createElement('div');
                        modal.id = 'enhancedIconModal_{}';
                        modal.className = 'enhanced-icon-picker-modal';
                        modal.innerHTML = this.getModalHTML();
                        
                        document.body.appendChild(modal);
                        
                        // Show with animation
                        setTimeout(() => modal.classList.add('active'), 10);
                        
                        this.attachModalEvents();
                        this.loadModalContent();
                        
                        // Focus search after animation
                        setTimeout(() => {{
                            const searchInput = modal.querySelector('.search-input');
                            if (searchInput) searchInput.focus();
                        }}, 300);
                    }},
                    
                    getModalHTML: function() {{
                        return `
                            <div class="modal-backdrop"></div>
                            <div class="modal-container">
                                <div class="modal-header">
                                    <div class="header-content">
                                        <h2><i class="fas fa-palette"></i> Professional Icon Picker v2.0</h2>
                                        <p>${{this.totalIcons}} premium FontAwesome icons mövcuddur</p>
                                    </div>
                                    <button class="close-btn" onclick="window.enhancedIconPicker_{}.closeModal()">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                                
                                <div class="modal-controls">
                                    <div class="search-section">
                                        <div class="search-box">
                                            <i class="fas fa-search search-icon"></i>
                                            <input type="text" class="search-input" placeholder="Icon axtarın... (məs: heart, laptop, car)">
                                            <button class="clear-search" style="display: none;">
                                                <i class="fas fa-times"></i>
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <div class="filter-section">
                                        <div class="filter-tabs">
                                            <button class="filter-tab active" data-filter="all">
                                                <i class="fas fa-th"></i> Hamısı
                                            </button>
                                            <button class="filter-tab" data-filter="recent">
                                                <i class="fas fa-history"></i> Son İstifadə
                                            </button>
                                            <button class="filter-tab" data-filter="popular">
                                                <i class="fas fa-star"></i> Populyar
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="modal-content">
                                    <div class="category-navigation">
                                        <div class="category-list">
                                            <!-- Categories will be populated -->
                                        </div>
                                    </div>
                                    
                                    <div class="icons-display">
                                        <div class="icons-grid">
                                            <!-- Icons will be populated -->
                                        </div>
                                        
                                        <div class="loading-indicator" style="display: none;">
                                            <i class="fas fa-spinner fa-spin"></i>
                                            <span>İconlar yüklənir...</span>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="modal-footer">
                                    <div class="selection-preview">
                                        <div class="selected-icon-display">
                                            <i class="fas fa-folder"></i>
                                        </div>
                                        <div class="selection-info">
                                            <div class="selection-name"></div>
                                            <div class="selection-class">—</div>
                                        </div>
                                    </div>
                                    
                                    <div class="action-buttons">
                                        <button class="btn secondary" onclick="window.enhancedIconPicker_{}.closeModal()">
                                            <i class="fas fa-times"></i> Ləğv et
                                        </button>
                                        <button class="btn danger" onclick="window.enhancedIconPicker_{}.clearIcon()">
                                            <i class="fas fa-trash"></i> Təmizlə
                                        </button>
                                        <button class="btn primary" id="selectIconBtn" disabled onclick="window.enhancedIconPicker_{}.selectCurrentIcon()">
                                            <i class="fas fa-check"></i> Seç və Tətbiq et
                                        </button>
                                    </div>
                                </div>
                            </div>
                        `;
                    }},
                    
                    attachModalEvents: function() {{
                        const modal = document.getElementById('enhancedIconModal_{}');
                        
                        // Search functionality
                        const searchInput = modal.querySelector('.search-input');
                        searchInput.addEventListener('input', (e) => {{
                            this.handleSearch(e.target.value);
                            this.toggleClearButton(e.target.value);
                        }});
                        
                        // Clear search
                        modal.querySelector('.clear-search').addEventListener('click', () => {{
                            searchInput.value = '';
                            this.handleSearch('');
                            this.toggleClearButton('');
                        }});
                        
                        // Filter tabs
                        modal.querySelectorAll('.filter-tab').forEach(tab => {{
                            tab.addEventListener('click', (e) => {{
                                this.handleFilterChange(e.target.dataset.filter);
                                modal.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
                                e.target.classList.add('active');
                            }});
                        }});
                        
                        // Modal backdrop close
                        modal.querySelector('.modal-backdrop').addEventListener('click', () => {{
                            this.closeModal();
                        }});
                        
                        // Keyboard shortcuts
                        document.addEventListener('keydown', this.handleKeyboard.bind(this));
                    }},
                    
                    loadModalContent: function() {{
                        this.populateCategories();
                        this.populateAllIcons();
                    }},
                    
                    populateCategories: function() {{
                        const categoryList = document.querySelector('.category-list');
                        let html = '<button class="category-btn active" data-category="all"><i class="fas fa-th-large"></i> Hamısı</button>';
                        
                        for (const [category, icons] of Object.entries(this.iconDatabase)) {{
                            const iconCount = icons.length;
                            const categoryIcon = this.getCategoryIcon(category);
                            html += `
                                <button class="category-btn" data-category="${{category}}">
                                    <i class="fas fa-${{categoryIcon}}"></i> 
                                    ${{category}} 
                                    <span class="count">${{iconCount}}</span>
                                </button>
                            `;
                        }}
                        
                        categoryList.innerHTML = html;
                        
                        // Attach category click events
                        categoryList.querySelectorAll('.category-btn').forEach(btn => {{
                            btn.addEventListener('click', (e) => {{
                                const category = e.currentTarget.dataset.category;
                                this.showCategoryIcons(category);
                                
                                // Update active category
                                categoryList.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
                                e.currentTarget.classList.add('active');
                            }});
                        }});
                    }},
                    
                    populateAllIcons: function() {{
                        this.showAllIcons();
                    }},
                    
                    showAllIcons: function() {{
                        const iconsGrid = document.querySelector('.icons-grid');
                        let html = '';
                        
                        for (const [category, icons] of Object.entries(this.iconDatabase)) {{
                            html += `<div class="category-section">
                                <h4 class="category-title">${{category}} <span class="count">(${{icons.length}})</span></h4>
                                <div class="category-icons">`;
                            
                            icons.forEach(icon => {{
                                const iconClass = category === 'Brendlər' ? `fab fa-${{icon}}` : `fas fa-${{icon}}`;
                                const displayName = icon.replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
                                html += this.getIconHTML(iconClass, displayName, category);
                            }});
                            
                            html += '</div></div>';
                        }}
                        
                        iconsGrid.innerHTML = html;
                        this.attachIconClickEvents();
                    }},
                    
                    showCategoryIcons: function(category) {{
                        const iconsGrid = document.querySelector('.icons-grid');
                        
                        if (category === 'all') {{
                            this.showAllIcons();
                            return;
                        }}
                        
                        const icons = this.iconDatabase[category] || [];
                        let html = `<div class="category-section single">
                            <h4 class="category-title">${{category}} <span class="count">(${{icons.length}})</span></h4>
                            <div class="category-icons large">`;
                        
                        icons.forEach(icon => {{
                            const iconClass = category === 'Brendlər' ? `fab fa-${{icon}}` : `fas fa-${{icon}}`;
                            const displayName = icon.replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
                            html += this.getIconHTML(iconClass, displayName, category, true);
                        }});
                        
                        html += '</div></div>';
                        iconsGrid.innerHTML = html;
                        this.attachIconClickEvents();
                    }},
                    
                    getIconHTML: function(iconClass, displayName, category, large = false) {{
                        return `
                            <div class="icon-item ${{large ? 'large' : ''}}" 
                                 data-icon="${{iconClass}}" 
                                 data-name="${{displayName}}"
                                 data-category="${{category}}"
                                 title="${{displayName}} (${{iconClass}})">
                                <div class="icon-visual">
                                    <i class="${{iconClass}}"></i>
                                </div>
                                <div class="icon-info">
                                    <span class="icon-name">${{displayName}}</span>
                                    <small class="icon-class">${{iconClass}}</small>
                                </div>
                                <div class="category-badge">${{category}}</div>
                            </div>
                        `;
                    }},
                    
                    attachIconClickEvents: function() {{
                        document.querySelectorAll('.icon-item').forEach(item => {{
                            item.addEventListener('click', () => {{
                                this.selectIcon(item);
                            }});
                        }});
                    }},
                    
                    selectIcon: function(iconElement) {{
                        // Remove previous selections
                        document.querySelectorAll('.icon-item').forEach(item => {{
                            item.classList.remove('selected');
                        }});
                        
                        // Select current
                        iconElement.classList.add('selected');
                        
                        const iconClass = iconElement.dataset.icon;
                        const iconName = iconElement.dataset.name;
                        
                        // Update selection preview
                        const preview = document.querySelector('.selected-icon-display i');
                        const nameDisplay = document.querySelector('.selection-name');
                        const classDisplay = document.querySelector('.selection-class');
                        const selectBtn = document.getElementById('selectIconBtn');
                        
                        preview.className = iconClass;
                        nameDisplay.textContent = iconName;
                        classDisplay.textContent = iconClass;
                        selectBtn.disabled = false;
                        
                        this.selectedIcon = {{ class: iconClass, name: iconName }};
                    }},
                    
                    selectCurrentIcon: function() {{
                        if (!this.selectedIcon) return;
                        
                        this.applyIcon(this.selectedIcon.class);
                        this.saveRecentIcon(this.selectedIcon);
                        this.closeModal();
                    }},
                    
                    clearIcon: function() {{
                        this.applyIcon('');
                        this.closeModal();
                    }},
                    
                    applyIcon: function(iconClass) {{
                        const input = document.querySelector('input[name="{}"]');
                        const preview = document.getElementById('icon-preview-{}');
                        const codeDisplay = document.querySelector('.current-icon-code');
                        
                        if (input) {{
                            input.value = iconClass;
                            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                        
                        this.updatePreview(iconClass);
                        
                        if (iconClass) {{
                            this.showSuccessMessage(`✅ Icon seçildi: ${{iconClass}}`);
                        }} else {{
                            this.showSuccessMessage('🗑️ Icon təmizləndi');
                        }}
                    }},
                    
                    updatePreview: function(iconClass) {{
                        const preview = document.getElementById('icon-preview-{}');
                        const codeDisplay = document.querySelector('.current-icon-code');
                        
                        if (preview) {{
                            if (iconClass && iconClass.includes('fa-')) {{
                                preview.querySelector('i').className = iconClass;
                                preview.querySelector('small').textContent = `#${{iconClass.replace(' ', '').toLowerCase()}}`;
                            }} else {{
                                preview.querySelector('i').className = 'fas fa-folder';
                                preview.querySelector('small').textContent = '#default';
                            }}
                        }}
                        
                        if (codeDisplay) {{
                            codeDisplay.textContent = iconClass || '';
                        }}
                    }},
                    
                    validateIcon: function(iconClass) {{
                        // Add validation feedback
                        const input = document.querySelector('input[name="{}"]');
                        if (!input) return;
                        
                        if (iconClass && !iconClass.match(/^(fas|far|fab)\\s+fa-[a-z0-9-]+$/)) {{
                            input.classList.add('invalid');
                            input.title = 'Düzgün format: fas fa-icon-name';
                        }} else {{
                            input.classList.remove('invalid');
                            input.title = '';
                        }}
                    }},
                    
                    handleSearch: function(query) {{
                        // Search implementation
                        const items = document.querySelectorAll('.icon-item');
                        const sections = document.querySelectorAll('.category-section');
                        
                        if (!query) {{
                            items.forEach(item => item.style.display = 'flex');
                            sections.forEach(section => section.style.display = 'block');
                            return;
                        }}
                        
                        const lowerQuery = query.toLowerCase();
                        let visibleCount = 0;
                        
                        items.forEach(item => {{
                            const iconClass = item.dataset.icon.toLowerCase();
                            const iconName = item.dataset.name.toLowerCase();
                            const category = item.dataset.category.toLowerCase();
                            
                            if (iconClass.includes(lowerQuery) || iconName.includes(lowerQuery) || category.includes(lowerQuery)) {{
                                item.style.display = 'flex';
                                visibleCount++;
                            }} else {{
                                item.style.display = 'none';
                            }}
                        }});
                        
                        // Show/hide category sections
                        sections.forEach(section => {{
                            const hasVisibleItems = section.querySelectorAll('.icon-item[style*="flex"]').length > 0;
                            section.style.display = hasVisibleItems ? 'block' : 'none';
                        }});
                        
                        this.updateSearchResults(visibleCount);
                    }},
                    
                    toggleClearButton: function(query) {{
                        const clearBtn = document.querySelector('.clear-search');
                        clearBtn.style.display = query ? 'flex' : 'none';
                    }},
                    
                    updateSearchResults: function(count) {{
                        // Update search results counter
                        console.log(`Search results: ${{count}} icons found`);
                    }},
                    
                    handleFilterChange: function(filter) {{
                        // Handle filter changes
                        switch(filter) {{
                            case 'recent':
                                this.showRecentIcons();
                                break;
                            case 'popular':
                                this.showPopularIcons();
                                break;
                            default:
                                this.showAllIcons();
                        }}
                    }},
                    
                    showRecentIcons: function() {{
                        const recentIcons = this.getRecentIcons();
                        // Implementation for recent icons display
                    }},
                    
                    showPopularIcons: function() {{
                        const popularIcons = ['heart', 'star', 'home', 'user', 'envelope', 'phone'];
                        // Implementation for popular icons display
                    }},
                    
                    getCategoryIcon: function(category) {{
                        const categoryIcons = {{
                            'Səhiyyə': 'heartbeat',
                            'Elektronika': 'laptop',
                            'Geyim & Moda': 'tshirt',
                            'Nəqliyyat': 'car',
                            'Təhsil': 'graduation-cap',
                            'Əyləncə & İdman': 'gamepad',
                            'Yemək & İçki': 'utensils',
                            'Alətlər & Texnika': 'tools',
                            'Təbiət & Hava': 'tree',
                            'Musiqi & Səs': 'music',
                            'Təhlükəsizlik': 'shield-alt',
                            'Ev & Yaşayış': 'home',
                            'İş & Biznes': 'briefcase',
                            'Sosial & Ünsiyyət': 'users',
                            'Brendlər': 'apple'
                        }};
                        return categoryIcons[category] || 'folder';
                    }},
                    
                    handleKeyboard: function(e) {{
                        const modal = document.getElementById('enhancedIconModal_{}');
                        if (!modal || !modal.classList.contains('active')) return;
                        
                        switch(e.key) {{
                            case 'Escape':
                                this.closeModal();
                                break;
                            case 'Enter':
                                if (this.selectedIcon) {{
                                    this.selectCurrentIcon();
                                }}
                                break;
                        }}
                    }},
                    
                    closeModal: function() {{
                        const modal = document.getElementById('enhancedIconModal_{}');
                        if (modal) {{
                            modal.classList.remove('active');
                            setTimeout(() => modal.remove(), 300);
                        }}
                        document.removeEventListener('keydown', this.handleKeyboard);
                    }},
                    
                    initQuickActions: function() {{
                        // Clear icon
                        const clearBtn = document.querySelector('.quick-action-btn.clear-icon[data-field="{}"]');
                        if (clearBtn) {{
                            clearBtn.addEventListener('click', () => {{
                                this.applyIcon('');
                            }});
                        }}
                        
                        // Random icon
                        const randomBtn = document.querySelector('.quick-action-btn.random-icon[data-field="{}"]');
                        if (randomBtn) {{
                            randomBtn.addEventListener('click', () => {{
                                this.selectRandomIcon();
                            }});
                        }}
                        
                        // Popular icons
                        const popularBtn = document.querySelector('.quick-action-btn.popular-icons[data-field="{}"]');
                        if (popularBtn) {{
                            popularBtn.addEventListener('click', () => {{
                                this.showPopularIconsQuick();
                            }});
                        }}
                    }},
                    
                    selectRandomIcon: function() {{
                        const allIcons = [];
                        for (const [category, icons] of Object.entries(this.iconDatabase)) {{
                            icons.forEach(icon => {{
                                const iconClass = category === 'Brendlər' ? `fab fa-${{icon}}` : `fas fa-${{icon}}`;
                                allIcons.push(iconClass);
                            }});
                        }}
                        
                        const randomIcon = allIcons[Math.floor(Math.random() * allIcons.length)];
                        this.applyIcon(randomIcon);
                        this.showSuccessMessage(`🎲 Təsadüfi icon seçildi: ${{randomIcon}}`);
                    }},
                    
                    showPopularIconsQuick: function() {{
                        const popularIcons = [
                            'fas fa-heart', 'fas fa-star', 'fas fa-home', 'fas fa-user', 
                            'fas fa-envelope', 'fas fa-phone', 'fas fa-search', 'fas fa-cog'
                        ];
                        const randomPopular = popularIcons[Math.floor(Math.random() * popularIcons.length)];
                        this.applyIcon(randomPopular);
                        this.showSuccessMessage(`⭐ Populyar icon seçildi: ${{randomPopular}}`);
                    }},
                    
                    saveRecentIcon: function(icon) {{
                        let recent = JSON.parse(localStorage.getItem('recentIcons_{}') || '[]');
                        recent = recent.filter(r => r.class !== icon.class);
                        recent.unshift(icon);
                        recent = recent.slice(0, 20);
                        localStorage.setItem('recentIcons_{}', JSON.stringify(recent));
                    }},
                    
                    getRecentIcons: function() {{
                        return JSON.parse(localStorage.getItem('recentIcons_{}') || '[]');
                    }},
                    
                    loadRecentIcons: function() {{
                        this.recentIcons = this.getRecentIcons();
                    }},
                    
                    showSuccessMessage: function(message) {{
                        const success = document.createElement('div');
                        success.className = 'icon-success-message';
                        success.textContent = message;
                        document.body.appendChild(success);
                        setTimeout(() => success.remove(), 3000);
                    }}
                }};
                
                // Initialize when DOM is ready
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', () => {{
                        window.enhancedIconPicker_{}.init();
                    }});
                }} else {{
                    window.enhancedIconPicker_{}.init();
                }}
            }})();
        ''', 
            field_name, field_name, field_name, icon_db_js, total_icons,
            field_name, field_name, field_name, field_name, field_name, 
            field_name, field_name, field_name, field_name, field_name,
            field_name, field_name, field_name, field_name, field_name,
            field_name, field_name, field_name, field_name, field_name,
            field_name, field_name, field_name, field_name, field_name,
            field_name, field_name, field_name
        )
    
    def python_dict_to_js(self, py_dict):
        """Convert Python dictionary to JavaScript object string"""
        js_obj = "{\n"
        for key, value in py_dict.items():
            js_obj += f'    "{key}": {value},\n'
        js_obj = js_obj.rstrip(',\n') + "\n}"
        return js_obj
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'admin/css/icon-admin-enhanced.css',
            )
        }
        js = (
            'admin/js/icon-picker-integration.js',
        )


class ColorPickerWidget(forms.TextInput):
    """
    Enhanced Color Picker Widget with preview
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'type': 'color',
            'class': 'color-picker enhanced'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        if not value:
            value = '#007bff'  # Default color
        
        attrs = {**self.attrs, **attrs}
        attrs['value'] = value
        
        input_html = super().render(name, value, attrs, renderer)
        
        widget_html = format_html('''
            <div class="color-picker-widget enhanced">
                <div class="color-input-group">
                    {}
                    <div class="color-preview" style="background-color: {};" title="Hazırki rəng: {}">
                        <div class="color-hex">{}</div>
                    </div>
                    <div class="color-presets">
                        <button type="button" class="preset-color" data-color="#007bff" style="background: #007bff;" title="Mavi"></button>
                        <button type="button" class="preset-color" data-color="#28a745" style="background: #28a745;" title="Yaşıl"></button>
                        <button type="button" class="preset-color" data-color="#dc3545" style="background: #dc3545;" title="Qırmızı"></button>
                        <button type="button" class="preset-color" data-color="#ffc107" style="background: #ffc107;" title="Sarı"></button>
                        <button type="button" class="preset-color" data-color="#6f42c1" style="background: #6f42c1;" title="Bənövşəyi"></button>
                        <button type="button" class="preset-color" data-color="#fd7e14" style="background: #fd7e14;" title="Narıncı"></button>
                    </div>
                </div>
                <div class="color-info">
                    <small>Rəng kodu: <code>{}</code></small>
                </div>
            </div>
            
            <script>
            (function() {{
                const colorInput = document.querySelector('input[name="{}"]');
                const preview = colorInput.closest('.color-picker-widget').querySelector('.color-preview');
                const hexDisplay = preview.querySelector('.color-hex');
                const codeDisplay = colorInput.closest('.color-picker-widget').querySelector('code');
                
                colorInput.addEventListener('input', function(e) {{
                    const color = e.target.value;
                    preview.style.backgroundColor = color;
                    preview.title = 'Hazırki rəng: ' + color;
                    hexDisplay.textContent = color;
                    codeDisplay.textContent = color;
                }});
                
                // Preset colors
                const presetButtons = colorInput.closest('.color-picker-widget').querySelectorAll('.preset-color');
                presetButtons.forEach(btn => {{
                    btn.addEventListener('click', function(e) {{
                        e.preventDefault();
                        const color = this.dataset.color;
                        colorInput.value = color;
                        colorInput.dispatchEvent(new Event('input'));
                    }});
                }});
            }})();
            </script>
        ''', 
            input_html, value, value, value, value, name
        )
        
        return mark_safe(widget_html)


class PriorityWidget(forms.NumberInput):
    """
    Enhanced Priority Number Input Widget with visual indicators
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'min': '0',
            'max': '999',
            'class': 'priority-input enhanced',
            'style': 'width: 120px; text-align: center; font-weight: bold; font-size: 16px;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = 0
        
        attrs = {**self.attrs, **attrs}
        input_html = super().render(name, value, attrs, renderer)
        
        # Priority level indicator
        priority_level = self.get_priority_level(value)
        priority_color = self.get_priority_color(value)
        
        widget_html = format_html('''
            <div class="priority-widget enhanced">
                <div class="priority-input-wrapper">
                    {}
                    <div class="priority-controls">
                        <button type="button" class="priority-btn up" title="Artır">
                            <i class="fas fa-chevron-up"></i>
                        </button>
                        <button type="button" class="priority-btn down" title="Azalt">
                            <i class="fas fa-chevron-down"></i>
                        </button>
                    </div>
                </div>
                <div class="priority-indicator" style="background: {};">
                    <span class="level">{}</span>
                    <span class="value">{}</span>
                </div>
                <div class="priority-presets">
                    <button type="button" class="preset-priority" data-priority="0" style="background: #6f42c1;">TOP</button>
                    <button type="button" class="preset-priority" data-priority="1" style="background: #28a745;">HIGH</button>
                    <button type="button" class="preset-priority" data-priority="5" style="background: #ffc107; color: black;">MID</button>
                    <button type="button" class="preset-priority" data-priority="10" style="background: #dc3545;">LOW</button>
                </div>
            </div>
            
            <script>
            (function() {{
                const input = document.querySelector('input[name="{}"]');
                const wrapper = input.closest('.priority-widget');
                const indicator = wrapper.querySelector('.priority-indicator');
                const levelSpan = indicator.querySelector('.level');
                const valueSpan = indicator.querySelector('.value');
                
                function updateIndicator(val) {{
                    const level = getPriorityLevel(val);
                    const color = getPriorityColor(val);
                    
                    indicator.style.background = color;
                    levelSpan.textContent = level;
                    valueSpan.textContent = val;
                }}
                
                function getPriorityLevel(value) {{
                    if (value == 0) return 'TOP';
                    if (value >= 1 && value <= 3) return 'HIGH';
                    if (value >= 4 && value <= 7) return 'MID';
                    return 'LOW';
                }}
                
                function getPriorityColor(value) {{
                    if (value == 0) return '#6f42c1';
                    if (value >= 1 && value <= 3) return '#28a745';
                    if (value >= 4 && value <= 7) return '#ffc107';
                    return '#dc3545';
                }}
                
                // Control buttons
                wrapper.querySelector('.priority-btn.up').addEventListener('click', function(e) {{
                    e.preventDefault();
                    const currentValue = parseInt(input.value) || 0;
                    const newValue = Math.min(currentValue + 1, 999);
                    input.value = newValue;
                    updateIndicator(newValue);
                    input.dispatchEvent(new Event('change'));
                }});
                
                wrapper.querySelector('.priority-btn.down').addEventListener('click', function(e) {{
                    e.preventDefault();
                    const currentValue = parseInt(input.value) || 0;
                    const newValue = Math.max(currentValue - 1, 0);
                    input.value = newValue;
                    updateIndicator(newValue);
                    input.dispatchEvent(new Event('change'));
                }});
                
                // Preset buttons
                wrapper.querySelectorAll('.preset-priority').forEach(btn => {{
                    btn.addEventListener('click', function(e) {{
                        e.preventDefault();
                        const priority = parseInt(this.dataset.priority);
                        input.value = priority;
                        updateIndicator(priority);
                        input.dispatchEvent(new Event('change'));
                    }});
                }});
                
                // Input change listener
                input.addEventListener('input', function() {{
                    updateIndicator(parseInt(this.value) || 0);
                }});
                
                // Initialize
                updateIndicator(parseInt(input.value) || 0);
            }})();
            </script>
        ''', input_html, priority_color, priority_level, value, name)
        
        return mark_safe(widget_html)
    
    def get_priority_level(self, value):
        """Priority səviyyəsini qaytarır"""
        if not value or value == 0:
            return "TOP"
        elif 1 <= value <= 3:
            return "HIGH"
        elif 4 <= value <= 7:
            return "MID"
        else:
            return "LOW"
    
    def get_priority_color(self, value):
        """Priority rəngini qaytarır"""
        if not value or value == 0:
            return "#6f42c1"
        elif 1 <= value <= 3:
            return "#28a745"
        elif 4 <= value <= 7:
            return "#ffc107"
        else:
            return "#dc3545"

    class Media:
        css = {
            'all': ('admin/css/icon-admin-enhanced.css',)
        }
        js = (
            'admin/js/priority-manager.js',
        )