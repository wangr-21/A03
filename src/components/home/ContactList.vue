<script setup lang="ts">
import { ref, computed } from 'vue';

interface Contact {
  name: string;
  title: string;
  avatar: string;
}

// 联系人数据
const contacts: Contact[] = [
  { name: '王小明', title: '数学教师', avatar: '/src/assets/demo/contactlist_images/avatar1.jpg' },
  { name: '李晓华', title: '语文组长', avatar: '/src/assets/demo/contactlist_images/avatar2.jpg' },
  { name: '张三', title: '科学教师', avatar: '/src/assets/demo/contactlist_images/avatar3.jpg' },
];

const searchContact = ref<string>('');

// 过滤联系人
const filteredContacts = computed(() => {
  if (!searchContact.value) return contacts;

  return contacts.filter(
    (contact) =>
      contact.name.includes(searchContact.value) || contact.title.includes(searchContact.value),
  );
});
</script>

<template>
  <el-card class="contacts-card">
    <div class="card-header">
      <h3>联系人({{ contacts.length }})</h3>
      <el-input
        placeholder="搜索联系人"
        prefix-icon="Search"
        v-model="searchContact"
        size="small"
        class="contact-search"
      ></el-input>
    </div>

    <div class="contact-list">
      <div class="contact-item" v-for="(contact, index) in filteredContacts" :key="index">
        <div class="contact-avatar">
          <img :src="contact.avatar" :alt="contact.name" />
        </div>
        <div class="contact-info">
          <div class="contact-name">{{ contact.name }}</div>
          <div class="contact-title">{{ contact.title }}</div>
        </div>
      </div>
      <el-empty v-if="filteredContacts.length === 0" description="未找到匹配的联系人"></el-empty>
    </div>
  </el-card>
</template>

<style scoped>
.contacts-card {
  margin-bottom: 30px;
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 15px 20px 0;
}

.card-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.contact-search {
  width: 250px;
}

.contact-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 10px 20px;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  width: calc(33.33% - 10px);
  transition: all 0.3s ease;
}

.contact-item:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

@media (max-width: 1199px) {
  .contact-item {
    width: calc(50% - 10px);
  }
}

@media (max-width: 768px) {
  .contact-item {
    width: 100%;
  }

  .contact-search {
    width: 100%;
  }
}

.contact-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 15px;
}

.contact-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.contact-info {
  flex: 1;
}

.contact-name {
  font-weight: bold;
  color: #333;
}

.contact-title {
  font-size: 12px;
  color: #909399;
  margin-top: 3px;
}
</style>
