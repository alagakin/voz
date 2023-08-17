<template>
    <div>
        <div class="bg-white p-2 rounded-lg mb-2 text-xl flex justify-between pr-4 pl-4 cursor-pointer"
             @click="collapse()">
            <div class="flex">
                <div>
                    <span class="mr-4" v-text="firstStation"></span>
                    <font-awesome-icon :icon="['fas', 'arrow-right']" class="mr-4"/>
                    <span v-text="lastStation"></span>
                </div>
                <span class="mr-2 ml-2">|</span>
                <div>
                    <font-awesome-icon :icon="['far', 'clock']" class="mr-2"/>
                    <span v-text="totalTime"></span>
                </div>
            </div>
            <div>
                <span><font-awesome-icon :icon="['fas', 'chevron-up']" :class="{'rotate-180': collapsed}"/></span>
            </div>
        </div>
        <div class="bg-white p-2 rounded-lg mb-2 text-xl block-container" :class="{'hidden': collapsed}">
            <div class="mb-2 pl-4">
                <p>Departure: {{ format(this.start, 'd.MM.Y HH:mm') }}</p>
                <p>Arrival: {{ format(this.end, 'd.MM.Y HH:mm') }}</p>
            </div>
            <hr>
            <div class="mt-2 pl-4 max-h-48 overflow-scroll overflow-x-hidden">

                <div class="flex items-center mb-2" v-for="(station, key) in route['stations']"
                     v-bind:key="station['id']">
                    <div class="mr-2" v-text="station['name']"></div>
                    <template v-if="station['departure']">
                        <span class="text-gray-600">|</span>
                        <span class="ml-2 mr-2 text-gray-600" v-text="format(station['departure'], 'HH:mm')"></span>
                        <font-awesome-icon :icon="['fas', 'arrow-right']" class="mr-4 text-gray-600"
                                           v-if="key < (route['stations'].length - 1)"/>
                    </template>
                </div>
            </div>
        </div>

    </div>
</template>
<script setup>
import {format} from "date-fns";
</script>
<script>

export default {
    components: {},
    props: {
        route: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            collapsed: true
        }
    },
    methods: {
        collapse() {
            this.collapsed = !this.collapsed
        }
    },
    computed: {
        start() {
            return this.route.stations[0]['arrival']
        },
        end() {
            return this.route.stations[this.route.stations.length - 1]['departure']
        },
        totalTime() {
            return format(this.end - this.start, "H 'h' m 'min'")
        },
        firstStation() {
            return this.route.stations[0]['name']
        },
        lastStation() {
            return this.route.stations[this.route.stations.length - 1]['name']
        }
    },
}

</script>