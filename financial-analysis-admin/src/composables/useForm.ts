/**
 * 表单功能 Composable
 * 提供表单验证、提交、重置等通用逻辑
 */
import { ref, Ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

export interface FormOptions<T> {
  initialValues: T
  rules?: FormRules
  submitFn: (values: T) => Promise<any>
  onSuccess?: (result: any) => void
  onError?: (error: Error) => void
  successMessage?: string
  errorMessage?: string
}

export function useForm<T extends Record<string, any>>(options: FormOptions<T>) {
  const {
    initialValues,
    rules,
    submitFn,
    onSuccess,
    onError,
    successMessage = '操作成功',
    errorMessage = '操作失败，请重试'
  } = options

  const formRef = ref<FormInstance>()
  const formData: Ref<T> = ref({ ...initialValues } as T)
  const submitting = ref(false)
  const error: Ref<Error | null> = ref(null)

  const validate = async (): Promise<boolean> => {
    if (!formRef.value) return false
    
    try {
      await formRef.value.validate()
      return true
    } catch {
      return false
    }
  }

  const submit = async () => {
    const isValid = await validate()
    if (!isValid) return

    submitting.value = true
    error.value = null

    try {
      const result = await submitFn(formData.value)
      ElMessage.success(successMessage)
      onSuccess?.(result)
      return result
    } catch (err) {
      error.value = err as Error
      ElMessage.error(errorMessage)
      onError?.(err as Error)
      throw err
    } finally {
      submitting.value = false
    }
  }

  const reset = () => {
    formRef.value?.resetFields()
    formData.value = { ...initialValues } as T
    error.value = null
  }

  const clearValidate = () => {
    formRef.value?.clearValidate()
  }

  return {
    formRef,
    formData,
    submitting,
    error,
    rules,
    validate,
    submit,
    reset,
    clearValidate
  }
}
