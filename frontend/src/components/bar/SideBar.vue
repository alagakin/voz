<template>
    <div :class="{'open': isOpen}"
         class="sidebar fixed top-0 left-0 bg-white p-4 shadow-xl h-full w-1/5 border-gray-200 border-r-2"
         style="z-index: 10000000;">
        <div class="flex gap-4 relative w-full h-full">
            <CloseButton :isOpen="isOpen" @toggle="toggle"/>
        </div>
    </div>

</template>
<script>

import CloseButton from "@/components/bar/CloseButton.vue";

export default {
    name: "SideBar",
    components: {CloseButton},
    methods: {
        toggle(){
            this.isOpen = !this.isOpen
        }
    },
    data() {
        return {
            isOpen: true
        }
    }
}
</script>


<style>

.sidebar {
    width: 20%;
    transform: translateX(-100%);
    transition: transform 0.3s ease-out;
}

.sidebar.open {
    transform: translateX(0);
}

.content {
    flex: 1;
    background-color: #ffffff;
    padding: 20px;
}
</style>