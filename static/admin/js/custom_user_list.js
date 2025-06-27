// Custom JavaScript for Enhanced User List Admin Page

document.addEventListener('DOMContentLoaded', function() {
    // Add user statistics dashboard
    addUserStatsDashboard();

    // Enhance boolean field displays
    enhanceBooleanFields();

    // Add tooltips for truncated content
    addTooltips();

    // Add loading states
    addLoadingStates();

    // Enhance search functionality
    enhanceSearch();
});

function addUserStatsDashboard() {
    const resultList = document.querySelector('.change-list .results tbody');
    if (!resultList) return;

    const rows = resultList.querySelectorAll('tr');
    if (rows.length === 0) return;

    let totalUsers = rows.length;
    let activeUsers = 0;
    let adminUsers = 0;
    let supervisorUsers = 0;
    let pgUsers = 0;

    rows.forEach(row => {
        // Count active users - look for the status display
        const statusCell = row.querySelector('.field-get_status_display');
        if (statusCell && statusCell.textContent.includes('✅')) {
            activeUsers++;
        }

        // Count roles - look for the role display
        const roleCell = row.querySelector('.field-get_role_display');
        if (roleCell) {
            const roleText = roleCell.textContent.toLowerCase();
            if (roleText.includes('🔴') || roleText.includes('admin')) {
                adminUsers++;
            } else if (roleText.includes('🟠') || roleText.includes('supervisor')) {
                supervisorUsers++;
            } else if (roleText.includes('🟢') || roleText.includes('pg')) {
                pgUsers++;
            }
        }
    });

    // Create stats dashboard HTML
    const statsHTML = `
        <div class="user-stats">
            <div class="stat-item">
                <span>👥 Total Users:</span>
                <span class="stat-number">${totalUsers}</span>
            </div>
            <div class="stat-item">
                <span>✅ Active:</span>
                <span class="stat-number">${activeUsers}</span>
            </div>
            <div class="stat-item">
                <span>🔴 Admins:</span>
                <span class="stat-number">${adminUsers}</span>
            </div>
            <div class="stat-item">
                <span>🟠 Supervisors:</span>
                <span class="stat-number">${supervisorUsers}</span>
            </div>
            <div class="stat-item">
                <span>🟢 PGs:</span>
                <span class="stat-number">${pgUsers}</span>
            </div>
        </div>
    `;

    // Insert stats dashboard
    const changeList = document.querySelector('.change-list');
    const searchForm = document.querySelector('.search-form');

    if (changeList) {
        if (searchForm) {
            searchForm.insertAdjacentHTML('afterend', statsHTML);
        } else {
            changeList.insertAdjacentHTML('afterbegin', statsHTML);
        }
    }
}

function enhanceBooleanFields() {
    // Enhance the status display fields if they're using default Django boolean display
    document.querySelectorAll('.field-is_active img').forEach(img => {
        const isTrue = img.getAttribute('alt') === 'True';
        const parent = img.parentElement;
        parent.innerHTML = isTrue ?
            '<span style="color: #28a745; font-weight: 500;">✅ Active</span>' :
            '<span style="color: #dc3545; font-weight: 500;">❌ Inactive</span>';
    });

    // Add role color indicators if they're not already there
    document.querySelectorAll('.field-role').forEach(roleCell => {
        const roleText = roleCell.textContent.trim().toLowerCase();
        if (!roleCell.textContent.includes('🔴') && !roleCell.textContent.includes('🟠') && !roleCell.textContent.includes('🟢')) {
            let indicator = '';

            if (roleText.includes('admin')) {
                indicator = '🔴 ';
            } else if (roleText.includes('supervisor')) {
                indicator = '🟠 ';
            } else if (roleText.includes('pg') || roleText.includes('postgraduate')) {
                indicator = '🟢 ';
            }

            if (indicator) {
                roleCell.innerHTML = indicator + roleCell.textContent;
            }
        }
    });
}

function addTooltips() {
    // Add tooltips to cells that might be truncated
    document.querySelectorAll('.change-list .results td').forEach(cell => {
        if (cell.scrollWidth > cell.clientWidth) {
            const fullText = cell.textContent.trim();
            if (fullText && !cell.getAttribute('title')) {
                cell.setAttribute('title', fullText);
                cell.style.cursor = 'help';
            }
        }
    });

    // Add descriptive tooltips to action buttons
    const addButton = document.querySelector('.object-tools a');
    if (addButton && !addButton.getAttribute('title')) {
        addButton.setAttribute('title', 'Add a new user to the system');
    }

    // Add tooltips to filter options
    document.querySelectorAll('#changelist-filter a').forEach(link => {
        if (!link.getAttribute('title')) {
            const filterText = link.textContent.trim();
            if (filterText && filterText !== 'All') {
                link.setAttribute('title', `Filter by: ${filterText}`);
            }
        }
    });
}

function addLoadingStates() {
    // Add loading state to pagination links
    document.querySelectorAll('.paginator a').forEach(link => {
        link.addEventListener('click', function() {
            this.style.opacity = '0.6';
            this.style.pointerEvents = 'none';

            // Create loading spinner
            const spinner = document.createElement('span');
            spinner.innerHTML = ' ⏳';
            spinner.className = 'loading-spinner';
            this.appendChild(spinner);
        });
    });

    // Add loading state to action buttons
    document.querySelectorAll('.actions button').forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit') {
                this.style.opacity = '0.6';
                this.innerHTML = '⏳ Processing...';
            }
        });
    });
}

function enhanceSearch() {
    const searchInput = document.querySelector('.search-form input[type="text"]');
    if (!searchInput) return;

    // Add placeholder text if not already set
    if (!searchInput.getAttribute('placeholder')) {
        searchInput.setAttribute('placeholder', 'Search users by name, email, or username...');
    }

    // Add search enhancement
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);

        // Add visual feedback for search
        this.style.borderColor = '#ffc107';

        searchTimeout = setTimeout(() => {
            this.style.borderColor = '#e9ecef';
        }, 500);
    });

    // Enhance the search form submission
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            const submitButton = this.querySelector('input[type="submit"]');
            if (submitButton) {
                submitButton.value = '🔍 Searching...';
                submitButton.style.opacity = '0.8';
            }
        });
    }
}

// Utility function to format dates nicely
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('en-US', options);
}

// Add keyboard shortcuts for better accessibility
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-form input[type="text"]');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }

    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInput = document.querySelector('.search-form input[type="text"]');
        if (searchInput && document.activeElement === searchInput) {
            searchInput.value = '';
            searchInput.blur();
        }
    }
});

// Add smooth scrolling for better UX
function addSmoothScrolling() {
    document.documentElement.style.scrollBehavior = 'smooth';
}

// Initialize smooth scrolling
addSmoothScrolling();

// Add visual feedback for successful actions
function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #d4edda;
        color: #155724;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        font-weight: 500;
        border: 1px solid #c3e6cb;
    `;
    successDiv.textContent = message;

    document.body.appendChild(successDiv);

    setTimeout(() => {
        successDiv.style.opacity = '0';
        successDiv.style.transition = 'opacity 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(successDiv);
        }, 300);
    }, 3000);
}

// Check for Django messages and enhance them
const djangoMessages = document.querySelectorAll('.messagelist .success, .messagelist .info');
djangoMessages.forEach(message => {
    message.style.cssText += `
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease;
    `;
});

// Add CSS animation for messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateY(-20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
