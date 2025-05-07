<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const persons = ref([]);
const loading = ref(false);

// เรียกข้อมูลจาก API
async function fetchPersons() {
    loading.value = true;
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/person/');
        persons.value = response.data;
    } catch (error) {
        console.error('Error:', error);
    } finally {
        loading.value = false;
    }
}

// ฟังก์ชันช่วยจัดกลุ่มประเภทปริญญา
function getDegreeType(degreeName) {
    if (degreeName.includes('ดุษฎีบัณฑิต')) return 'ดุษฎีบัณฑิต';
    if (degreeName.includes('มหาบัณฑิต')) return 'มหาบัณฑิต';
    return 'บัณฑิต';
}

// สรุปข้อมูลตามชื่อปริญญา และเรียงลำดับประเภท
const summaryByDegree = computed(() => {
    const summary = {};

    persons.value.forEach((person) => {
        const degree = person.degree;
        if (!summary[degree]) {
            summary[degree] = { degree, total: 0, reported: 0, absent: 0 };
        }
        summary[degree].total += 1;
        if (person.verified === 1) {
            summary[degree].reported += 1;
        }
    });

    Object.values(summary).forEach((entry) => {
        entry.absent = entry.total - entry.reported;
        entry.percentage = entry.total > 0 ? ((entry.reported / entry.total) * 100).toFixed(2) : '0.00';
    });

    // ลำดับประเภทปริญญา
    const degreeOrder = ['บัณฑิต', 'ดุษฎีบัณฑิต', 'มหาบัณฑิต'];

    return Object.values(summary).sort((a, b) => {
        return degreeOrder.indexOf(getDegreeType(a.degree)) - degreeOrder.indexOf(getDegreeType(b.degree));
    });
});

// รวมสรุปทั้งหมด
const totalSummary = computed(() => {
    const total = { degree: 'รวมทั้งหมด', total: 0, reported: 0, absent: 0, percentage: '0.00' };

    summaryByDegree.value.forEach((item) => {
        total.total += item.total;
        total.reported += item.reported;
        total.absent += item.absent;
    });

    total.percentage = total.total > 0 ? ((total.reported / total.total) * 100).toFixed(2) : '0.00';

    return total;
});

onMounted(() => {
    fetchPersons();
});
</script>


<template>
    <div class="p-6 space-y-6">
        <h1 class="text-2xl font-bold">📋 รายงานสถานะบัณฑิตตามชื่อปริญญา</h1>

        <!-- Summary Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-blue-400 p-4 rounded-lg text-center shadow">
                <div class="text-gray-600 text-xl">บัณฑิตทั้งหมด</div>
                <div class="text-2xl font-bold">{{ totalSummary.total }}</div>
            </div>
            <div class="bg-green-400 p-4 rounded-lg text-center shadow">
                <div class="text-gray-600 text-xl">รายงานตัวแล้ว</div>
                <div class="text-2xl font-bold">{{ totalSummary.reported }}</div>
            </div>
            <div class="bg-red-400 p-4 rounded-lg text-center shadow">
                <div class="text-gray-600 text-xl">ขาด</div>
                <div class="text-2xl font-bold">{{ totalSummary.absent }}</div>
            </div>
            <div class="bg-yellow-400 p-4 rounded-lg text-center shadow">
                <div class="text-gray-600 text-xl">เปอร์เซ็นต์</div>
                <div class="text-2xl font-bold">{{ totalSummary.percentage }}%</div>
            </div>
        </div>

        <!-- Data Table -->
        <div class="overflow-x-auto">
            <table class="min-w-full text-sm border border-gray-300 rounded-lg shadow">
                <thead class="bg-blue-500 sticky top-0 z-10">
                    <tr>
                        <th class="px-4 py-2 border">ชื่อปริญญา</th>
                        <th class="px-4 py-2 border">จำนวนทั้งหมด</th>
                        <th class="px-4 py-2 border">รายงานตัวแล้ว</th>
                        <th class="px-4 py-2 border">ขาด</th>
                        <th class="px-4 py-2 border">เปอร์เซ็นต์</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in summaryByDegree" :key="item.degree" class="hover:bg-gray-500">
                        <td class="px-4 py-2 border text-xl">{{ item.degree }}</td>
                        <td class="px-4 py-2 border text-xl">{{ item.total }}</td>
                        <td class="px-4 py-2 border text-xl text-green-400">{{ item.reported }}</td>
                        <td class="px-4 py-2 border text-xl text-red-400">{{ item.absent }}</td>
                        <td class="px-4 py-2 border text-xl">
                            <div class="w-full bg-gray-200 rounded-full h-4">
                                <div class="bg-green-500 h-4 rounded-full" :style="{ width: item.percentage + '%' }"></div>
                            </div>
                            <div class="text-xl text-gray-300 mt-1">{{ item.percentage }}%</div>
                        </td>
                    </tr>
                    <!-- รวมทั้งหมด -->
                    <tr class="">
                        <td class="px-4 py-2 border text-xl">{{ totalSummary.degree }}</td>
                        <td class="px-4 py-2 border text-xl">{{ totalSummary.total }}</td>
                        <td class="px-4 py-2 border text-xl text-green-400">{{ totalSummary.reported }}</td>
                        <td class="px-4 py-2 border text-xl text-red-400">{{ totalSummary.absent }}</td>
                        <td class="px-4 py-2 border">
                            <div class="w-full bg-gray-300 rounded-full h-4">
                                <div class="bg-blue-600 h-4 rounded-full" :style="{ width: totalSummary.percentage + '%' }"></div>
                            </div>
                            <div class="text-xl text-gray-300 mt-1">{{ totalSummary.percentage }}%</div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
table {
    font-family: 'Arial', sans-serif;
}
th,
td {
    text-align: center;
}
</style>
