// types/results.ts

export interface ApplicantInfo {
  id: number;
  name: string;
  email: string;
  contact_number: string;
  application_status: string;
  exam_status: string;
}

export interface ExamInfo {
  uuid: string;
  title: string;
  description: string;
  date: string;
  duration_minutes: number;
}

export interface CourseInfo {
  id: number;
  code: string;
  name: string;
  min_score: number | null;
}

export interface ExamResult {
  uuid: string;
  applicant: ApplicantInfo;
  exam: ExamInfo;
  score: number | null;
  recommendation_score: string;
  accuracy: string;
  total_questions: number;
  attempted_questions: number;
  correct_answers: number;
  recommended_course: CourseInfo | null;
  exam_attempt_number: number;
  status: string;
  started_at: string;
  completed_at: string;
  created_at: string;
}

export interface PassedApplicantResult {
  uuid: string;
  applicant_name: string;
  applicant_email: string;
  exam_title: string;
  exam_date: string;
  score: number | null;
  recommendation_score: string;
  accuracy: string;
  total_questions: number;
  attempted_questions: number;
  correct_answers: number;
  recommended_course_name: string;
  exam_attempt_number: number;
  completed_at: string;
  created_at: string;
}

export interface FailedApplicantResult {
  uuid: string;
  applicant_name: string;
  applicant_email: string;
  exam_title: string;
  exam_date: string;
  score: number | null;
  recommendation_score: string;
  accuracy: string;
  total_questions: number;
  attempted_questions: number;
  correct_answers: number;
  recommended_course_name: string | null;
  exam_attempt_number: number;
  completed_at: string;
  created_at: string;
}

export interface ResultsStatistics {
  total_exams: number;
  average_score: number;
  highest_score: number;
  lowest_score: number;
  passed_count: number;
  failed_count: number;
}

export interface CourseDistribution {
  recommended_course__code: string;
  recommended_course__name: string;
  count: number;
}

export interface ResultsStatisticsResponse {
  statistics: ResultsStatistics;
  course_distribution: CourseDistribution[];
}