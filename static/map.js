
function initialize() {
    var data = JSON.parse('{{ data | safe }}');
    var map = L.map('map').setView([48.833, 2.333], 7);
    for (var i = data.length-1 ; i>=0;i-- ) {
        L.marker([ data[i][1] , data[i][2]]).addTo(map) .bindTooltip( (data[i][0]), {permanent: false, direction: 'top'});
        }
    var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors',maxZoom: 19 });
    map.addLayer(osmLayer);
}
