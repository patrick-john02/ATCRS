export interface UpcomingExam {
  uuid: string
  title: string
  description: string
  date: string
  start_time: string
  end_time: string
  duration_minutes: number
  access_code: string
  max_attempts: number
}
