import api from "@/utils/axios";
import type { ViewCourse } from "@/types/course";

export async function fetchCourse(): Promise<ViewCourse[]> {
  const response = await api.get<ViewCourse[]>("/superadmin-manage-courses/");
  return response.data;
}

export async function createCourse(
  data: Omit<ViewCourse, "id" | "application_status" | "exam_status" | "exam_score"> & { password: string }
): Promise<ViewCourse> {
  const response = await api.post<ViewCourse>("/superadmin-manage-courses/", data);
  return response.data;
}
