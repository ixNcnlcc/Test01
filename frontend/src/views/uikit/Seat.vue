<script setup>
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { Icon } from '@iconify/vue';

const toast = useToast();
const persons = ref([]);
const loading = ref(false);

// เพิ่ม 0 ให้เลขครบ 4 หลัก
function formatId(id) {
    return id.toString().padStart(4, '0');
}

async function fetchPersons() {
    loading.value = true; // เริ่มต้น loading
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/person/');
        console.log('data:', response.data);
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
        <div class="card grid grid-cols-12 grid-rows-20 gap-2">
            <div v-for="(person, index) in persons" :key="index" class="w-20 h-20 flex items-center justify-center bg-blue shadow-md rounded border border-gray-500">
                <Icon
                    icon="material-symbols:event-seat"
                    class="text-4xl"
                    :class="{
                        'text-green-500': person.verified === 1,
                        'text-red-500': person.verified === 0,
                        'text-gray-400': person.verified !== 1 && person.verified !== 0
                    }"
                />
                <div class="text-sm mt-1">{{ person.id }}</div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* สไตล์สำหรับที่นั่ง */
.grid div {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 14px;
    cursor: pointer;
    flex-direction: column; /* ให้รายการอยู่ในแนวตั้ง */
    text-align: center;
}
/* สไตล์สำหรับหมายเลขที่นั่ง */
.text-sm {
    font-size: 12px; /* ขนาดตัวอักษรที่เล็กลง */
    margin-top: 4px; /* ช่องว่างระหว่างไอคอนและหมายเลข */
}
/* สไตล์สำหรับที่นั่งที่มีข้อมูล */
.bg-gray-400 {
    background-color: #8195ad; /* สีเทา */
}

/* สไตล์สำหรับที่นั่งว่าง */
.bg-gray-300 {
    background-color: #e2e8f0; /* สีเทาที่อ่อนกว่า */
}

/* สไตล์สำหรับที่นั่งที่เลือก */
.bg-orange-500 {
    background-color: #f97316;
}

.hover\:bg-orange-600:hover {
    background-color: #ea580c;
}
</style>
