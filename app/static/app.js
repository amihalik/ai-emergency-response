// Simple waveform animation placeholder
const path = document.getElementById('wavePath');
let t = 0;
setInterval(() => {
  const points = Array.from({length: 30}, (_, i) => {
    const y = 30 + Math.sin(i / 2 + t) * 20;
    return `${i*10},${y}`;
  });
  path.setAttribute('d', 'M' + points.join(' L'));
  t += 0.1;
}, 100);

// Transcript auto-scroll
const transcript = document.querySelector('.transcript-log');
let autoScroll = true;
if (transcript) {
  transcript.addEventListener('mouseover', () => autoScroll = false);
  transcript.addEventListener('mouseout', () => autoScroll = true);
}

function appendTranscript(role, text) {
  const div = document.createElement('div');
  div.innerHTML = `<span class="${role}">${role}:</span> ${text}`;
  transcript.appendChild(div);
  if (autoScroll) transcript.scrollTop = transcript.scrollHeight;
}

// Mapbox map
if (typeof mapboxgl !== 'undefined') {
  mapboxgl.accessToken = 'YOUR_MAPBOX_TOKEN';
  const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v10',
    center: [-122.4194, 37.7749],
    zoom: 3
  });
  const marker = new mapboxgl.Marker({color: '#e64d46'})
    .setLngLat([-122.4194, 37.7749])
    .setPopup(new mapboxgl.Popup().setText('Pinned location'))
    .addTo(map);
}

// Dummy resource updates
const resources = document.querySelector('.nearest-resources ul');
function updateResources() {
  const items = [
    {type:'police', label:'Unit 12 - 2 min'},
    {type:'fire', label:'Engine 5 - 5 min'},
    {type:'hospital', label:'Ambulance 3 - 7 min'}
  ];
  resources.innerHTML = '';
  items.forEach(i => {
    const li = document.createElement('li');
    li.className = i.type;
    li.textContent = i.label;
    resources.appendChild(li);
  });
}
setInterval(updateResources, 5000);
updateResources();
