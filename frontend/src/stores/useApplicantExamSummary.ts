import { defineStore } from 'pinia';
import type { ExamSummary } from "@/types/applicantExamSummary";
import { fetchExamSummary } from '@/services/applicantExamSummary';

interface ExamSummaryState {
  summaries: ExamSummary[];
  loading: boolean;
  error: string | null;
}

export const useExamSummaryStore = defineStore('examSummary', {
  state: (): ExamSummaryState => ({
    summaries: [],
    loading: false,
    error: null,
  }),
  actions: {
    async loadExamSummary() {
      this.loading = true;
      this.error = null;
      try {
        this.summaries = await fetchExamSummary();
      } catch (err: any) {
        this.error = err.message || 'Failed to fetch exam summary';
      } finally {
        this.loading = false;
      }
    },
  },
});
