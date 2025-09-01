// services/adminUsers.ts
import api from "@/utils/axios";
import type { ViewAdmin } from "@/types/viewAdmin";

export async function fetchAdminUsers(): Promise<ViewAdmin[]> {
  const response = await api.get<ViewAdmin[]>("/admin-users/");
  return response.data;
}

export async function createAdminUser(
  data: Omit<ViewAdmin, "id" | "application_status" | "exam_status" | "exam_score"> & { password: string }
): Promise<ViewAdmin> {
  const response = await api.post<ViewAdmin>("/admin-users/", data);
  return response.data;
}
