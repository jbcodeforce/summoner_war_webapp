<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as api from '@/api'

const factions = ref<api.Faction[]>([])
const loading = ref(true)
const error = ref('')
const showOwnedOnly = ref<boolean | null>(null)
const formOpen = ref(false)
const editingId = ref<number | null>(null)

const form = ref({
  name: '',
  summoner_name: '',
  owned: false,
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    factions.value = await api.getFactions(showOwnedOnly.value ?? undefined)
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
  form.value = { name: '', summoner_name: '', owned: false }
}

function openAddForm() {
  resetForm()
  formOpen.value = true
}

function setEdit(f: api.Faction) {
  editingId.value = f.id
  formOpen.value = true
  form.value = {
    name: f.name,
    summoner_name: f.summoner_name,
    owned: f.owned,
  }
}

async function toggleOwned(f: api.Faction) {
  error.value = ''
  try {
    await api.updateFaction(f.id, { owned: !f.owned })
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}

async function submit() {
  if (!form.value.name.trim() || !form.value.summoner_name.trim()) return
  error.value = ''
  try {
    if (editingId.value) {
      await api.updateFaction(editingId.value, form.value)
    } else {
      await api.createFaction(form.value)
    }
    resetForm()
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}

async function remove(id: number) {
  if (!confirm('Delete this faction? Games using it may be affected.')) return
  error.value = ''
  try {
    await api.deleteFaction(id)
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}
</script>

<template>
  <div class="factions-view">
    <div class="view-toolbar">
      <h1 class="view-title">Factions</h1>
      <div class="toolbar-actions">
        <label class="filter-label">
          Filter:
          <select v-model="showOwnedOnly" @change="load" class="filter-select">
            <option :value="null">All</option>
            <option :value="true">Owned only</option>
            <option :value="false">Not owned</option>
          </select>
        </label>
        <button type="button" class="btn-primary" @click="openAddForm">Add faction</button>
      </div>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <section v-if="formOpen" class="form-card">
      <h2 class="form-card-title">{{ editingId ? 'Edit faction' : 'Add faction' }}</h2>
      <form @submit.prevent="submit" class="form-inline">
        <input v-model="form.name" type="text" placeholder="Faction name" required class="form-input" />
        <input v-model="form.summoner_name" type="text" placeholder="Summoner name" required class="form-input" />
        <label class="checkbox-label">
          <input v-model="form.owned" type="checkbox" />
          Owned
        </label>
        <div class="form-actions">
          <button type="submit" class="btn-primary">{{ editingId ? 'Update' : 'Add' }}</button>
          <button type="button" @click="formOpen = false">Cancel</button>
        </div>
      </form>
    </section>

    <section class="table-card">
      <p v-if="loading" class="loading">Loading…</p>
      <div v-else-if="factions.length === 0" class="empty">No factions yet. Click “Add faction” to create one.</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Summoner</th>
            <th>Owned</th>
            <th class="col-actions"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="f in factions" :key="f.id">
            <td class="col-name">{{ f.name }}</td>
            <td>{{ f.summoner_name }}</td>
            <td>
              <button
                type="button"
                class="btn-owned"
                :class="{ owned: f.owned }"
                @click="toggleOwned(f)"
                :title="f.owned ? 'Mark as not owned' : 'Mark as owned'"
              >
                {{ f.owned ? '✓ Yes' : 'No' }}
              </button>
            </td>
            <td class="col-actions">
              <button type="button" class="btn-icon" title="Edit" @click="setEdit(f)" aria-label="Edit">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
                  <path d="m15 5 4 4"/>
                </svg>
              </button>
              <button type="button" class="btn-icon danger" title="Delete" @click="remove(f.id)" aria-label="Delete">
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
.factions-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.view-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.view-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: var(--color-heading);
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.filter-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.filter-select {
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-background);
  color: var(--color-text);
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

.form-input {
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-background);
  color: var(--color-text);
  min-width: 140px;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.9rem;
  cursor: pointer;
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

.col-name {
  font-weight: 600;
}

.col-actions {
  width: 1%;
  white-space: nowrap;
}

.btn-owned {
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-background);
  color: var(--color-text);
  cursor: pointer;
}

.btn-owned:hover {
  background: var(--color-border);
}

.btn-owned.owned {
  color: var(--vt-c-green, #27ae60);
  border-color: rgba(39, 174, 96, 0.5);
}

.btn-owned.owned:hover {
  background: rgba(39, 174, 96, 0.1);
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
