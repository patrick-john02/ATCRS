import api from "@/utils/axios";
import type { ViewApplicants } from "@/types/viewApplicants";

export async function fetchApplicantUsers(): Promise<ViewApplicants[]> {
  const response = await api.get<ViewApplicants[]>("/applicants/");
  return response.data;
}

export async function createApplicantUser(
  data: Omit<ViewApplicants, "id" | "application_status" | "exam_status" | "exam_score"> & { password: string }
): Promise<ViewApplicants> {
  const response = await api.post<ViewApplicants>("/applicants/", data);
  return response.data;
}

export async function updateApplicantUser(
  id: number,
  data: Partial<Omit<ViewApplicants, "id" | "username">> & { password?: string }
): Promise<ViewApplicants> {
  const response = await api.patch<ViewApplicants>(`/applicants/${id}/`, data)
  return response.data
}