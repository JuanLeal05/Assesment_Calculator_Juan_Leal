export type Operation =
  | 'add'
  | 'subtract'
  | 'multiply'
  | 'divide'
  | 'power'
  | 'percent'
  | 'squareRoot'

export interface OperationConfig {
  id: Operation
  label: string
  symbol: string
  /** Labels for the inputs, in order. One label means a unary operation. */
  inputs: [string] | [string, string]
}

export const OPERATIONS: OperationConfig[] = [
  { id: 'add', label: 'Add', symbol: '+', inputs: ['First number', 'Second number'] },
  { id: 'subtract', label: 'Subtract', symbol: '−', inputs: ['First number', 'Second number'] },
  { id: 'multiply', label: 'Multiply', symbol: '×', inputs: ['First number', 'Second number'] },
  { id: 'divide', label: 'Divide', symbol: '÷', inputs: ['Dividend', 'Divisor'] },
  { id: 'power', label: 'Power', symbol: 'xʸ', inputs: ['Base', 'Exponent'] },
  { id: 'percent', label: 'Percent', symbol: '%', inputs: ['Number', 'Percentage'] },
  { id: 'squareRoot', label: 'Square root', symbol: '√', inputs: ['Number'] },
]

export interface CalculationRequest {
  a: number
  b?: number
}

export interface CalculationResponse {
  result: number
}
