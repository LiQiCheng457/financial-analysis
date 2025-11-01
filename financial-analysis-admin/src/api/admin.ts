import request from '@/utils/request'

export interface AdminUserItem {
  id: number
  username: string
  role: string
  email?: string
  nickname?: string
  created_at?: string
}

export const adminApi = {
  listUsers(params: { skip?: number; limit?: number; q?: string } = {}) {
    return request.get('/vadmin/users/', { params })
  },
  createUser(payload: { username: string; password: string; role?: string; email?: string; nickname?: string }) {
    return request.post('/vadmin/users/', payload)
  },
  updateUser(userId: number, payload: any) {
    return request.put(`/vadmin/users/${userId}`, payload)
  },
  resetPassword(userId: number, newPassword: string) {
    return request.patch(`/vadmin/users/${userId}/password`, { new_password: newPassword })
  }
  ,
  deleteUser(userId: number) {
    return request.delete(`/vadmin/users/${userId}`)
  }
  ,
  getUser(userId: number) {
    return request.get(`/vadmin/users/${userId}`)
  }
}

export default adminApi
