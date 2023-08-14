<template>
    <template v-for="point in points" v-bind:key="point['coordinates'][1]">
        <start-marker :point="point" v-if="point.start">
            <slot>Hi!</slot>
        </start-marker>
        <finish-marker :point="point" v-else-if="point.finish"></finish-marker>
        <station-marker :point="point" v-else></station-marker>

    </template>
    <ArrowMarker v-for="arrow in arrows" :start="arrow[0]" :end="arrow[1]" v-bind:key="arrow"  />
</template>
<script>
import FinishMarker from "@/components/markers/FinishMarker.vue";
import StartMarker from "@/components/markers/StartMarker.vue";
import StationMarker from "@/components/markers/StationMarker.vue";
import ArrowMarker from "@/components/markers/ArrowMarker.vue";

export default {
    components: {ArrowMarker, StationMarker, StartMarker, FinishMarker},
    props: {
        stations: {
            type: Array
        }
    },
    watch: {
        stations() {
            this.points = []
            this.arrows = []
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
                if (index > 0) {
                    this.arrows.push([
                        this.points[this.points.length - 1].coordinates,
                        point.coordinates
                    ])
                }
                this.points.push(point)

            })
        }
    },

    data() {
        return {
            points: [],
            arrows: []
        }
    }
}

</script>