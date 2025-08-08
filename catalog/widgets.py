# catalog/widgets.py - Your structure compatible

from django import forms
from django.utils.safestring import mark_safe

class IconPickerWidget(forms.TextInput):
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css',
                'admin/css/icon-admin-enhanced.css',  # Your static structure
            )
        }
        js = (
            'admin/js/icon-picker-integration.js',  # Your static structure
        )
    
    def render(self, name, value, attrs=None, renderer=None):
        html_input = super().render(name, value, attrs, renderer)
        current_icon = value or 'fas fa-folder'
        
        # ÇOX DAHA ÇOX ICONLAR
        all_icons = {
            'Səhiyyə': ['heartbeat', 'user-md', 'pills', 'syringe', 'first-aid', 'stethoscope', 'thermometer', 'tooth', 'eye', 'hospital', 'ambulance', 'band-aid'],
            'Elektronika': ['laptop', 'mobile-alt', 'desktop', 'tablet', 'keyboard', 'mouse', 'headphones', 'tv', 'camera', 'video', 'microphone', 'usb', 'wifi', 'bluetooth'],
            'Geyim': ['tshirt', 'shoe-prints', 'hat-cowboy', 'glasses', 'ring', 'gem', 'crown', 'mask', 'umbrella', 'backpack', 'handbag', 'shopping-bag'],
            'Nəqliyyat': ['car', 'truck', 'motorcycle', 'bicycle', 'plane', 'train', 'bus', 'taxi', 'ship', 'rocket', 'helicopter', 'subway'],
            'Təhsil': ['book', 'graduation-cap', 'pencil-alt', 'pen', 'bookmark', 'newspaper', 'file-alt', 'folder', 'archive', 'clipboard', 'calculator', 'ruler'],
            'Əyləncə': ['gamepad', 'dice', 'chess', 'puzzle-piece', 'magic', 'gift', 'birthday-cake', 'balloon', 'party-horn', 'fireworks', 'ticket-alt'],
            'Yemək': ['utensils', 'coffee', 'wine-bottle', 'beer', 'pizza-slice', 'hamburger', 'ice-cream', 'apple-alt', 'carrot', 'fish', 'bread-slice', 'cheese'],
            'Alətlər': ['hammer', 'wrench', 'screwdriver', 'paint-roller', 'brush', 'toolbox', 'hard-hat', 'bolt', 'cog', 'gear', 'cut', 'magnet'],
            'Təbiət': ['tree', 'leaf', 'seedling', 'flower', 'sun', 'moon', 'cloud', 'rainbow', 'snowflake', 'fire', 'mountain', 'water'],
            'Musiqi': ['music', 'volume-up', 'play', 'pause', 'stop', 'forward', 'backward', 'random', 'repeat', 'guitar', 'drum', 'violin'],
            'Təhlükəsizlik': ['shield-alt', 'lock', 'key', 'fingerprint', 'user-secret', 'mask', 'eye-slash', 'unlock', 'safe', 'vault', 'crown', 'badge'],
            'Ev': ['home', 'couch', 'bed', 'chair', 'door-open', 'lightbulb', 'plug', 'shower', 'toilet', 'kitchen-set', 'stairs', 'window-maximize'],
            'İş': ['briefcase', 'building', 'city', 'industry', 'store', 'warehouse', 'handshake', 'chart-bar', 'presentation', 'calculator', 'balance-scale'],
            'İdman': ['running', 'dumbbell', 'futbol', 'basketball-ball', 'tennis-ball', 'volleyball-ball', 'table-tennis', 'golf-ball', 'hockey-puck', 'medal'],
            'Sosial': ['users', 'user-friends', 'user-plus', 'comments', 'share-alt', 'thumbs-up', 'thumbs-down', 'heart', 'star', 'fire', 'trophy'],
            'Brendlər': ['apple', 'google', 'microsoft', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin', 'github', 'whatsapp', 'telegram', 'discord', 'spotify', 'netflix', 'amazon', 'paypal']
        }
        
        widget_html = f'''
        <div class="icon-picker-widget" data-field-name="{name}">
            <div style="display: flex; align-items: center; gap: 12px; margin: 10px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef;">
                {html_input}
                <div id="icon-preview-{name}" style="width: 44px; height: 44px; border: 2px solid #e9ecef; border-radius: 6px; display: flex; align-items: center; justify-content: center; background: white;">
                    <i class="{current_icon}" style="font-size: 20px; color: #495057;"></i>
                </div>
                <button type="button" id="icon-btn-{name}" style="padding: 10px 16px; background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 13px;">
                    <i class="fas fa-palette"></i> Icon Seç ({len(sum(all_icons.values(), []))})
                </button>
            </div>
            <div style="padding-top: 8px; border-top: 1px solid #e9ecef; margin-top: 8px;">
                <small style="color: #6c757d;">Hazırki: <code style="background: #e7f3ff; color: #007bff; padding: 2px 6px; border-radius: 3px;">{value or 'Heç bir icon seçilməyib'}</code></small>
            </div>
        </div>

        <script>
        (function() {{
            // Unique namespace for this field
            window.iconPicker_{name} = {{
                fieldName: '{name}',
                
                openPicker: function() {{
                    // Remove existing modal if any
                    const existingModal = document.getElementById('iconModal_{name}');
                    if (existingModal) existingModal.remove();
                    
                    let iconContent = '';
                    const categories = {all_icons};
                    
                    // Generate categories and icons
                    for (const [category, icons] of Object.entries(categories)) {{
                        iconContent += `<div style="margin: 20px 0;">
                            <h4 style="color: #007bff; margin: 15px 0 10px 0; font-size: 14px; border-bottom: 2px solid #e9ecef; padding-bottom: 5px;">${{category}} (${{icons.length}} icon)</h4>
                            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(90px, 1fr)); gap: 8px;">`;
                        
                        icons.forEach(icon => {{
                            const iconClass = category === 'Brendlər' ? `fab fa-${{icon}}` : `fas fa-${{icon}}`;
                            iconContent += `
                                <div class="icon-selector" 
                                     data-icon="${{iconClass}}" 
                                     style="cursor: pointer; padding: 12px 8px; border: 2px solid #e9ecef; border-radius: 8px; text-align: center; background: #f8f9fa; transition: all 0.2s ease; min-height: 80px; display: flex; flex-direction: column; align-items: center; justify-content: center;"
                                     onmouseover="this.style.borderColor='#007bff'; this.style.background='white'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(0,123,255,0.15)'"
                                     onmouseout="this.style.borderColor='#e9ecef'; this.style.background='#f8f9fa'; this.style.transform='translateY(0)'; this.style.boxShadow='none'"
                                     onclick="window.iconPicker_{name}.selectIcon('${{iconClass}}')">
                                    <i class="${{iconClass}}" style="font-size: 24px; color: #495057; margin-bottom: 6px;"></i>
                                    <small style="font-size: 10px; color: #6c757d; font-weight: 500;">${{icon.replace('-', ' ')}}</small>
                                </div>
                            `;
                        }});
                        
                        iconContent += '</div></div>';
                    }}
                    
                    // Create modal
                    const modal = document.createElement('div');
                    modal.id = 'iconModal_{name}';
                    modal.style.cssText = `
                        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                        background: rgba(0,0,0,0.6); z-index: 10000; display: flex; 
                        align-items: center; justify-content: center; backdrop-filter: blur(3px);
                    `;
                    
                    modal.innerHTML = `
                        <div style="background: white; border-radius: 16px; width: 90%; max-width: 900px; max-height: 85vh; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); animation: modalSlideIn 0.3s ease;">
                            <div style="background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; padding: 20px 30px; text-align: center;">
                                <h3 style="margin: 0; font-size: 20px;">🎨 Professional Icon Picker</h3>
                                <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 14px;">{len(sum(all_icons.values(), []))} premium icon mövcuddur</p>
                            </div>
                            
                            <div style="padding: 0 30px;">
                                <div style="margin: 20px 0; text-align: center;">
                                    <input type="text" id="iconSearch_{name}" placeholder="Icon axtarın... (məs: heart, laptop, car)" 
                                           style="width: 60%; padding: 10px 15px; border: 2px solid #e9ecef; border-radius: 25px; font-size: 14px; outline: none;" 
                                           onkeyup="window.iconPicker_{name}.searchIcons(this.value)">
                                </div>
                            </div>
                            
                            <div id="iconContent_{name}" style="padding: 0 30px; max-height: 450px; overflow-y: auto;">
                                ${{iconContent}}
                            </div>
                            
                            <div style="padding: 20px 30px; border-top: 1px solid #eee; text-align: right; background: #f8f9fa;">
                                <button onclick="window.iconPicker_{name}.closeModal()" 
                                        style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; margin-right: 10px;">
                                    <i class="fas fa-times"></i> Ləğv et
                                </button>
                                <button onclick="window.iconPicker_{name}.clearIcon()" 
                                        style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px;">
                                    <i class="fas fa-trash"></i> Təmizlə
                                </button>
                            </div>
                        </div>
                    `;
                    
                    document.body.appendChild(modal);
                    
                    // Close on background click
                    modal.addEventListener('click', function(e) {{
                        if (e.target === modal) window.iconPicker_{name}.closeModal();
                    }});
                    
                    // Focus search
                    setTimeout(() => {{
                        const searchInput = document.getElementById('iconSearch_{name}');
                        if (searchInput) searchInput.focus();
                    }}, 100);
                }},
                
                selectIcon: function(iconClass) {{
                    const input = document.querySelector('input[name="{name}"]');
                    const preview = document.getElementById('icon-preview-{name}');
                    
                    if (input && preview) {{
                        input.value = iconClass;
                        preview.innerHTML = `<i class="${{iconClass}}" style="font-size: 20px; color: #495057;"></i>`;
                        
                        // Update current selection text
                        const currentSelection = input.closest('.icon-picker-widget').querySelector('code');
                        if (currentSelection) currentSelection.textContent = iconClass;
                        
                        // Trigger change event
                        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                    
                    this.closeModal();
                    this.showSuccess(`✅ Seçildi: ${{iconClass}}`);
                }},
                
                clearIcon: function() {{
                    const input = document.querySelector('input[name="{name}"]');
                    const preview = document.getElementById('icon-preview-{name}');
                    
                    if (input && preview) {{
                        input.value = '';
                        preview.innerHTML = '<i class="fas fa-folder" style="font-size: 20px; color: #6c757d;"></i>';
                        
                        const currentSelection = input.closest('.icon-picker-widget').querySelector('code');
                        if (currentSelection) currentSelection.textContent = 'Heç bir icon seçilməyib';
                    }}
                    
                    this.closeModal();
                    this.showSuccess('🗑️ Icon təmizləndi');
                }},
                
                searchIcons: function(query) {{
                    const content = document.getElementById('iconContent_{name}');
                    if (!content) return;
                    
                    const iconSelectors = content.querySelectorAll('.icon-selector');
                    iconSelectors.forEach(selector => {{
                        const iconClass = selector.dataset.icon.toLowerCase();
                        const iconName = selector.querySelector('small').textContent.toLowerCase();
                        
                        if (iconClass.includes(query.toLowerCase()) || iconName.includes(query.toLowerCase())) {{
                            selector.style.display = 'flex';
                        }} else {{
                            selector.style.display = 'none';
                        }}
                    }});
                }},
                
                closeModal: function() {{
                    const modal = document.getElementById('iconModal_{name}');
                    if (modal) modal.remove();
                }},
                
                showSuccess: function(message) {{
                    const success = document.createElement('div');
                    success.style.cssText = `
                        position: fixed; top: 20px; right: 20px; background: #28a745; 
                        color: white; padding: 12px 20px; border-radius: 8px; z-index: 10001;
                        font-weight: 500; box-shadow: 0 4px 12px rgba(40,167,69,0.3);
                        animation: slideInRight 0.3s ease;
                    `;
                    success.textContent = message;
                    document.body.appendChild(success);
                    setTimeout(() => success.remove(), 3000);
                }}
            }};
            
            // Add animations
            const style = document.createElement('style');
            style.textContent = `
                @keyframes modalSlideIn {{
                    from {{ opacity: 0; transform: scale(0.8) translateY(-20px); }}
                    to {{ opacity: 1; transform: scale(1) translateY(0); }}
                }}
                @keyframes slideInRight {{
                    from {{ opacity: 0; transform: translateX(100px); }}
                    to {{ opacity: 1; transform: translateX(0); }}
                }}
            `;
            document.head.appendChild(style);
            
            // Attach click event with delay to ensure DOM is ready
            setTimeout(function() {{
                const btn = document.getElementById('icon-btn-{name}');
                if (btn) {{
                    btn.addEventListener('click', function(e) {{
                        e.preventDefault();
                        window.iconPicker_{name}.openPicker();
                    }});
                }}
            }}, 200);
        }})();
        </script>
        '''
        
        return mark_safe(widget_html)