// services/results.service.ts

import api from '@/utils/axios';
import type { 
  ExamResult, 
  PassedApplicantResult, 
  FailedApplicantResult,
  ResultsStatisticsResponse 
} from '@/types/results';

export const resultsService = {
  getAllResults: async (params?: {
    exam?: string;
    course?: number;
    min_score?: number;
    max_score?: number;
    status?: 'passed' | 'failed';
    search?: string;
  }): Promise<ExamResult[]> => {
    const response = await api.get('/admin/results/', { params });
    return response.data;
  },

  getResultById: async (uuid: string): Promise<ExamResult> => {
    const response = await api.get(`/admin/results/${uuid}/`);
    return response.data;
  },

  getStatistics: async (): Promise<ResultsStatisticsResponse> => {
    const response = await api.get('/admin/results/statistics/');
    return response.data;
  },

  getPassedApplicants: async (params?: {
    min_score?: number;
    course?: number;
  }): Promise<PassedApplicantResult[]> => {
    const response = await api.get('/admin/results/passed/', { params });
    return response.data;
  },

  getFailedApplicants: async (params?: {
    max_score?: number;
    exam?: string;
  }): Promise<FailedApplicantResult[]> => {
    const response = await api.get('/admin/results/failed/', { params });
    return response.data;
  },
};