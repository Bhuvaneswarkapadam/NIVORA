/**
 * NIVORA – Search & Filter Controller
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Budget Range Sliders synchronization
  const maxRentInput = document.getElementById('max_rent');
  const maxRentDisplay = document.getElementById('max_rent_display');

  if (maxRentInput && maxRentDisplay) {
    maxRentInput.addEventListener('input', function () {
      const val = parseInt(this.value, 10);
      maxRentDisplay.textContent = '₹' + val.toLocaleString();
    });
  }

  // 2. "Find My Location" Button in Hero & Search
  const geoBtns = document.querySelectorAll('.btn-detect-location');
  geoBtns.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const originalText = this.innerHTML;
      this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Locating...';

      triggerBrowserGeolocation(
        (lat, lon) => {
          this.innerHTML = '<i class="fa-solid fa-check text-success"></i> Located!';
          
          // If on search page, fill hidden coordinates and submit
          const latField = document.getElementById('search_lat');
          const lonField = document.getElementById('search_lon');
          const searchForm = document.getElementById('searchForm');

          if (latField && lonField && searchForm) {
            latField.value = lat;
            lonField.value = lon;
            const sortSelect = document.getElementById('sort');
            if (sortSelect) sortSelect.value = 'distance';
            searchForm.submit();
          } else {
            // Redirect to search page with lat and lon
            window.location.href = `/search?lat=${lat}&lon=${lon}&sort=distance&location_name=My+Current+Location`;
          }
        },
        error => {
          this.innerHTML = originalText;
          showToast(error, 'warning');
        }
      );
    });
  });

  // 3. Clear filters action
  const clearBtn = document.getElementById('clearFiltersBtn');
  if (clearBtn) {
    clearBtn.addEventListener('click', function (e) {
      e.preventDefault();
      window.location.href = '/search';
    });
  }

  // 4. Map vs List View Toggle for Mobile & Tablet
  const viewToggleBtns = document.querySelectorAll('[data-view-toggle]');
  const listView = document.getElementById('search-list-col');
  const mapView = document.getElementById('search-map-col');

  if (viewToggleBtns.length > 0 && listView && mapView) {
    viewToggleBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        viewToggleBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        const mode = this.getAttribute('data-view-toggle');
        if (mode === 'list') {
          listView.classList.remove('d-none');
          mapView.classList.add('d-none');
        } else if (mode === 'map') {
          listView.classList.add('d-none');
          mapView.classList.remove('d-none');
          if (searchMap) searchMap.invalidateSize();
        } else { // 'split'
          listView.classList.remove('d-none');
          mapView.classList.remove('d-none');
          if (searchMap) searchMap.invalidateSize();
        }
      });
    });
  }
});

