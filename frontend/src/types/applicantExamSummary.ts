export interface ExamSummary {
  exam_title: string;
  exam_status: string; 
  score: number | null;
  recommendation_score: number | null;
  recommended_course: string | null;
  eligible_courses: EligibleCourse[];
  total_questions: number;
  attempted_questions: number;
  correct_answers: number;
  exam_attempt_number: number;
  started_at: string | null; 
  completed_at: string | null; 
}

export interface EligibleCourse {
  code: string;
  name: string;
  min_score: number;
}
