/**
 * NIVORA – Leaflet.js Map & Geolocation Engine
 * Handles interactive maps, Bangalore area markers, distance circles, and browser geolocation.
 */

// Bangalore Center Default Coordinates
const BANGALORE_DEFAULT = [12.9716, 77.5946];

// Area Coordinates Dictionary for quick client-side lookup & Admin auto-fill
const BANGALORE_AREA_COORDS = {
  'Koramangala': { lat: 12.9352, lng: 77.6245 },
  'Indiranagar': { lat: 12.9784, lng: 77.6408 },
  'HSR Layout': { lat: 12.9121, lng: 77.6446 },
  'BTM Layout': { lat: 12.9166, lng: 77.6101 },
  'Whitefield': { lat: 12.9698, lng: 77.7499 },
  'Electronic City': { lat: 12.8452, lng: 77.6602 },
  'Bellandur': { lat: 12.9304, lng: 77.6784 },
  'Marathahalli': { lat: 12.9591, lng: 77.6974 },
  'Jayanagar': { lat: 12.9308, lng: 77.5838 },
  'Sarjapur Road': { lat: 12.9098, lng: 77.6853 },
  'Bommanahalli': { lat: 12.9015, lng: 77.6231 },
  'Hebbal': { lat: 13.0358, lng: 77.5970 },
  'Rajajinagar': { lat: 12.9982, lng: 77.5530 },
  'Yelahanka': { lat: 13.1007, lng: 77.5963 },
  'Mahadevapura': { lat: 12.9868, lng: 77.6888 }
};

let searchMap = null;
let searchMarkersLayer = null;
let userLocationMarker = null;

/**
 * Initialize Search Map
 */
function initSearchMap(listingsData, userLat, userLon) {
  const mapElement = document.getElementById('search-map');
  if (!mapElement) return;

  // Determine center
  let initialCenter = BANGALORE_DEFAULT;
  let initialZoom = 12;

  if (userLat && userLon) {
    initialCenter = [userLat, userLon];
    initialZoom = 13;
  } else if (listingsData && listingsData.length > 0) {
    initialCenter = [listingsData[0].latitude, listingsData[0].longitude];
  }

  // Initialize Leaflet Map
  searchMap = L.map('search-map', {
    scrollWheelZoom: true,
    zoomControl: true
  }).setView(initialCenter, initialZoom);

  // Add OpenStreetMap Tile Layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | NIVORA'
  }).addTo(searchMap);

  searchMarkersLayer = L.layerGroup().addTo(searchMap);

  // If user location is passed, show User Marker
  if (userLat && userLon) {
    addUserMarker(userLat, userLon, 'Your Location');
  }

  // Add PG Markers
  if (listingsData && listingsData.length > 0) {
    renderPGMarkers(listingsData);
  }
}

/**
 * Custom Gold Leaflet Icon for PGs
 */
function createGoldMarkerIcon(rent) {
  return L.divIcon({
    className: 'custom-gold-marker',
    html: `
      <div style="
        background: #0E0E0E;
        color: #D4AF37;
        border: 2px solid #D4AF37;
        border-radius: 20px;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        gap: 4px;
        white-space: nowrap;
        transform: translate(-50%, -50%);
      ">
        <i class="fa-solid fa-house" style="font-size: 9px;"></i> ₹${rent >= 1000 ? (rent / 1000).toFixed(1) + 'k' : rent}
      </div>
    `,
    iconSize: [60, 24],
    iconAnchor: [30, 12]
  });
}

/**
 * Render PGs onto Map with Rich Popups
 */
function renderPGMarkers(pgs) {
  if (!searchMarkersLayer) return;
  searchMarkersLayer.clearLayers();

  const bounds = [];

  pgs.forEach(pg => {
    if (pg.latitude && pg.longitude) {
      const marker = L.marker([pg.latitude, pg.longitude], {
        icon: createGoldMarkerIcon(pg.monthly_rent)
      });

      const distBadge = pg.distance_km != null 
        ? `<div style="font-size: 11px; color: #2A9D8F; font-weight: 600; margin-bottom: 4px;">
             <i class="fa-solid fa-location-arrow"></i> ${pg.distance_km} km away
           </div>`
        : '';

      const popupHtml = `
        <div class="map-popup-card">
          <img src="/static/${pg.primary_photo}" class="map-popup-img" alt="${pg.name}" onerror="this.src='/static/images/pg/placeholder.svg';">
          <div class="map-popup-body">
            <div style="font-size: 10px; color: #D4AF37; font-weight: 700; text-transform: uppercase;">
              ${pg.area} • ${pg.gender_category}
            </div>
            <div class="map-popup-title">${pg.name}</div>
            ${distBadge}
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
              <span class="map-popup-rent">₹${pg.monthly_rent.toLocaleString()}<small style="font-size: 10px; color: #999;">/mo</small></span>
              <a href="/pg/${pg.id}" class="btn-gold" style="padding: 4px 10px; font-size: 11px; text-decoration: none;">
                View PG
              </a>
            </div>
          </div>
        </div>
      `;

      marker.bindPopup(popupHtml, { maxWidth: 280 });
      searchMarkersLayer.addLayer(marker);
      bounds.push([pg.latitude, pg.longitude]);
    }
  });

  // Fit bounds if markers exist and not zoomed into user
  if (bounds.length > 0 && !userLocationMarker) {
    searchMap.fitBounds(bounds, { padding: [40, 40] });
  }
}

/**
 * Add / Update User Location Marker on Map
 */
function addUserMarker(lat, lon, label = 'Your Location') {
  if (!searchMap) return;

  if (userLocationMarker) {
    searchMap.removeLayer(userLocationMarker);
  }

  const userIcon = L.divIcon({
    className: 'custom-user-marker',
    html: `
      <div style="
        background: #0077B6;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        box-shadow: 0 0 15px rgba(0, 119, 182, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        animation: pulse 2s infinite;
      ">
        <i class="fa-solid fa-person-walking"></i>
      </div>
    `,
    iconSize: [22, 22],
    iconAnchor: [11, 11]
  });

  userLocationMarker = L.marker([lat, lon], { icon: userIcon }).addTo(searchMap);
  userLocationMarker.bindPopup(`<strong>📍 ${label}</strong>`).openPopup();
  searchMap.setView([lat, lon], 14);
}

/**
 * Browser Geolocation Trigger
 * Asks browser permission gracefully.
 */
function triggerBrowserGeolocation(onSuccess, onError) {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by your current browser. Please select an area manually.");
    if (onError) onError("Not supported");
    return;
  }

  const statusText = document.getElementById('geoStatusText');
  if (statusText) statusText.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Detecting your current location...';

  navigator.geolocation.getCurrentPosition(
    position => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      if (statusText) statusText.innerHTML = `📍 Location detected: ${lat.toFixed(4)}, ${lon.toFixed(4)}`;
      if (onSuccess) onSuccess(lat, lon);
    },
    error => {
      let msg = "Could not detect location.";
      if (error.code === error.PERMISSION_DENIED) {
        msg = "Location permission was denied. You can still search by selecting any Bangalore area.";
      } else if (error.code === error.POSITION_UNAVAILABLE) {
        msg = "Location information is currently unavailable.";
      } else if (error.code === error.TIMEOUT) {
        msg = "Location request timed out. Please try again.";
      }
      if (statusText) statusText.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-warning"></i> ${msg}`;
      if (onError) onError(msg);
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
  );
}

/**
 * Mini Map for PG Details Page
 */
function initDetailMap(lat, lon, title, address) {
  const mapElement = document.getElementById('detail-map');
  if (!mapElement || !lat || !lon) return;

  const detailMap = L.map('detail-map', {
    scrollWheelZoom: false,
    zoomControl: true
  }).setView([lat, lon], 15);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap | NIVORA'
  }).addTo(detailMap);

  const marker = L.marker([lat, lon]).addTo(detailMap);
  marker.bindPopup(`<strong>${title}</strong><br><small>${address}</small>`).openPopup();
}

/**
 * Helper for Admin PG Add/Edit form:
 * When user selects an area from dropdown, auto-populate default Latitude and Longitude.
 */
function setupAdminAreaCoordAutoFill() {
  const areaSelect = document.getElementById('area');
  const latInput = document.getElementById('latitude');
  const lonInput = document.getElementById('longitude');

  if (areaSelect && latInput && lonInput) {
    areaSelect.addEventListener('change', function () {
      const selectedArea = this.value;
      if (BANGALORE_AREA_COORDS[selectedArea]) {
        // Only autofill if fields are empty or 0
        if (!latInput.value || latInput.value === '0' || latInput.value === '0.0') {
          latInput.value = BANGALORE_AREA_COORDS[selectedArea].lat;
          lonInput.value = BANGALORE_AREA_COORDS[selectedArea].lng;
        }
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  setupAdminAreaCoordAutoFill();
});

