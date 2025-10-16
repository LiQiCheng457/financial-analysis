import request from '@/utils/request'

export interface UserInfo {
  id: number
  username: string
  avatar?: string
  nickname?: string
  phone?: string
  email?: string
  signature?: string
  created_at?: string
}

export interface UpdateProfileData {
  nickname?: string
  phone?: string
  email?: string
  signature?: string
}

export interface ChangePasswordData {
  old_password: string
  new_password: string
}

export interface AvatarUpdateData {
  avatar: string
}

/**
 * 获取当前用户信息
 */
export const getCurrentUser = () => {
  return request<UserInfo>({
    url: '/users/me',
    method: 'get'
  })
}

/**
 * 更新用户资料
 */
export const updateUserProfile = (data: UpdateProfileData) => {
  return request({
    url: '/users/me/profile',
    method: 'put',
    data
  })
}

/**
 * 更新用户头像
 */
export const updateUserAvatar = (data: AvatarUpdateData) => {
  return request({
    url: '/users/me/avatar',
    method: 'put',
    data
  })
}

/**
 * 修改密码
 */
export const changePassword = (data: ChangePasswordData) => {
  return request({
    url: '/users/me/password',
    method: 'post',
    data
  })
}
