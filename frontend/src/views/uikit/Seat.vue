<script setup>
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { Icon } from '@iconify/vue';

const toast = useToast();
const persons = ref();
const loading = ref(false);

// เพิ่ม 0 ให้เลขครบ 4 หลัก
function formatId(id) {
    return id.toString().padStart(4, '0');
}

async function fetchPersons() {
    loading.value = true; // เริ่มต้น loading
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/person/');
        persons.value = response.data.map((person) => ({
            ...person,
            formatted_id: formatId(person.id) // ใช้ฟังก์ชันจัดรูปแบบ ID
        }));
    } catch (error) {
        console.error('Error fetching persons:', error);
    } finally {
        loading.value = false; // หยุด loading ไม่ว่าจะสำเร็จหรือล้มเหลว
    }
}
onMounted(fetchPersons);
</script>

<template>
    <div>
        <div v-if="loading">กำลังโหลดข้อมูล...</div>
        <div class="card grid grid-cols-6 grid-rows-5 gap-5">
            <div class="min-h-[100px] rounded-lg bg-orange-500 shadow">01</div>
            <div class="min-h-[100px] rounded-lg bg-orange-500 shadow">02</div>
            <!-- <div class="" v-for="(persons, index) in persons" :key="index">( {{ persons.id }} )</div> -->
        </div>
    </div>
</template>

<style scoped>
.iconify {
    width: 18px;
    height: 18px;
}
</style>
