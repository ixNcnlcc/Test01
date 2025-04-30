<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { Icon } from '@iconify/vue';
import Dialog from 'primevue/dialog';
import Paginator from 'primevue/paginator';

const persons = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const dialogVisible = ref(false);
const selectedPerson = ref({});

// สำหรับ pagination
const currentPage = ref(0);
const rowsPerPage = ref(180);

// ดึงข้อมูล
async function fetchPersons() {
    loading.value = true;
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/person/');
        persons.value = response.data.map((person) => ({
            ...person,
            formatted_id: person.id.toString().padStart(4, '0')
        }));
    } catch (error) {
        console.error('Error:', error);
    } finally {
        loading.value = false;
    }
}

// ฟิลเตอร์ข้อมูล
const filteredPersons = computed(() => {
    if (!searchQuery.value) return persons.value;
    const query = searchQuery.value.toLowerCase();
    return persons.value.filter(
        (person) =>
            person.id.toString().includes(query) ||
            person.formatted_id.includes(query) ||
            person.name?.toLowerCase().includes(query) ||
            person.nisit?.includes(query) ||
            person.degree?.toLowerCase().includes(query) ||
            person.seat?.toString().includes(query)
    );
});

// จัดหน้าข้อมูล
const paginatedPersons = computed(() => {
    const start = currentPage.value * rowsPerPage.value;
    return filteredPersons.value.slice(start, start + rowsPerPage.value);
});

// เปิด dialog
function showPersonDetail(person) {
    selectedPerson.value = person;
    dialogVisible.value = true;
}
// ฟังก์ชันเมื่อ Dialog ปิด
function onBeforeHide() {
    dialogVisible.value = false;
}

// ฟังก์ชันเมื่อ Dialog เปิด
function onDialogShow() {
    setTimeout(() => {
        // ให้การเปิด dialog เป็นไปอย่างราบรื่น
        document.querySelector('.p-dialog').classList.add('transition-opacity');
    }, 10);
}

onMounted(fetchPersons);
</script>

<template>
    <div>
        <!-- Search bar -->
        <div class="my-3 relative">
            <!-- ไอคอนค้นหาด้านซ้าย -->
            <Icon icon="material-symbols:search" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
            <!-- ช่องกรอกข้อมูล -->
            <input v-model="searchQuery" type="text" placeholder="ค้นหา (ชื่อ, ID, รหัสนิสิต...)" class="p-inputtext p-component pl-10 w-full" />
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center my-4">กำลังโหลดข้อมูล...</div>

        <!-- Grid -->
        <div v-else class="card flex flex-wrap gap-2">
            <div v-for="(person, index) in paginatedPersons" :key="index" class="w-16 h-16 flex flex-col items-center justify-center text-center">
                <Icon
                    icon="material-symbols:event-seat"
                    class="text-4xl cursor-pointer"
                    :class="{
                        'text-green-500': person.verified === 1,
                        'text-red-500': person.verified === 0,
                        'text-gray-400': person.verified !== 1 && person.verified !== 0
                    }"
                    @click="() => showPersonDetail(person)"
                />
                <div class="text-xs mt-1">{{ person.seat }}</div>
            </div>
        </div>

        <!-- Pagination -->
        <Paginator class="mt-6" :rows="rowsPerPage" :totalRecords="filteredPersons.length" :first="currentPage * rowsPerPage" @page="(e) => (currentPage = e.page)" />

        <!-- Dialog -->
        <Dialog v-model:visible="dialogVisible" header="รายละเอียดผู้เข้าร่วม" modal :closable="true" :style="{ width: '300px', maxWidth: '90vw' }" @before-hide="onBeforeHide" @show="onDialogShow">
            <div>
                <p><strong>ชื่อ:</strong> {{ selectedPerson.name }}</p>
                <p><strong>รหัสนิสิต:</strong> {{ selectedPerson.nisit }}</p>
                <p><strong>คณะ:</strong> {{ selectedPerson.degree }}</p>
                <p><strong>ที่นั่ง:</strong> {{ selectedPerson.seat }}</p>
            </div>
        </Dialog>
    </div>
</template>

<style scoped>
/* เพิ่ม transition effect สำหรับ Dialog */
.p-dialog {
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.p-dialog-enter-active,
.p-dialog-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.p-dialog-enter,
.p-dialog-leave-to {
    opacity: 0;
    transform: translateY(-50px);
}

/* ปรับแต่งขนาดและตำแหน่งของ Dialog */
.p-dialog .p-dialog-content {
    padding: 20px;
}

.p-dialog-header {
    background-color: #4caf50;
    color: white;
    text-align: center;
}

/* กำหนดให้กรอบ Dialog มีมุมโค้งและเงา */
.p-dialog {
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* ปรับแต่งปุ่มปิด (x) */
.p-dialog .p-dialog-header-close {
    color: white;
    font-size: 18px;
}
</style>

