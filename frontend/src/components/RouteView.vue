<template>
    <template v-for="point in points" v-bind:key="point['coordinates'][1]">
        <start-marker :point="point" v-if="point.start">
            <slot>Hi!</slot>
        </start-marker>
        <finish-marker :point="point" v-else-if="point.finish"></finish-marker>
        <station-marker :point="point" v-else></station-marker>
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
                    coordinates: station.coordinates,
                    name: station['name']
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