<template>
    <nav>
      <router-link to="/">Просмотр расписания</router-link>
      <router-link to="/editor">Редактировать расписание</router-link>
    </nav>
    <router-view />
</template>

<style>
nav {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
</style>