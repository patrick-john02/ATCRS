export interface ApplicantProfile {
  full_name: string;
  email: string;
  contact_number: string;
  address: string;
  birthdate: string; // ISO date string
  high_school: string;
  year_graduated: number;
  course_applied_name: string | null;
  profile_photo_url: string | null;
}
