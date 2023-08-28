<template>
    <div class="cursor-pointer pl-4" @click="() => $emit('back')">
        <font-awesome-icon :icon="['fas', 'arrow-left-long']" size="lg" style="color: #5a6372;"/>
    </div>
    <div class="h-full max-h-fit overflow-scroll overflow-x-hidden overflow-y-auto p-4">
        <div>
            <div v-for="(station, index) in route['stations']" v-bind:key="index">
                <div class="flex mb-1" :class="{'text-gray-500': !willVisit(station['id'])}">
                    <span v-text="format(station['arrival'], 'HH:mm')" class="mr-2"></span>
                    <span v-text="station['name']" class="mr-4"></span>
                    <span v-text="format(station['departure'], 'HH:mm')"></span>
                </div>
            </div>
        </div>
    </div>
</template>
<script>

export default {
    name: "DetailRoute",
    props: {
        route: Object
    },
    methods: {
        willVisit(stationId) {
            console.log(stationId)
            console.log(this.stationsToVisitIds)
            return this.stationsToVisitIds.includes(stationId)
        },
        calcStationsToVisitIds(route) {
            this.stationsToVisitIds = []
            console.log(route)
            if (!route) {
                return
            }

            let stationsIds = []
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
                    stationsIds.push(station['id'])
                    from_is_set = true
                    continue
                }
                if (station["id"] === to_id) {
                    stationsIds.push(station['id'])
                    to_is_set = true
                    continue
                }
                if (from_is_set) {
                    stationsIds.push(station['id'])
                }
            }
            this.stationsToVisitIds = stationsIds
        }
    },
    watch: {
        route(newVal) {
            this.calcStationsToVisitIds(newVal)
        }
    },
    mounted() {
        this.calcStationsToVisitIds(this.route)
    },
    data() {
        return {
            stationsToVisitIds: []
        }
    },
    emits: ["back"]
}
</script>
<script setup>
import {format} from "date-fns";
</script>