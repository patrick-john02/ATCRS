// services/examScores.service.ts

import api from '@/utils/axios';
import type { RecentExamScore } from '@/types/scores';

export const examScoresService = {
  getRecentScores: async (): Promise<RecentExamScore[]> => {
    const response = await api.get('/recent-exam-scores/');
    return response.data;
  },
};