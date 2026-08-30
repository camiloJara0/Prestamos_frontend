import { defineStore } from 'pinia'

export const useSyncStore = defineStore('sync', {
  state: () => ({
    isOnline: true,
    lastSyncAt: null as string | null,
    pendingCount: 0,
    syncing: false
  }),

  getters: {
    syncStatus: (state): 'ok' | 'pending' | 'syncing' | 'offline' => {
      if (!state.isOnline) return 'offline'
      if (state.syncing) return 'syncing'
      if (state.pendingCount > 0) return 'pending'
      return 'ok'
    }
  },

  actions: {
    setOnline(online: boolean) {
      this.isOnline = online
    },
    setSyncing(syncing: boolean) {
      this.syncing = syncing
    },
    setPendingCount(count: number) {
      this.pendingCount = count
    },
    markSynced() {
      this.lastSyncAt = new Date().toISOString()
      this.pendingCount = 0
      this.syncing = false
    },
    incrementPending() {
      this.pendingCount++
    },
    decrementPending() {
      if (this.pendingCount > 0) this.pendingCount--
    }
  }
})
