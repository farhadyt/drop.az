/* static/admin/js/priority-manager.js - Priority Management for drop.az */

(function($) {
    'use strict';

    // Global priority management functions
    window.setPriority = function(categoryId, priorityValue) {
        const csrfToken = $('[name=csrfmiddlewaretoken]').val() || 
                         document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                         getCsrfTokenFromCookie();
        
        if (!csrfToken) {
            alert('CSRF token tapılmadı. Səhifəni yeniləyin.');
            return;
        }

        // Show loading indicator
        showAdminMessage('Priority dəyişdirilir...', 'info');

        // AJAX request to update priority
        $.ajax({
            url: `/admin/catalog/category/${categoryId}/change/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data: {
                'priority': priorityValue,
                'csrfmiddlewaretoken': csrfToken,
                '_continue': 'Təqdim et və redaktəyə davam et'
            },
            success: function(response) {
                // Show success message
                showAdminMessage(`✅ Priority ${priorityValue} uğurla təyin edildi!`, 'success');
                
                // Update the display without full page reload
                updatePriorityDisplay(categoryId, priorityValue);
                
                // Update cache
                invalidateCategoryCache();
                
                // Optionally reload the page after a short delay
                setTimeout(() => {
                    if (confirm('Dəyişikliklər tətbiq edildi. Səhifəni yeniləmək istəyirsiniz?')) {
                        window.location.reload();
                    }
                }, 2000);
            },
            error: function(xhr, status, error) {
                console.error('Priority update error:', error);
                showAdminMessage(`❌ Xəta: Priority dəyişdirilmədi. ${error}`, 'error');
                
                // Fallback: redirect to edit page
                if (confirm('Xəta baş verdi. Edit səhifəsini açmaq istəyirsiniz?')) {
                    window.open(`/admin/catalog/category/${categoryId}/change/`, '_blank');
                }
            }
        });
    };

    // Get CSRF token from cookie
    function getCsrfTokenFromCookie() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Show admin message with different types
    function showAdminMessage(message, type) {
        // Remove existing messages
        $('.admin-priority-message').remove();
        
        // Define colors for different message types
        const typeColors = {
            'success': '#28a745',
            'error': '#dc3545',
            'warning': '#ffc107',
            'info': '#007bff'
        };
        
        // Create new message
        const messageDiv = $(`
            <div class="admin-priority-message alert alert-${type}" style="
                position: fixed;
                top: 100px;
                right: 20px;
                z-index: 9999;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                background: ${typeColors[type] || '#007bff'};
                min-width: 300px;
                max-width: 500px;
                animation: slideInRight 0.3s ease;
            ">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fas ${getIconForType(type)}"></i>
                    <span>${message}</span>
                    <button onclick="$(this).closest('.admin-priority-message').remove()" style="
                        background: none;
                        border: none;
                        color: white;
                        cursor: pointer;
                        font-size: 16px;
                        margin-left: auto;
                        padding: 0;
                    ">×</button>
                </div>
            </div>
        `);
        
        $('body').append(messageDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.fadeOut(300, () => messageDiv.remove());
        }, 5000);
    }

    // Get icon for message type
    function getIconForType(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || 'fa-info-circle';
    }

    // Update priority display in table
    function updatePriorityDisplay(categoryId, newPriority) {
        // Find the priority cell for this category
        const priorityCell = $(`.priority-display[data-category-id="${categoryId}"]`);
        if (priorityCell.length) {
            let color, badge, level;
            
            if (newPriority == 0) {
                color = '#6f42c1';
                badge = 'TOP';
                level = 'TOP';
            } else if (newPriority >= 1 && newPriority <= 3) {
                color = '#28a745';
                badge = 'HIGH';
                level = 'HIGH';
            } else if (newPriority >= 4 && newPriority <= 7) {
                color = '#ffc107';
                badge = 'MID';
                level = 'MEDIUM';
            } else {
                color = '#dc3545';
                badge = 'LOW';
                level = 'LOW';
            }
            
            priorityCell.html(`
                <div style="display: flex; align-items: center; gap: 5px;">
                    <div style="text-align: center;">
                        <div style="background: ${color}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 11px; margin-bottom: 2px;">${badge}</div>
                        <div style="font-size: 18px; font-weight: bold; color: ${color};">${newPriority}</div>
                    </div>
                    <div class="priority-buttons" style="margin-left: 8px;">
                        <button type="button" onclick="setPriority(${categoryId}, 0)" style="background: #6f42c1; color: white; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="TOP">0</button>
                        <button type="button" onclick="setPriority(${categoryId}, 1)" style="background: #28a745; color: white; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="HIGH">H</button>
                        <button type="button" onclick="setPriority(${categoryId}, 5)" style="background: #ffc107; color: black; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="MID">M</button>
                        <button type="button" onclick="setPriority(${categoryId}, 10)" style="background: #dc3545; color: white; border: none; padding: 2px 6px; border-radius: 3px; font-size: 10px; cursor: pointer; margin: 1px;" title="LOW">L</button>
                    </div>
                </div>
            `);
            
            // Add animation effect
            priorityCell.addClass('updated').delay(2000).queue(function() {
                $(this).removeClass('updated').dequeue();
            });
        }
    }

    // Invalidate category cache
    function invalidateCategoryCache() {
        // Send request to clear category cache
        $.ajax({
            url: '/api/clear-category-cache/',
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfTokenFromCookie()
            },
            success: function() {
                console.log('Category cache cleared');
            },
            error: function() {
                console.log('Cache clear failed, but priority was updated');
            }
        });
    }

    // Enhanced priority input styling and functionality
    $(document).ready(function() {
        // Style priority inputs
        $('.priority-input').each(function() {
            const $input = $(this);
            const $wrapper = $('<div class="priority-input-wrapper"></div>');
            
            $input.wrap($wrapper);
            $wrapper.append(`
                <div class="priority-buttons">
                    <button type="button" class="priority-btn priority-up" title="Artır (+1)">↑</button>
                    <button type="button" class="priority-btn priority-down" title="Azalt (-1)">↓</button>
                </div>
            `);
            
            // Add priority level indicator
            updatePriorityIndicator($input);
            
            // Add event handlers for up/down buttons
            $wrapper.find('.priority-up').on('click', function(e) {
                e.preventDefault();
                const currentValue = parseInt($input.val()) || 0;
                const newValue = Math.min(currentValue + 1, 999);
                $input.val(newValue);
                updatePriorityIndicator($input);
                $input.trigger('change');
                showAdminMessage(`Priority artırıldı: ${newValue}`, 'info');
            });
            
            $wrapper.find('.priority-down').on('click', function(e) {
                e.preventDefault();
                const currentValue = parseInt($input.val()) || 0;
                const newValue = Math.max(currentValue - 1, 0);
                $input.val(newValue);
                updatePriorityIndicator($input);
                $input.trigger('change');
                showAdminMessage(`Priority azaldıldı: ${newValue}`, 'info');
            });
            
            // Update indicator on input change
            $input.on('input change', function() {
                updatePriorityIndicator($(this));
            });
            
            // Add keyboard shortcuts
            $input.on('keydown', function(e) {
                if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    $wrapper.find('.priority-up').click();
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    $wrapper.find('.priority-down').click();
                }
            });
        });

        // Enhanced priority column sorting
        $('.column-priority_display').on('click', function() {
            showAdminMessage('📊 Priority sütunu ilə sıralama aktiv!', 'success');
        });

        // Add bulk priority actions
        if ($('#changelist-form').length) {
            addBulkPriorityActions();
        }

        // Add priority statistics
        if ($('.results').length) {
            addPriorityStatistics();
        }

        // Add CSS animations
        addAnimations();

        console.log('🎯 Priority Manager v2.0 loaded successfully!');
    });

    // Update priority level indicator
    function updatePriorityIndicator($input) {
        const value = parseInt($input.val()) || 0;
        const level = getPriorityLevel(value);
        const color = getPriorityColor(value);
        
        // Remove existing indicator
        $input.siblings('.priority-level-indicator').remove();
        
        // Add new indicator
        const indicator = $(`
            <div class="priority-level-indicator" style="
                position: absolute;
                right: 25px;
                top: 50%;
                transform: translateY(-50%);
                background: ${color};
                color: white;
                padding: 2px 6px;
                border-radius: 3px;
                font-size: 10px;
                font-weight: bold;
                pointer-events: none;
                z-index: 5;
            ">${level}</div>
        `);
        
        $input.parent().append(indicator);
    }

    // Get priority level
    function getPriorityLevel(value) {
        if (value === 0) return 'TOP';
        if (value >= 1 && value <= 3) return 'HIGH';
        if (value >= 4 && value <= 7) return 'MID';
        return 'LOW';
    }

    // Get priority color
    function getPriorityColor(value) {
        if (value === 0) return '#6f42c1';
        if (value >= 1 && value <= 3) return '#28a745';
        if (value >= 4 && value <= 7) return '#ffc107';
        return '#dc3545';
    }

    // Add bulk priority change actions
    function addBulkPriorityActions() {
        const $actionBar = $('.actions');
        if ($actionBar.length) {
            const bulkPriorityHtml = `
                <div class="bulk-priority-actions" style="margin: 15px 0; padding: 15px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 8px; border-left: 4px solid #007bff;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                        <strong style="color: #007bff; font-size: 16px;">🎯 Bulk Priority Actions</strong>
                        <small style="color: #6c757d;">Seçilmiş kateqoriyaların priority-sini dəyişin</small>
                    </div>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <button type="button" class="btn-bulk-priority" data-priority="0" style="background: #6f42c1; color: white;">
                            <i class="fas fa-crown"></i> TOP (0)
                        </button>
                        <button type="button" class="btn-bulk-priority" data-priority="1" style="background: #28a745; color: white;">
                            <i class="fas fa-arrow-up"></i> HIGH (1)
                        </button>
                        <button type="button" class="btn-bulk-priority" data-priority="5" style="background: #ffc107; color: black;">
                            <i class="fas fa-equals"></i> MID (5)
                        </button>
                        <button type="button" class="btn-bulk-priority" data-priority="10" style="background: #dc3545; color: white;">
                            <i class="fas fa-arrow-down"></i> LOW (10)
                        </button>
                        <button type="button" id="btn-priority-reset" style="background: #6c757d; color: white;">
                            <i class="fas fa-undo"></i> Reset All
                        </button>
                    </div>
                </div>
            `;
            
            $actionBar.after(bulkPriorityHtml);
            
            // Add click handlers for bulk actions
            $('.btn-bulk-priority').on('click', function() {
                const priority = $(this).data('priority');
                const selectedItems = $('input[name="_selected_action"]:checked');
                
                if (selectedItems.length === 0) {
                    showAdminMessage('❌ Ən azı bir kateqoriya seçin!', 'error');
                    return;
                }
                
                const priorityText = getPriorityLevel(priority);
                if (confirm(`${selectedItems.length} kateqoriyanın priority-sini ${priorityText} (${priority}) təyin etmək istəyirsiniz?`)) {
                    bulkSetPriority(selectedItems, priority);
                }
            });
            
            // Reset all priorities
            $('#btn-priority-reset').on('click', function() {
                const selectedItems = $('input[name="_selected_action"]:checked');
                
                if (selectedItems.length === 0) {
                    showAdminMessage('❌ Ən azı bir kateqoriya seçin!', 'error');
                    return;
                }
                
                if (confirm(`${selectedItems.length} kateqoriyanın priority-sini sıfırlamaq istəyirsiniz? (0-a təyin ediləcək)`)) {
                    bulkSetPriority(selectedItems, 0);
                }
            });
        }
    }

    // Add priority statistics display
    function addPriorityStatistics() {
        // Calculate statistics from current page
        let stats = {
            top: 0,
            high: 0,
            medium: 0,
            low: 0,
            total: 0
        };
        
        $('.priority-display').each(function() {
            const text = $(this).text();
            stats.total++;
            
            if (text.includes('TOP')) stats.top++;
            else if (text.includes('HIGH')) stats.high++;
            else if (text.includes('MID')) stats.medium++;
            else if (text.includes('LOW')) stats.low++;
        });
        
        if (stats.total > 0) {
            const statsHtml = `
                <div class="priority-statistics" style="margin: 10px 0; padding: 12px; background: linear-gradient(135deg, #e7f3ff 0%, #cce7ff 100%); border-radius: 6px; border-left: 4px solid #007bff;">
                    <strong style="color: #007bff;">📊 Priority Statistics (Current Page):</strong>
                    <div style="display: flex; gap: 15px; margin-top: 8px; flex-wrap: wrap;">
                        <span style="background: #6f42c1; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px;">
                            👑 TOP: ${stats.top}
                        </span>
                        <span style="background: #28a745; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px;">
                            ⬆️ HIGH: ${stats.high}
                        </span>
                        <span style="background: #ffc107; color: black; padding: 3px 8px; border-radius: 4px; font-size: 12px;">
                            ➡️ MID: ${stats.medium}
                        </span>
                        <span style="background: #dc3545; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px;">
                            ⬇️ LOW: ${stats.low}
                        </span>
                        <span style="background: #17a2b8; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px;">
                            📈 TOTAL: ${stats.total}
                        </span>
                    </div>
                </div>
            `;
            
            $('.results').prepend(statsHtml);
        }
    }

    // Bulk priority update with progress tracking
    function bulkSetPriority(selectedItems, priority) {
        let completed = 0;
        const total = selectedItems.length;
        const priorityText = getPriorityLevel(priority);
        
        // Show progress message
        showAdminMessage(`🔄 ${total} kateqoriya üçün priority ${priorityText} (${priority}) təyin edilir...`, 'info');
        
        // Create progress bar
        const progressBar = $(`
            <div id="bulk-progress" style="
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: white;
                border: 2px solid #007bff;
                border-radius: 8px;
                padding: 15px;
                min-width: 300px;
                z-index: 10000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            ">
                <div style="margin-bottom: 10px; font-weight: bold; color: #007bff;">
                    📊 Bulk Priority Update Progress
                </div>
                <div style="background: #f8f9fa; height: 20px; border-radius: 10px; overflow: hidden; margin-bottom: 8px;">
                    <div id="progress-fill" style="background: linear-gradient(90deg, #007bff, #28a745); height: 100%; width: 0%; transition: width 0.3s ease;"></div>
                </div>
                <div id="progress-text">0 / ${total} completed</div>
            </div>
        `);
        
        $('body').append(progressBar);
        
        selectedItems.each(function(index) {
            const categoryId = $(this).val();
            setTimeout(() => {
                setPriorityWithCallback(categoryId, priority, () => {
                    completed++;
                    const percentage = (completed / total) * 100;
                    
                    // Update progress bar
                    $('#progress-fill').css('width', percentage + '%');
                    $('#progress-text').text(`${completed} / ${total} completed`);
                    
                    if (completed === total) {
                        setTimeout(() => {
                            $('#bulk-progress').fadeOut(300, function() {
                                $(this).remove();
                            });
                        }, 1500);
                        
                        showAdminMessage(`✅ ${total} kateqoriyanın priority-si ${priorityText} (${priority}) təyin edildi!`, 'success');
                        
                        setTimeout(() => {
                            if (confirm('Bütün dəyişikliklər tamamlandı! Səhifəni yeniləmək istəyirsiniz?')) {
                                window.location.reload();
                            }
                        }, 3000);
                    }
                });
            }, index * 300); // Stagger requests by 300ms
        });
    }

    // Priority update with callback
    function setPriorityWithCallback(categoryId, priorityValue, callback) {
        const csrfToken = getCsrfTokenFromCookie();
        
        $.ajax({
            url: `/admin/catalog/category/${categoryId}/change/`,
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            data: {
                'priority': priorityValue,
                'csrfmiddlewaretoken': csrfToken,
                '_continue': 'Təqdim et və redaktəyə davam et'
            },
            success: function(response) {
                updatePriorityDisplay(categoryId, priorityValue);
                if (callback) callback();
            },
            error: function(xhr, status, error) {
                console.error(`Category ${categoryId} priority update failed:`, error);
                if (callback) callback(); // Continue with other items even if one fails
            }
        });
    }

    // Add CSS animations
    function addAnimations() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes priorityUpdate {
                0% { background-color: #fff3cd; }
                50% { background-color: #ffeaa7; }
                100% { background-color: transparent; }
            }
            
            .priority-display.updated {
                animation: priorityUpdate 2s ease;
            }
            
            .priority-input-wrapper {
                position: relative;
                display: inline-block;
            }
            
            .priority-buttons {
                position: absolute;
                right: 2px;
                top: 2px;
                display: flex;
                flex-direction: column;
                gap: 1px;
            }
            
            .priority-btn {
                width: 20px;
                height: 14px;
                border: none;
                background: #6c757d;
                color: white;
                font-size: 10px;
                cursor: pointer;
                border-radius: 2px;
                transition: all 0.2s ease;
            }
            
            .priority-btn:hover {
                background: #007bff;
                transform: scale(1.1);
            }
            
            .priority-up:hover {
                background: #28a745;
            }
            
            .priority-down:hover {
                background: #dc3545;
            }
            
            .btn-bulk-priority {
                padding: 8px 12px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: 500;
                font-size: 12px;
                transition: all 0.2s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .btn-bulk-priority:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }
            
            @media (max-width: 768px) {
                .priority-buttons {
                    flex-direction: row;
                    position: static;
                    margin-top: 5px;
                    justify-content: center;
                }
                
                .bulk-priority-actions > div:last-child {
                    flex-direction: column;
                }
                
                .btn-bulk-priority {
                    width: 100%;
                    justify-content: center;
                }
            }
        `;
        document.head.appendChild(style);
    }

})(django.jQuery || jQuery);