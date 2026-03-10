<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import * as api from '@/api'

const factions = ref<api.Faction[]>([])
const games = ref<api.Game[]>([])
const loading = ref(true)
const error = ref('')
const editingId = ref<number | null>(null)
const formOpen = ref(false)

const form = ref({
  faction_a_id: 0,
  faction_b_id: 0,
  winner: 'a',
  played_at: new Date().toISOString().slice(0, 16),
  player_a_name: '',
  player_b_name: '',
})

const factionNames = computed(() => {
  const m: Record<number, string> = {}
  factions.value.forEach((f) => { m[f.id] = f.name })
  return m
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const [f, g] = await Promise.all([api.getFactions(), api.getGames()])
    factions.value = f
    games.value = g
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

onMounted(load)

function resetForm() {
  editingId.value = null
  formOpen.value = false
  form.value = {
    faction_a_id: factions.value[0]?.id ?? 0,
    faction_b_id: factions.value[1]?.id ?? 0,
    winner: 'a',
    played_at: new Date().toISOString().slice(0, 16),
    player_a_name: '',
    player_b_name: '',
  }
}

function setEdit(game: api.Game) {
  editingId.value = game.id
  formOpen.value = true
  form.value = {
    faction_a_id: game.faction_a_id,
    faction_b_id: game.faction_b_id,
    winner: game.winner,
    played_at: game.played_at.slice(0, 16),
    player_a_name: game.player_a_name ?? '',
    player_b_name: game.player_b_name ?? '',
  }
}

function openAddForm() {
  resetForm()
  formOpen.value = true
}

async function submit() {
  if (!form.value.faction_a_id || !form.value.faction_b_id) {
    error.value = 'Select both factions'
    return
  }
  error.value = ''
  try {
    const payload = {
      faction_a_id: form.value.faction_a_id,
      faction_b_id: form.value.faction_b_id,
      winner: form.value.winner,
      played_at: new Date(form.value.played_at).toISOString(),
      player_a_name: form.value.player_a_name || null,
      player_b_name: form.value.player_b_name || null,
    }
    if (editingId.value) {
      await api.updateGame(editingId.value, payload)
    } else {
      await api.createGame(payload)
    }
    resetForm()
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}

async function remove(id: number) {
  if (!confirm('Delete this game?')) return
  error.value = ''
  try {
    await api.deleteGame(id)
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}

function formatDate(s: string) {
  return new Date(s).toLocaleDateString(undefined, { dateStyle: 'short' })
}
</script>

<template>
  <div class="games-view">
    <div class="view-toolbar">
      <h1 class="view-title">All games</h1>
      <button type="button" class="btn-primary" @click="openAddForm" v-if="factions.length >= 2">
        Add game
      </button>
      <p v-else class="hint">Add at least two factions to record games.</p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <!-- Compact add/edit form (collapsible) -->
    <section v-if="formOpen" class="form-card">
      <h2 class="form-card-title">{{ editingId ? 'Edit game' : 'Add game' }}</h2>
      <form @submit.prevent="submit" class="form-inline">
        <select v-model.number="form.faction_a_id" required title="Faction A">
          <option v-for="f in factions" :key="f.id" :value="f.id">{{ f.name }}</option>
        </select>
        <span class="vs">vs</span>
        <select v-model.number="form.faction_b_id" required title="Faction B">
          <option v-for="f in factions" :key="f.id" :value="f.id">{{ f.name }}</option>
        </select>
        <select v-model="form.winner" title="Winner">
          <option value="a">A wins</option>
          <option value="b">B wins</option>
        </select>
        <input v-model="form.played_at" type="datetime-local" required class="date-input" />
        <input v-model="form.player_a_name" type="text" placeholder="Player A" class="player-input" />
        <input v-model="form.player_b_name" type="text" placeholder="Player B" class="player-input" />
        <div class="form-actions">
          <button type="submit" class="btn-primary">{{ editingId ? 'Update' : 'Add' }}</button>
          <button type="button" @click="formOpen = false">Cancel</button>
        </div>
      </form>
    </section>

    <!-- Center: games table -->
    <section class="table-card">
      <p v-if="loading" class="loading">Loading…</p>
      <div v-else-if="games.length === 0" class="empty">No games yet. Click “Add game” to record one.</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Faction A</th>
            <th>Faction B</th>
            <th>Winner</th>
            <th>Players</th>
            <th class="col-actions"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="g in games" :key="g.id">
            <td>{{ formatDate(g.played_at) }}</td>
            <td>{{ factionNames[g.faction_a_id] ?? g.faction_a_id }}</td>
            <td>{{ factionNames[g.faction_b_id] ?? g.faction_b_id }}</td>
            <td>{{ g.winner === 'a' ? factionNames[g.faction_a_id] : factionNames[g.faction_b_id] }}</td>
            <td>{{ [g.player_a_name, g.player_b_name].filter(Boolean).join(' vs ') || '—' }}</td>
            <td class="col-actions">
              <button type="button" class="btn-icon" title="Edit" @click="setEdit(g)" aria-label="Edit">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
                  <path d="m15 5 4 4"/>
                </svg>
              </button>
              <button type="button" class="btn-icon danger" title="Delete" @click="remove(g.id)" aria-label="Delete">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 6h18"/>
                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                  <line x1="10" x2="10" y1="11" y2="17"/>
                  <line x1="14" x2="14" y1="11" y2="17"/>
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<style scoped>
.games-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.view-toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.view-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: var(--color-heading);
}

.btn-primary {
  padding: 0.5rem 1rem;
  background: var(--vt-c-indigo);
  color: var(--vt-c-white);
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary:hover {
  filter: brightness(1.1);
}

.hint {
  margin: 0;
  color: var(--color-text);
  opacity: 0.8;
  font-size: 0.9rem;
}

.error {
  margin: 0;
  padding: 0.5rem;
  background: rgba(200, 60, 60, 0.15);
  color: var(--vt-c-red, #c0392b);
  border-radius: 6px;
}

.form-card {
  padding: 1rem 1.25rem;
  background: var(--color-background-mute);
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.form-card-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.form-inline {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
}

.form-inline select,
.date-input,
.player-input {
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-background);
  color: var(--color-text);
}

.player-input {
  min-width: 90px;
}

.vs {
  font-size: 0.85rem;
  opacity: 0.8;
}

.form-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: 0.25rem;
}

.table-card {
  flex: 1;
  min-height: 200px;
  padding: 0;
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
}

.loading,
.empty {
  padding: 2rem;
  text-align: center;
  color: var(--color-text);
  opacity: 0.85;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.65rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.data-table th {
  font-weight: 600;
  background: var(--color-background-mute);
  color: var(--color-heading);
}

.data-table tbody tr:hover {
  background: var(--color-background-mute);
}

.col-actions {
  width: 1%;
  white-space: nowrap;
}

.col-actions .btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  margin-right: 0.25rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text);
  cursor: pointer;
}

.col-actions .btn-icon:hover {
  background: var(--color-border);
}

.col-actions .btn-icon.danger {
  color: var(--vt-c-red, #c0392b);
  border-color: rgba(200, 60, 60, 0.4);
}

.col-actions .btn-icon.danger:hover {
  background: rgba(200, 60, 60, 0.15);
}
</style>
