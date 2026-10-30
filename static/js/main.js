/**
 * NIVORA – Core JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Sticky Navbar styling on scroll
  const navbar = document.querySelector('.nivora-navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 30) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // 2. Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      try {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      } catch (e) {
        alert.remove();
      }
    }, 5000);
  });

  // 3. Favourites AJAX toggle
  document.querySelectorAll('.fav-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const pgId = this.getAttribute('data-pg-id');
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

      if (!pgId) return;

      fetch(`/api/toggle-favourite/${pgId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken || ''
        }
      })
      .then(response => {
        if (response.status === 401) {
          window.location.href = `/login?next=${encodeURIComponent(window.location.pathname)}`;
          return null;
        }
        return response.json();
      })
      .then(data => {
        if (!data) return;
        if (data.success) {
          if (data.favourited) {
            this.classList.add('active');
            this.innerHTML = '<i class="fa-solid fa-heart"></i>';
            showToast('Saved to Favourites', 'success');
          } else {
            this.classList.remove('active');
            this.innerHTML = '<i class="fa-regular fa-heart"></i>';
            showToast('Removed from Favourites', 'info');
            // If on favorites page, remove the card dynamically
            if (window.location.pathname.includes('/favorites')) {
              const cardCol = this.closest('.pg-card-col');
              if (cardCol) {
                cardCol.style.transition = 'all 0.3s ease';
                cardCol.style.opacity = '0';
                cardCol.style.transform = 'scale(0.9)';
                setTimeout(() => cardCol.remove(), 300);
              }
            }
          }
        }
      })
      .catch(err => {
        console.error('Error toggling favourite:', err);
      });
    });
  });

  // 4. Detail Image Gallery Thumbnail Switcher
  const mainImage = document.getElementById('detailMainImage');
  const thumbs = document.querySelectorAll('.detail-thumb');
  if (mainImage && thumbs.length > 0) {
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', function () {
        thumbs.forEach(t => t.classList.remove('active'));
        this.classList.add('active');
        const newSrc = this.getAttribute('data-src');
        if (newSrc) {
          mainImage.src = newSrc;
        }
      });
    });
  }
});

// Toast notification helper
function showToast(message, type = 'info') {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.style.position = 'fixed';
    container.style.bottom = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `alert alert-${type === 'success' ? 'success' : 'dark'} shadow-lg py-2 px-3 mb-2`;
  toast.style.borderRadius = '8px';
  toast.style.fontSize = '0.9rem';
  toast.style.borderLeft = '4px solid #D4AF37';
  toast.style.background = '#0E0E0E';
  toast.style.color = '#FFFFFF';
  toast.innerHTML = `<i class="fa-solid fa-circle-info text-gold me-2"></i> ${message}`;

  document.getElementById('toast-container').appendChild(toast);
  setTimeout(() => {
    toast.style.transition = 'opacity 0.4s ease';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

