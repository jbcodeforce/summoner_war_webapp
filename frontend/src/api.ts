const BASE = '/api'

export interface Faction {
  id: number
  name: string
  summoner_name: string
  owned: boolean
}

export interface Game {
  id: number
  faction_a_id: number
  faction_b_id: number
  winner: string
  played_at: string
  player_a_name: string | null
  player_b_name: string | null
}

export interface MatrixEntry {
  faction_a_id: number
  faction_a_name: string
  faction_b_id: number
  faction_b_name: string
  wins_a: number
  wins_b: number
  total_games: number
}

export async function getFactions(owned?: boolean): Promise<Faction[]> {
  const url = owned !== undefined ? `${BASE}/factions?owned=${owned}` : `${BASE}/factions`
  const r = await fetch(url)
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function getFaction(id: number): Promise<Faction> {
  const r = await fetch(`${BASE}/factions/${id}`)
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function createFaction(data: { name: string; summoner_name: string; owned?: boolean }): Promise<Faction> {
  const r = await fetch(`${BASE}/factions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...data, owned: data.owned ?? false }),
  })
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function updateFaction(
  id: number,
  data: { name?: string; summoner_name?: string; owned?: boolean }
): Promise<Faction> {
  const r = await fetch(`${BASE}/factions/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function deleteFaction(id: number): Promise<void> {
  const r = await fetch(`${BASE}/factions/${id}`, { method: 'DELETE' })
  if (!r.ok) throw new Error(await r.text())
}

export async function getGames(factionId?: number): Promise<Game[]> {
  const url = factionId !== undefined ? `${BASE}/games?faction_id=${factionId}` : `${BASE}/games`
  const r = await fetch(url)
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function getGame(id: number): Promise<Game> {
  const r = await fetch(`${BASE}/games/${id}`)
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function createGame(data: {
  faction_a_id: number
  faction_b_id: number
  winner: string
  played_at?: string
  player_a_name?: string | null
  player_b_name?: string | null
}): Promise<Game> {
  const r = await fetch(`${BASE}/games`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function updateGame(
  id: number,
  data: {
    faction_a_id?: number
    faction_b_id?: number
    winner?: string
    played_at?: string
    player_a_name?: string | null
    player_b_name?: string | null
  }
): Promise<Game> {
  const r = await fetch(`${BASE}/games/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export async function deleteGame(id: number): Promise<void> {
  const r = await fetch(`${BASE}/games/${id}`, { method: 'DELETE' })
  if (!r.ok) throw new Error(await r.text())
}

export async function getMatrix(ownedOnly = false): Promise<MatrixEntry[]> {
  const r = await fetch(`${BASE}/matrix?owned_only=${ownedOnly}`)
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}
