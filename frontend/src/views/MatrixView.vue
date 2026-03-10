<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import * as api from '@/api'

const factions = ref<api.Faction[]>([])
const matrix = ref<api.MatrixEntry[]>([])
const loading = ref(true)
const error = ref('')
const ownedOnly = ref(false)

// Normalized key for a pair (smaller id first) -> total games (for tooltip)
const pairDone = computed(() => {
  const map = new Map<string, number>()
  for (const row of matrix.value) {
    const key = [row.faction_a_id, row.faction_b_id].sort((a, b) => a - b).join('-')
    map.set(key, (map.get(key) ?? 0) + row.total_games)
  }
  return map
})

function isMatchupDone(idA: number, idB: number): boolean {
  if (idA === idB) return false
  const key = [idA, idB].sort((a, b) => a - b).join('-')
  return (pairDone.value.get(key) ?? 0) > 0
}

function matchupCount(idA: number, idB: number): number {
  if (idA === idB) return 0
  const key = [idA, idB].sort((a, b) => a - b).join('-')
  return pairDone.value.get(key) ?? 0
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    const [factionList, matrixList] = await Promise.all([
      api.getFactions(ownedOnly.value ?? undefined),
      api.getMatrix(ownedOnly.value),
    ])
    factions.value = factionList
    matrix.value = matrixList
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

onMounted(load)

function refresh() {
  load()
}
</script>

<template>
  <div class="matrix-view">
    <div class="view-toolbar">
      <h1 class="view-title">Faction vs Faction matrix</h1>
      <label class="filter-label">
        <input type="checkbox" v-model="ownedOnly" @change="refresh" />
        Owned factions only
      </label>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading" class="loading">Loading…</p>
    <div v-else class="matrix-wrap">
      <table class="matrix-table">
        <thead>
          <tr>
            <th class="corner"></th>
            <th v-for="f in factions" :key="f.id" class="col-header">{{ f.name }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rowF in factions" :key="rowF.id">
            <th class="row-header">{{ rowF.name }}</th>
            <td
              v-for="colF in factions"
              :key="colF.id"
              class="cell"
              :class="{ done: isMatchupDone(rowF.id, colF.id), self: rowF.id === colF.id }"
              :title="rowF.id === colF.id ? '' : matchupCount(rowF.id, colF.id) ? `${matchupCount(rowF.id, colF.id)} game(s)` : 'Not played'"
            >
              <template v-if="rowF.id === colF.id">—</template>
              <template v-else-if="isMatchupDone(rowF.id, colF.id)">
                <span class="check" aria-hidden="true">✓</span>
              </template>
              <template v-else>—</template>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-if="!loading && factions.length === 0" class="empty">Add factions and record games to see the matrix.</p>
    <p v-else-if="!loading && factions.length > 0" class="legend">✓ = matchup played at least once</p>
  </div>
</template>

<style scoped>
.matrix-view {
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

.filter-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
}

.error {
  margin: 0;
  padding: 0.5rem;
  background: rgba(200, 60, 60, 0.15);
  color: var(--vt-c-red, #c0392b);
  border-radius: 6px;
}

.loading,
.empty {
  margin: 0;
  color: var(--color-text);
  opacity: 0.85;
}

.matrix-wrap {
  overflow-x: auto;
}

.matrix-table {
  border-collapse: collapse;
  font-size: 0.9rem;
}

.matrix-table th,
.matrix-table td {
  border: 1px solid var(--color-border);
  padding: 0.4rem 0.6rem;
  text-align: center;
  min-width: 2.5rem;
}

.corner {
  background: var(--color-background-mute);
  min-width: 6rem;
}

.row-header {
  text-align: left;
  font-weight: 600;
  background: var(--color-background-mute);
  white-space: nowrap;
  padding-right: 0.75rem;
}

.col-header {
  font-weight: 600;
  background: var(--color-background-mute);
  writing-mode: horizontal-tb;
  max-width: 5rem;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cell {
  background: var(--color-background);
}

.cell.self {
  background: var(--color-background-mute);
  color: var(--color-text);
  opacity: 0.6;
}

.cell.done {
  background: rgba(39, 174, 96, 0.15);
  color: var(--vt-c-green, #27ae60);
  font-weight: 600;
}

.cell.done .check {
  display: inline-block;
}

.legend {
  margin: 0;
  font-size: 0.85rem;
  opacity: 0.8;
}
</style>
