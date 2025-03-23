<template>
  <div>
    <h1 class="text-center mb-4">Расписание</h1>
    <div class="row justify-content-center" style="width: 100%;">
      <div v-for="(schedule, key) in schedules" :key="key" class="col-2 border m-3 p-3">
        <div @click="openModal(schedule)">
          <div class="text-lowercase fw-bold">Форма</div>
          <div>{{ schedule[1] }}</div>

          <div class="text-lowercase fw-bold">Время</div>
          <div>{{ key }}</div>

          <div class="text-lowercase fw-bold">Группа</div>
          <div>{{ schedule[2] }}</div>

          <div class="text-lowercase fw-bold">Состав группы</div>
          <div>{{ schedule[3] }}</div>

          <div class="text-lowercase fw-bold">Предмет</div>
          <div>{{ schedule[4] }}</div>

          <div class="text-lowercase fw-bold">Учитель</div>
          <div>{{ schedule[5] }}</div>

          <div class="text-lowercase fw-bold">Кабинет</div>
          <div>{{ schedule[6] }}</div>

          <div class="text-lowercase fw-bold">Ссылка на подключения</div>
          <div><a :href="schedule[7]">{{ trunsText(schedule[7]) }}</a></div>

          <div v-if="schedule[8]">
            <div class="text-lowercase fw-bold">Учитель на замену</div>
            <div>{{ schedule[8] }}</div>
          </div>

          <div v-if="schedule[9]">
            <div class="text-lowercase fw-bold">Ссылка на замену</div>
            <div>{{ trunsText(schedule[9]) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade " :class="{ show: isModalOpen }" tabindex="-1"
    :style="{ display: isModalOpen ? 'block' : 'none' }" @click.self="closeModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ selectedItem ? selectedItem[0] : '' }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" @click="closeModal"
            aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div>
            <div class="text-lowercase fw-bold">Форма</div>
            <div>{{ selectedItem ? selectedItem[1] : '' }}</div>

            <div class="text-lowercase fw-bold">Группа</div>
            <div>{{ selectedItem ? selectedItem[2] : '' }}</div>

            <div class="text-lowercase fw-bold">Состав группы</div>
            <div>{{ selectedItem ? selectedItem[3] : '' }}</div>

            <div class="text-lowercase fw-bold">Предмет</div>
            <div>{{ selectedItem ? selectedItem[4] : '' }}</div>

            <div class="text-lowercase fw-bold">Учитель</div>
            <div>{{ selectedItem ? selectedItem[5] : '' }}</div>

            <div class="text-lowercase fw-bold">Кабинет</div>
            <div>{{ selectedItem ? selectedItem[6] : '' }}</div>

            <div class="text-lowercase fw-bold">Ссылка на подключения</div>
            <div><a href="#">{{ selectedItem ? selectedItem[7] : '' }}</a></div>

            <div v-if="selectedItem">
              <div v-if="selectedItem[8]">
                <div class="text-lowercase fw-bold">Учитель на замену</div>
                <div>{{ selectedItem ? selectedItem[8] : '' }}</div>
              </div>

              <div v-if="selectedItem[9]">
                <div class="text-lowercase fw-bold">Ссылка на замену</div>
                <div>{{ selectedItem ? selectedItem[9] : '' }}</div>
              </div>
            </div>
          </div>

        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeModal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="isModalOpen" class="modal-backdrop fade show"></div>
</template>

<script>
export default {
  data() {
    return {
      schedules: [],
      socket: null,
      isModalOpen: false,
      selectedItem: null
    };
  },
  methods: {
    trunsText(text) {
      if (text.length > 20) {
        return text.substring(0, 20) + '...';

      }
    },
    openModal(schedule) {
      this.selectedItem = schedule;
      this.isModalOpen = true;
      console.log(this.selectedItem);
    },
    closeModal() {
      this.isModalOpen = false;
      this.selectedItem = null;
    }
  },
  created() {
    this.socket = new WebSocket("ws://localhost:8765");

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.action == 'init' || data.action == 'update') {
        console.log(data.schedules);
        this.schedules = data.schedules;
      }
    };
  }
};
</script>

<style scoped></style>