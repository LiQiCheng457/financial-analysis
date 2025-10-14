export interface MenuItem {
  key: string
  title: string
  path?: string
  icon?: string
  children?: MenuItem[]
}
