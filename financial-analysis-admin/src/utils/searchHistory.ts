/**
 * 搜索历史管理工具
 * 用于存储和管理股票搜索历史
 */

interface SearchHistoryItem {
  code: string
  name: string
  market?: string
  timestamp: number
}

const STORAGE_KEY = 'stock_search_history'
const MAX_HISTORY_SIZE = 50 // 最多保存50条历史记录

class SearchHistoryManager {
  /**
   * 添加一条搜索记录
   */
  add(item: Omit<SearchHistoryItem, 'timestamp'> & { timestamp?: number }): void {
    const history = this.getAll()
    
    // 移除重复项（相同股票代码）
    const filtered = history.filter(h => h.code !== item.code)
    
    // 添加新记录到开头
    const newHistory = [
      {
        ...item,
        timestamp: item.timestamp || Date.now()
      },
      ...filtered
    ]
    
    // 限制数量
    const trimmed = newHistory.slice(0, MAX_HISTORY_SIZE)
    
    // 保存到本地存储
    this.save(trimmed)
  }

  /**
   * 获取所有搜索历史
   */
  getAll(): SearchHistoryItem[] {
    try {
      const data = localStorage.getItem(STORAGE_KEY)
      if (!data) return []
      
      const history = JSON.parse(data) as SearchHistoryItem[]
      
      // 按时间戳降序排序
      return history.sort((a, b) => b.timestamp - a.timestamp)
    } catch (e) {
      console.error('读取搜索历史失败:', e)
      return []
    }
  }

  /**
   * 获取最近N条搜索历史
   */
  getRecent(limit: number = 10): SearchHistoryItem[] {
    return this.getAll().slice(0, limit)
  }

  /**
   * 清空搜索历史
   */
  clear(): void {
    try {
      localStorage.removeItem(STORAGE_KEY)
    } catch (e) {
      console.error('清空搜索历史失败:', e)
    }
  }

  /**
   * 删除指定股票的搜索记录
   */
  remove(code: string): void {
    const history = this.getAll()
    const filtered = history.filter(item => item.code !== code)
    this.save(filtered)
  }

  /**
   * 保存搜索历史到本地存储
   */
  private save(history: SearchHistoryItem[]): void {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(history))
    } catch (e) {
      console.error('保存搜索历史失败:', e)
      
      // 如果存储满了，尝试清理旧数据后重试
      if (e instanceof DOMException && e.name === 'QuotaExceededError') {
        const reduced = history.slice(0, Math.floor(MAX_HISTORY_SIZE / 2))
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(reduced))
        } catch (e2) {
          console.error('清理后仍无法保存:', e2)
        }
      }
    }
  }

  /**
   * 检查某个股票是否在历史记录中
   */
  has(code: string): boolean {
    const history = this.getAll()
    return history.some(item => item.code === code)
  }

  /**
   * 获取搜索历史的统计信息
   */
  getStats(): {
    total: number
    oldest: Date | null
    newest: Date | null
  } {
    const history = this.getAll()
    
    if (history.length === 0) {
      return {
        total: 0,
        oldest: null,
        newest: null
      }
    }

    return {
      total: history.length,
      oldest: new Date(Math.min(...history.map(h => h.timestamp))),
      newest: new Date(Math.max(...history.map(h => h.timestamp)))
    }
  }
}

// 导出单例
export const searchHistoryManager = new SearchHistoryManager()

// 导出类型
export type { SearchHistoryItem }
