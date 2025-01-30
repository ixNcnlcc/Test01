<script setup>
import { useLocalStorage } from '@vueuse/core';
import { computed, ref, nextTick } from 'vue';
import { Icon } from '@iconify/vue';

const displayTime = ref(new Date());
setInterval(() => {
    displayTime.value = new Date();
}, 1000);
const displayTimeString = computed(() => {
    return displayTime.value.toLocaleString('th-TH', {
        timeStyle: 'medium'
    });
});
const displayDateString = computed(() => {
    return displayTime.value.toLocaleString('th-TH', {
        dateStyle: 'full'
    });
});

const features = ref([
    {
        title: 'จำนวนบัญฑิตทั้งหมด',
        description: '0'
    },
    {
        title: 'จำนวนบัญฑิตที่มารายงานตัวทั้งหมด',
        description: '0'
    },
    {
        title: 'จำนวนบัญฑิตในห้องรายงานตัว',
        description: '0'
    },
    {
        title: 'จำนวนบัญฑิตในห้องรับปริญญาบัตร',
        description: '0'
    }
]);

// ตัวแปรคอมเมนต์
const newComment = ref('');
const commentsContainer = ref(null);
const comments = useLocalStorage('box', [
    {
        comment: 'starts',
        time: new Date()
    }
]);
const addComment = () => {
    if (newComment.value.trim()) {
        comments.value.push({
            comment: newComment.value,
            time: new Date()
        });
        newComment.value = '';

        nextTick(() => {
            scrollToBottom();
        });
    }
};
const confirmClear = () => {
    const confirmed = window.confirm('แน่ใจไหมว่าจะลบทั้งหมด ?');
    if (confirmed) {
        comments.value = [];
        return {
            comments,
            clearComments
        };
    }
};

const scrollToBottom = () => {
    if (commentsContainer.value) {
        commentsContainer.value.scrollTo({
            top: commentsContainer.value.scrollHeight,
            behavior: 'smooth' // เพิ่ม effect การเลื่อนแบบ smooth
        });
    }
};
</script>

<template>
    <div class="flex flex-col">
        <!-- ส่วนแสดงวันที่และเวลา -->
        <div class="card flex flex-row md:flex-row items-center justify-between mb-[2rem] gap-2 divide-x-4 divide-indigo-600">
            <div class="text-1xl sm:text-2xl md:text-3xl xl:text-4xl flex-1 text-center">{{ displayDateString }}</div>
            <div class="flex text-2xl sm:text-4xl md:text-6xl gap-2 items-center flex-1 justify-center">
                <Icon icon="material-symbols:alarm-outline-rounded"></Icon>
                <span>{{ displayTimeString }}</span>
            </div>
        </div>
        <div class="grid grid-cols-12 md:flex-row gap-[2rem]">
            <!-- ส่วนแสดงจำนวน -->
            <div class="col-span-12 md:col-span-8">
                <div class="grid grid-cols-12 gap-[2rem] h-full">
                    <div
                        class="rounded-s-md hover:-translate-y-2 duration-150 hover:shadow-2xl card flex flex-col col-span-12 xl:col-span-6"
                        v-for="(feat, index) in features"
                        :key="feat"
                        :class="[
                            index % 4 === 0
                                ? 'hover:border-b-8 hover:border-blue-500 rounded-lg'
                                : index % 4 === 1
                                ? 'hover:border-b-8 hover:border-green-500 rounded-lg'
                                : index % 4 === 2
                                ? 'hover:border-b-8 hover:border-[#FFEB00] rounded-lg'
                                : 'hover:border-b-8 hover:border-orange-500 rounded-lg'
                        ]"
                    >
                        <h2 class="pb-2 border-b-2 border-indigo-600 text-xl xl:text-2xl text-center">
                            {{ feat.title }}
                        </h2>
                        <span class="text-4xl xl:text-6xl pt-4 flex flex-grow justify-around items-center">     {{ feat.description }} </span>
                    </div>
                </div>
            </div>
            <!-- ส่วนแสดงคอมเมนต์ -->
            <div class="col-span-12 md:col-span-4">
                <div class="card h-[calc(100vh-100px)] max-h-[calc(100vh-230px)] xl:max-h-[calc(100vh-300px)] overflow-auto" ref="commentsContainer">
                    <div class="text-2xl pb-2">Comments</div>
                    <div v-for="(comment, index) in comments" :key="index" class="mb-2 border-t-2 border-indigo-600 pt-2">
                        <p class="w-full text-center text-xs">
                            {{
                                new Date(comment.time).toLocaleString('th-TH', {
                                    dateStyle: 'short'
                                })
                            }}
                            {{
                                new Date(comment.time).toLocaleString('th-TH', {
                                    timeStyle: 'short'
                                })
                            }}
                        </p>
                        <p class="text-lg w-full px-2 flex-col break-words">
                            {{ comment.comment }}
                        </p>
                    </div>  
                    <div class="">
                        <div class="grid grid-cols-12 md:flex-row gap-2 pt-4">
                            <InputText type="text" v-model="newComment" placeholder="พิมพ์คอมเมนต์ของคุณ.... " class="flex flex-col col-span-12 xl:col-span-8 px-2 border text-1xl resize-none rounded-md" />
                            <Button label="Post" @click="addComment" class="flex flex-col col-span-12 xl:col-span-2 text-xl" Rounded />
                            <Button label="Clear" @click="confirmClear" class="flex flex-col col-span-12 xl:col-span-2 text-xl" severity="danger" Rounded />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
