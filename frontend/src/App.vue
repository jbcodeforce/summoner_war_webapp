<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="header-brand">
        <img src="/summoner-wars-cover.webp" alt="Summoner Wars" class="game-logo" width="48" height="67" />
        <span class="app-title">Summoner Wars Tracker</span>
      </div>
      <nav class="main-nav">
        <RouterLink to="/" class="nav-link">Games</RouterLink>
        <RouterLink to="/matrix" class="nav-link">Matrix</RouterLink>
        <RouterLink to="/factions" class="nav-link">Factions</RouterLink>
      </nav>
    </header>
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style>
#app {
  font-family: system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-background);
  color: var(--color-text);
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-background-mute);
  border-bottom: 2px solid var(--color-border);
  flex-shrink: 0;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.game-logo {
  display: block;
  height: 48px;
  width: auto;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.app-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-heading);
}

.main-nav {
  display: flex;
  gap: 0.25rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  color: var(--color-text);
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: background 0.15s, color 0.15s;
}

.nav-link:hover {
  background: var(--color-border);
}

.nav-link.router-link-active {
  background: var(--vt-c-indigo);
  color: var(--vt-c-white);
}

.app-main {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem;
  box-sizing: border-box;
}
</style>
