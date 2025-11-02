// stores/examScoresStores.ts

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { examScoresService } from '@/services/examScores.service';
import type { RecentExamScore } from '@/types/scores';

export const useExamScoresStore = defineStore('examScores', () => {
  const recentScores = ref<RecentExamScore[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchRecentScores = async () => {
    loading.value = true;
    error.value = null;
    try {
      recentScores.value = await examScoresService.getRecentScores();
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch exam scores';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    recentScores,
    loading,
    error,
    fetchRecentScores,
  };
});