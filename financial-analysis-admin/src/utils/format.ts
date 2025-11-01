/**
 * 数字格式化工具
 */

/**
 * 格式化数字，添加千分位分隔符
 * @param num 数字
 * @param decimals 小数位数
 * @returns 格式化后的字符串
 */
export const formatNumber = (num: number | string | null | undefined, decimals = 2): string => {
  if (num === null || num === undefined || num === '') return '-'

  const numValue = typeof num === 'string' ? parseFloat(num) : num
  if (isNaN(numValue)) return '-'

  return numValue.toLocaleString('zh-CN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  })
}

/**
 * 格式化百分比
 * @param num 数字 (0-100)
 * @param decimals 小数位数
 * @returns 格式化后的字符串
 */
export const formatPercent = (num: number | string | null | undefined, decimals = 2): string => {
  if (num === null || num === undefined || num === '') return '-'

  const numValue = typeof num === 'string' ? parseFloat(num) : num
  if (isNaN(numValue)) return '-'

  return `${numValue.toFixed(decimals)}%`
}

/**
 * 格式化金额（自动转换单位）
 * @param amount 金额
 * @param unit 单位
 * @returns 格式化后的字符串
 */
export const formatAmount = (
  amount: number | string | null | undefined,
  unit = '元'
): string => {
  if (amount === null || amount === undefined || amount === '') return '-'

  const numValue = typeof amount === 'string' ? parseFloat(amount) : amount
  if (isNaN(numValue)) return '-'

  const absValue = Math.abs(numValue)

  if (absValue >= 100000000) {
    return `${(numValue / 100000000).toFixed(2)}亿${unit}`
  } else if (absValue >= 10000) {
    return `${(numValue / 10000).toFixed(2)}万${unit}`
  } else {
    return `${numValue.toFixed(2)}${unit}`
  }
}

/**
 * 格式化涨跌幅（带颜色标识）
 * @param change 涨跌幅
 * @returns 格式化对象 { text, color, icon }
 */
export const formatChange = (change: number | string | null | undefined) => {
  if (change === null || change === undefined || change === '') {
    return { text: '-', color: '', icon: '' }
  }

  const numValue = typeof change === 'string' ? parseFloat(change) : change
  if (isNaN(numValue)) {
    return { text: '-', color: '', icon: '' }
  }

  const text = `${numValue > 0 ? '+' : ''}${numValue.toFixed(2)}%`
  const color = numValue > 0 ? '#f56c6c' : numValue < 0 ? '#67c23a' : '#909399'
  const icon = numValue > 0 ? '↑' : numValue < 0 ? '↓' : '-'

  return { text, color, icon }
}

/**
 * 格式化成交量
 * @param volume 成交量
 * @returns 格式化后的字符串
 */
export const formatVolume = (volume: number | string | null | undefined): string => {
  if (volume === null || volume === undefined || volume === '') return '-'

  const numValue = typeof volume === 'string' ? parseFloat(volume) : volume
  if (isNaN(numValue)) return '-'

  return formatAmount(numValue, '手')
}
