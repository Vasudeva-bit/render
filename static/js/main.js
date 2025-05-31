// Notifications polling
function pollNotifications() {
    fetch('/api/notifications/count')
        .then(response => response.json())
        .then(data => {
            const count = data.count;
            const badge = document.getElementById('notification-badge');
            if (badge) {
                badge.textContent = count > 0 ? count : '';
                badge.style.display = count > 0 ? 'inline' : 'none';
            }
        });
}

// Unread messages polling
function pollUnreadMessages() {
    fetch('/api/unread_messages')
        .then(response => response.json())
        .then(data => {
            const count = data.count;
            const badge = document.getElementById('messages-badge');
            if (badge) {
                badge.textContent = count > 0 ? count : '';
                badge.style.display = count > 0 ? 'inline' : 'none';
            }
        });
}

// Update timestamps to relative time
function updateTimestamps() {
    document.querySelectorAll('.timestamp').forEach(el => {
        const timestamp = new Date(el.getAttribute('data-time'));
        el.textContent = getRelativeTimeString(timestamp);
    });
}

function getRelativeTimeString(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHour = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHour / 24);

    if (diffDay > 30) {
        return date.toLocaleDateString();
    } else if (diffDay > 0) {
        return `${diffDay}d ago`;
    } else if (diffHour > 0) {
        return `${diffHour}h ago`;
    } else if (diffMin > 0) {
        return `${diffMin}m ago`;
    } else {
        return 'just now';
    }
}

// Start polling if elements exist
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('notification-badge')) {
        pollNotifications();
        setInterval(pollNotifications, 30000);
    }
    if (document.getElementById('messages-badge')) {
        pollUnreadMessages();
        setInterval(pollUnreadMessages, 30000);
    }
    updateTimestamps();
    setInterval(updateTimestamps, 60000);
});
