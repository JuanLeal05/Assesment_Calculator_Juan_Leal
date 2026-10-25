import type { CalculationRequest, CalculationResponse, Operation } from '../types/calculator'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const CALCULATE_URL = `${API_URL}/api/v1/calculate`

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

interface ValidationIssue {
  loc: (string | number)[]
  msg: string
}

/**
 * The API returns `{ detail: string }` for domain errors (400) and
 * `{ detail: ValidationIssue[] }` for FastAPI validation errors (422).
 */
function readErrorDetail(body: unknown): string | null {
  if (typeof body !== 'object' || body === null || !('detail' in body)) {
    return null
  }
  const { detail } = body as { detail: unknown }
  if (typeof detail === 'string') {
    return detail
  }
  if (Array.isArray(detail)) {
    return (detail as ValidationIssue[])
      .map(({ loc, msg }) => `${String(loc.at(-1))}: ${msg}`)
      .join('. ')
  }
  return null
}

export async function calculate(
  operation: Operation,
  request: CalculationRequest,
  signal?: AbortSignal,
): Promise<number> {
  let response: Response
  try {
    response = await fetch(`${CALCULATE_URL}/${operation}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
      signal,
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw error
    }
    throw new ApiError('Could not reach the calculator service. Is the API running?', 0)
  }

  const body: unknown = await response.json().catch(() => null)

  if (!response.ok) {
    const message = readErrorDetail(body) ?? `Unexpected error (HTTP ${response.status}).`
    throw new ApiError(message, response.status)
  }

  return (body as CalculationResponse).result
}
