export interface Dashboard {
  applicants_count: number
  course_count: number
  exams_count: number
}

export interface CourseStatistics {
  name: string
  total_applicants: number
  recommended_count: number
}