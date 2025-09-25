import { defineStore } from 'pinia';
import type { ApplicantProfile } from '@/types/applicantProfile';
import { fetchApplicantProfile } from '@/services/applicantServices';

interface ApplicantProfileState {
  profile: ApplicantProfile | null;
  loading: boolean;
  error: string | null;
}

export const useApplicantProfileStore = defineStore('applicantProfile', {
  state: (): ApplicantProfileState => ({
    profile: null,
    loading: false,
    error: null,
  }),
  actions: {
    async fetchProfile() {
      this.loading = true;
      this.error = null;
      try {
        const profiles = await fetchApplicantProfile(); 
        this.profile = profiles[0] || null;
      } catch (err: any) {
        this.error = err.message || 'Failed to load profile';
      } finally {
        this.loading = false;
      }
    },
  },
});
