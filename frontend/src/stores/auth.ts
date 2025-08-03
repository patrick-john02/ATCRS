import { defineStore } from "pinia";
import api from '@/utils/axios';
// import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: '',
    refreshToken: '',
    user: null as Record<string, any> | null,
  }),

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await api.post('/token/', {
          username,
          password,
        });

        const { access, refresh } = response.data;
        this.accessToken = access;
        this.refreshToken = refresh;

        await this.fetchUser();
      } catch (error) {
        console.error(error);
        throw new Error('Login failed');
      }
    },

    async fetchUser() {
      const res = await api.get('/users/me/');
      this.user = res.data;
    },

    logout() {
      this.accessToken = '';
      this.refreshToken = '';
      this.user = null;
    }
  },

  persist: true
});
