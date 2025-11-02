// types/scores.ts (add to existing file)

export interface RecentExamScore {
  uuid: string;
  exam: {
    uuid: string;
    title: string;
    description: string;
    date: string;
  };
  status: 'not_started' | 'in_progress' | 'completed';
  score: number | null;
  recommendation_score: number | null;
  recommended_course: {
    code: string;
    name: string;
  } | null;
  total_questions: number;
  attempted_questions: number;
  correct_answers: number;
  accuracy: number | null;
  exam_attempt_number: number;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}