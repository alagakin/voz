<template>
    <div class="relative">
        <LocationInput @setLocation="setLocationFrom"/>
    </div>
    <div class="mt-2 flex justify-center">
        <span class="cursor-pointer" @click="() => $emit('reverse')">
            <font-awesome-icon :icon="['fas', 'rotate']" style="color: #5e6064;" size="xl"/>
        </span>
    </div>
    <div class="relative mt-3">
        <LocationInput @setLocation="setLocationTo"/>
    </div>

    <div class="relative mt-3">
        <CalendarView @selectDate="setDate"/>
    </div>
</template>
<script>
import formatDateToYMD from "@/utils/Dates";
import CalendarView from "@/components/CalendarView.vue";
import LocationInput from "@/components/bar/LocationInput.vue";

export default {
    name: "SearchInputs",
    components: {LocationInput, CalendarView},
    methods: {
        setLocationFrom(type, id) {
            let from = {
                id: id,
                type: type,
                direction: 'from'
            }
            this.from = from
            this.$emit('setRequestParam', from)
        },
        setLocationTo(type, id) {
            let to = {
                id: id,
                type: type,
                direction: 'to'
            }
            this.to = to
            this.$emit('setRequestParam', to)
        },
        setDate(date) {
            if (date) {
                this.date = formatDateToYMD(date)
            } else {
                this.date = null
            }
            this.$emit('setDate', this.date)
        },
    },
    props: {
        request: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            date: null,
            from: {},
            to: {}
        };

    },
    emits: ["setRoutes", "setRequestParam", "setDate", "reverse"]
}
</script>