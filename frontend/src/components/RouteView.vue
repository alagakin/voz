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
        route: {
        }
    },
    watch: {
        route(route) {
            this.points = []
            if (!route) {
                return
            }
            let stations = []
            let from_id = route["from"]["id"]
            let to_id = route["to"]["id"]
            let from_is_set = false
            let to_is_set = false
            for (let index in route["stations"]) {
                let station = route["stations"][index]
                if (from_is_set && to_is_set) {
                    continue
                }
                if (station["id"] === from_id) {
                    stations.push(station)
                    from_is_set = true
                    continue
                }
                if (station["id"] === to_id) {
                    stations.push(station)
                    to_is_set = true
                    continue
                }
                if (from_is_set) {
                    stations.push(station)
                }

            }

            stations.forEach((station, index) => {
                let point = {
                    coordinates: station.coordinates,
                    name: station['name'],
                    arrival: station['arrival'],
                    departure: station['departure']
                }
                if (index === 0) {
                    point.start = true
                }
                if (index === stations.length - 1) {
                    point.finish = true
                }
                if (index > 0) {
                    point['time'] = point.arrival - this.points[this.points.length - 1]['departure']
                } else {
                    point['time'] = 0
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