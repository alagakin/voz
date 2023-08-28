<template>
    <div class="bg-white p-2 rounded-lg mb-2 text-sm flex justify-between pr-4 pl-4 cursor-pointer border-b-2"
         @click="collapse()">
        <div class="flex flex-col w-full">
            <div class="">
                <span class="mr-4" v-text="firstStation"></span>
                <font-awesome-icon :icon="['fas', 'arrow-right']" class="mr-4"/>
                <span v-text="lastStation"></span>
            </div>
            <div class="flex justify-between">
                <div>
                    <font-awesome-icon :icon="['far', 'clock']" class="mr-2"/>
                    <span v-text="totalTime"></span>
                </div>
                <div>
                    <a href="" class="text-blue-500 hover:underline">more</a>
                </div>

            </div>
        </div>
    </div>
</template>
<script>
import formatName from "../utils/Text"
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
            return this.route.from['departure']
        },
        end() {
            return this.route.to['arrival']
        },
        totalTime() {
            const timeDifference = this.end - this.start;
            const hours = Math.floor(timeDifference / (1000 * 60 * 60));
            const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
            if (hours === 0 && minutes === 0) {
                return '0m'; // If both hours and minutes are zero
            }

            const formattedHours = hours > 0 ? `${hours.toString().padStart(2, '0')}h` : '';
            const formattedMinutes = minutes > 0 ? `${minutes.toString().padStart(2, '0')}m` : '';

            return `${formattedHours} ${formattedMinutes}`.trim();
        },
        firstStation() {
            return formatName(this.route.from['name'])
        },
        lastStation() {
            return formatName(this.route.to['name'])
        },

    },
}

</script>