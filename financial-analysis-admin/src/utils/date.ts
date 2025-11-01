/**
 * 日期格式化工具
 */
import dayjs, { type Dayjs } from 'dayjs'

/**
 * 格式化日期
 * @param date 日期
 * @param format 格式字符串
 * @returns 格式化后的日期字符串
 */
export const formatDate = (date: string | Date | Dayjs, format = 'YYYY-MM-DD'): string => {
  return dayjs(date).format(format)
}

/**
 * 获取日期范围快捷选项
 */
export const getDateShortcuts = () => [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  },
  {
    text: '最近半年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 180)
      return [start, end]
    }
  },
  {
    text: '最近一年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 365)
      return [start, end]
    }
  }
]

/**
 * 日期转换为 YYYYMMDD 格式
 */
export const toYYYYMMDD = (date: string | Date | Dayjs): string => {
  return dayjs(date).format('YYYYMMDD')
}

/**
 * YYYYMMDD 格式转换为 YYYY-MM-DD
 */
export const fromYYYYMMDD = (dateStr: string): string => {
  if (!dateStr || dateStr.length !== 8) return dateStr
  return `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6, 8)}`
}
