<template>
  <div>
    <h1>Редактирование расписания</h1>
    <form @submit.prevent="saveSchedule">
      <div v-for="schedule in schedules" :key="schedule.id">
        <input v-model="schedule.subject" placeholder="Название предмета" />
        <input v-model="schedule.time" placeholder="Время (например, 10:00)" />
        <button type="button" @click="deleteLesson(schedule.id)">Удалить</button>
      </div>
      <button type="button" @click="addLesson">Добавить урок</button>
      <button type="submit">Сохранить</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      schedules: [],
      socket: null
    };
  },
  created(){
    this.socket = new WebSocket("ws://localhost:8765");
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.action == 'init' || data.action == 'update'){
        this.schedules = data.schedules;
      }
    }
  }

};
</script>