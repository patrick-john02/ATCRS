import { defineStore } from "pinia";
import axios from "axios"; // <-- raw axios, not api

export const useAuthStore = defineStore("auth", {
  state: () => ({
    accessToken: "",
    refreshToken: "",
    user: null as Record<string, any> | null,
  }),

  actions: {
    async login(username: string, password: string) {
      const response = await axios.post("http://127.0.0.1:8000/api/token/", {
        username,
        password,
      });

      const { access, refresh } = response.data;
      this.accessToken = access;
      this.refreshToken = refresh;

      await this.fetchUser();
    },

    async fetchUser() {
      const api = (await import("@/utils/axios")).default; // lazy import api
      const res = await api.get("/users/me/");
      this.user = res.data;
    },

    logout() {
      this.accessToken = "";
      this.refreshToken = "";
      this.user = null;
    },
  },

  persist: true,
});
