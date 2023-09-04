<template>
    <div class="relative">
        <LocationInput ref="from" @setLocation="setLocationFrom" :placeholder="'From'" :request="request.from"/>
    </div>
    <div class="mt-2 flex justify-center">
        <span class="cursor-pointer" @click="reverse">
            <font-awesome-icon :icon="['fas', 'rotate']" :spin-pulse="reverseSpin" style="color: #5e6064;" size="md"/>
        </span>
    </div>
    <div class="relative mt-3">
        <LocationInput ref="to" @setLocation="setLocationTo" :placeholder="'To'" :request="request.to"/>
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
        reverse() {
            let temp = this.$refs.from.getQuery()
            this.$refs.from.setQuery(this.$refs.to.getQuery())
            this.$refs.to.setQuery(temp)
            this.reverseSpin = true
            setTimeout(() => {
                this.reverseSpin = false
            }, 500)
            this.$emit('reverse')
        },
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
            to: {},
            reverseSpin: false
        };

    },
    emits: ["setRoutes", "setRequestParam", "setDate", "reverse"]
}
</script>