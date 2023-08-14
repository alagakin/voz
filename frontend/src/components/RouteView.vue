<template>
    <template v-for="point in points" v-bind:key="point.coordinates[0]">
        <start-marker :lat-lng="point.coordinates" v-if="point.start"></start-marker>
        <finish-marker :lat-lng="point.coordinates" v-else-if="point.finish"></finish-marker>
        <station-marker :lat-lng="point.coordinates" v-else></station-marker>
    </template>
</template>
<script>
import FinishMarker from "@/components/markers/FinishMarker.vue";
import StartMarker from "@/components/markers/StartMarker.vue";
import StationMarker from "@/components/markers/StationMarker.vue";
export default {
    components: {StationMarker, StartMarker, FinishMarker},
    props: {
        stations: {
            type: Array
        }
    },
    watch: {
        stations() {
            this.points = []
            this.stations.forEach((station, index) => {
                let point = {
                    coordinates: station.coordinates
                }
                if (index === 0) {
                    point.start = true
                }
                if (index === this.stations.length - 1) {
                    point.finish = true
                }
                this.points.push(point)
            })
        }
    },
    data() {
        return {
            points: []
        }
    }
}

</script>