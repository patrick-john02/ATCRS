import api from "@/utils/axios";
import type { ApplicantProfile } from "@/types/applicantProfile";

export async function fetchApplicantProfile(): Promise<ApplicantProfile[]> {
  const response = await api.get<ApplicantProfile[]>("/profile");
  return response.data;
}
