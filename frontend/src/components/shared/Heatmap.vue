<template>
    <div ref="map" style="height: 500px;"> </div>
</template>

<script>
import L from 'leaflet';

export default {
    name: 'heatmap',
    props: ['coordinates'],
    data() {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            map: null,
            heatmap: null,
            mapOptions: {
                center: L.latLng(0, 0),
                minZoom: 2,
                maxZoom: 12,
                maxBounds: L.latLngBounds([-90, -180], [90, 180]),
            },
            heatOptions: {
                radius: 10,
                maxZoom: 2,
            }
        }
    },
    mounted() {
        this.refresh();
        setTimeout(() => this.heatmap.addTo(this.map), 100);
        setTimeout(() => this.map.invalidateSize(), 100);
    },
    methods: {
        refresh() {
            if (this.map) {
                this.map.off();
                this.map.remove();
            }
            this.map = L.map(this.$refs.map, this.mapOptions).setView([0, 0], 2);
            L.tileLayer(this.url, {attribution: this.attribution}).addTo(this.map);
            if (this.coordinates)
                this.heatmap = L.heatLayer(this.coordinates, this.heatOptions).addTo(this.map);
        },
    },
    watch: {
        coordinates() {
            this.refresh();
        }
    }
}
</script>


<style scoped>

</style>