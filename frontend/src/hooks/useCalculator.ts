import { useCallback, useEffect, useRef, useState } from 'react'
import { ApiError, calculate } from '../api/calculatorApi'
import type { CalculationRequest, Operation } from '../types/calculator'

interface UseCalculatorResult {
  result: number | null
  error: string | null
  isLoading: boolean
  execute: (operation: Operation, request: CalculationRequest) => Promise<void>
  setError: (message: string | null) => void
  reset: () => void
}

export function useCalculator(): UseCalculatorResult {
  const [result, setResult] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const controllerRef = useRef<AbortController | null>(null)

  // Abort any in-flight request when the component unmounts.
  useEffect(() => () => controllerRef.current?.abort(), [])

  const execute = useCallback(async (operation: Operation, request: CalculationRequest) => {
    // A new calculation replaces the previous one, so cancel it if it's still pending.
    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      setResult(await calculate(operation, request, controller.signal))
    } catch (err) {
      if (controller.signal.aborted) return
      setError(err instanceof ApiError ? err.message : 'Something went wrong. Please try again.')
    } finally {
      if (controllerRef.current === controller) {
        setIsLoading(false)
      }
    }
  }, [])

  const reset = useCallback(() => {
    controllerRef.current?.abort()
    setResult(null)
    setError(null)
    setIsLoading(false)
  }, [])

  return { result, error, isLoading, execute, setError, reset }
}
