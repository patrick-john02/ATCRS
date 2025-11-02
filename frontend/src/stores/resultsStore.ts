// stores/resultsStore.ts

import { defineStore } from 'pinia';
import { ref } from 'vue';
import { resultsService } from '@/services/resultsService';
import type { 
  ExamResult, 
  PassedApplicantResult, 
  FailedApplicantResult,
  ResultsStatisticsResponse 
} from '@/types/results';

export const useResultsStore = defineStore('results', () => {
  const results = ref<ExamResult[]>([]);
  const passedApplicants = ref<PassedApplicantResult[]>([]);
  const failedApplicants = ref<FailedApplicantResult[]>([]);
  const statistics = ref<ResultsStatisticsResponse | null>(null);
  const selectedResult = ref<ExamResult | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchAllResults = async (params?: {
    exam?: string;
    course?: number;
    min_score?: number;
    max_score?: number;
    status?: 'passed' | 'failed';
    search?: string;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      results.value = await resultsService.getAllResults(params);
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch results';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchResultById = async (uuid: string) => {
    loading.value = true;
    error.value = null;
    try {
      selectedResult.value = await resultsService.getResultById(uuid);
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch result details';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchStatistics = async () => {
    loading.value = true;
    error.value = null;
    try {
      statistics.value = await resultsService.getStatistics();
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch statistics';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchPassedApplicants = async (params?: {
    min_score?: number;
    course?: number;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      passedApplicants.value = await resultsService.getPassedApplicants(params);
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch passed applicants';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const fetchFailedApplicants = async (params?: {
    max_score?: number;
    exam?: string;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      failedApplicants.value = await resultsService.getFailedApplicants(params);
    } catch (err: any) {
      error.value = err.response?.data?.message || 'Failed to fetch failed applicants';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    results,
    passedApplicants,
    failedApplicants,
    statistics,
    selectedResult,
    loading,
    error,
    fetchAllResults,
    fetchResultById,
    fetchStatistics,
    fetchPassedApplicants,
    fetchFailedApplicants,
  };
});