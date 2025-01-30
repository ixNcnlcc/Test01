<script setup>
import { ref } from 'vue';

const display = ref(false);

function open() {
    display.value = true;
}

function close() {
    display.value = false;
}

const box = ref([
    {
        title: 'ดาว์นโหลดรายชื่อ CSV'
    },
    {
        title: 'ดาว์นโหลดรายชื่อ PDF'
    },
    {
        title: 'เพิ่มรายชื่อบัณฑิต'
    },
    {
        title: 'รายชื่อทั้งหมด'
    },
    {
        title: 'ไม่มารายงานตัว'
    },
    {
        title: 'รายชื่อมารายงานตัว'
    }
]);
</script>

<template>
    <div class="flex flex-col md:flex-row">
        <div class="md:w-full">
            <div class="card">
                <div class="flex items-center gap-5 justify-between mb-4">
                    <div class="flex space-x-10">
                        <Dialog header="Dialog" v-model:visible="display" :breakpoints="{ '960px': '75vw' }" :style="{ width: '30vw' }" :modal="true">
                            <template #footer>
                                <Button label="Save" @click="close" />
                            </template>
                            <template #default></template>
                        </Dialog>
                        <ButtonGroup>
                            <Button v-for="tap in box" :label="tap.title" severity="secondary" style="width: auto" @click="open" size="large" raised />
                        </ButtonGroup>
                    </div>
                    <div class="flex">
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText placeholder="ค้นหาข้อมูลบัญฑิต"></InputText>
                        </IconField>
                    </div>
                </div>
                <DataTable :value="RFID_Student" :paginator="true" :rows="15" dataKey="id" :rowHover="true" v-model:filters="filters1" filterDisplay="menu" :loading="loading1" :filters="filters1" :globalFilterFields="[]" showGridlines>
                    <Column field="name" header="ลำดับที่" style="min-width: 12rem">
                        <template #body="{ data }">
                            {{ data.id }}
                        </template>
                    </Column>
                    <Column field="name" header="รหัสนิสิต" style="min-width: 12rem">
                        <template #body="{ data }">
                            {{ data.id.collegian }}
                        </template>
                    </Column>
                    <Column field="name" header="ชื่อ-นามสกุล" style="min-width: 12rem">
                        <template #body="{ data }">
                            {{ data.name.th }}
                        </template>
                    </Column>
                    <Column field="name" header="ชื่อปริญญา" style="min-width: 12rem">
                        <template #body="{ data }">
                            {{ data.degree }}
                        </template>
                    </Column>
                    <Column field="name" header="เลขที่นั่ง" style="min-width: 12rem">
                        <template #body="{ data }">
                            {{ data.seat }}
                        </template>
                    </Column>
                    <Column field="verified" header="Verified" dataType="boolean" bodyClass="text-center" style="min-width: 8rem">
                        <template #body="{ data }">
                            <i class="pi" :class="{ 'pi-check-circle text-green-500 ': data.verified, 'pi-times-circle text-red-500': !data.verified }"></i>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>
