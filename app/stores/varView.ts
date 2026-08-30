import { defineStore } from 'pinia'

export const useVarView = defineStore('varView', {
  state: () => ({
    showAside: false
  }),
  actions: {
    toggleAside() {
      this.showAside = !this.showAside
    }
  }
})
