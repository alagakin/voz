<template>
    <div class="bg-white absolute top-1/2 border-gray-200 border-2 rounded-r-md pt-2 pb-2 pl-2 pr-2 cursor-pointer" @click="handleClick"
         style="right: -45px;">
        <font-awesome-icon v-if="isOpen" :icon="['fas', 'caret-left']" style="color: #656b76;" />
        <font-awesome-icon v-else :icon="['fas', 'caret-right']" style="color: #656b76;" />

    </div>
</template>

<script>

export default {
    name: "CloseButton",
    props: {
        isOpen: {
            type: Boolean
        }
    },
    methods: {
        handleClick() {
            this.$emit('toggle')
        }
    }
}
</script>
