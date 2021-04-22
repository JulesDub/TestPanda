
        function initialize() {
            console.log(JSON);
            var ID = JSON.parse('{{ ID | safe}}');
            var Lat = JSON.parse('{{ Lat | safe}}');
            var Long = JSON.parse('{{ Long | safe}}');
            var map = L.map('map').setView([48.833, 2.333], 7);
            for (var i = Lat.length -1 ; i>=0;i-- ) { //Créer un marqueur avec le nom[i], la latitude[i] et la longitude[i]
                L.marker([ Lat[i][0] , Long[i][0]]).addTo(map) .bindTooltip( (ID[i][0]), {permanent: false, direction: 'top'});
             }
            var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { // LIGNE 20
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
            });

            map.addLayer(osmLayer);
             }
