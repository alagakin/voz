<template>
    <div class="bg-white p-2 rounded-lg mb-2 text-sm flex justify-between pr-4 pl-4 cursor-pointer border-b-2"
         @click="select">
        <div class="flex flex-col w-full pl-2" :class="{'border-blue-500': selected, 'border-l-4': selected, 'text-gray-400': route['not_available']}">
            <div class="">
                <span class="mr-4" v-text="firstStationName"></span>
                <font-awesome-icon :icon="['fas', 'arrow-right']" class="mr-4"/>
                <span v-text="lastStationName"></span>
            </div>
            <div class="flex justify-between">
                <div>
                    <div>
                        {{fromDepartureTime}} - {{toArrivalTime}}
                    </div>
                    <font-awesome-icon :icon="['far', 'clock']" class="mr-2"/>
                    <span v-text="totalTime"></span>
                </div>
                <div v-show="!route['not_available']">
                    <span @click="showMore(route)" class="text-blue-500 hover:underline">more</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import formatName from "../utils/Text";
import {format} from "date-fns";

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
            selected: false
        }
    },
    methods: {
        showMore(route) {
            this.$emit("showMore", route)
        },
        select() {
            this.$emit("unselectAll")
            this.$emit("selectRoute", this.route)
            this.selected = true
        },
        unselect() {
            this.selected = false
        }
    },
    computed: {
        start() {
            return this.route.from["departure"]
        },
        end() {
            return this.route.to["arrival"]
        },
        totalTime() {
            const timeDifference = this.end - this.start;
            const hours = Math.floor(timeDifference / (1000 * 60 * 60));
            const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
            if (hours === 0 && minutes === 0) {
                return '0m';
            }
            const formattedHours = hours > 0 ? `${hours.toString().padStart(2, '0')}h` : '';
            const formattedMinutes = minutes > 0 ? `${minutes.toString().padStart(2, '0')}m` : '';

            return `${formattedHours} ${formattedMinutes}`.trim();
        },
        firstStationName() {
            return formatName(this.route.from["name"])
        },
        lastStationName() {
            return formatName(this.route.to["name"])
        },
        fromDepartureTime() {
            return format(this.route.from.departure, 'HH:mm')
        },
        toArrivalTime() {
            return format(this.route.to.arrival, 'HH:mm')
        }
    },
    emits: ["unselectAll", "selectRoute", "showMore"]
}

</script>