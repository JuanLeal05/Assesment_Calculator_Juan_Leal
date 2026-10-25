import { useState, type FormEvent } from 'react'
import { useCalculator } from '../../hooks/useCalculator'
import { OPERATIONS, type Operation } from '../../types/calculator'
import { ErrorBanner } from '../ErrorBanner/ErrorBanner'
import { OperationTabs } from '../OperationTabs/OperationTabs'
import './CalculatorCard.css'

export function CalculatorCard() {
  const [operation, setOperation] = useState<Operation>('add')
  const [values, setValues] = useState<string[]>(['', ''])
  const { result, error, isLoading, execute, setError, reset } = useCalculator()

  const config = OPERATIONS.find((op) => op.id === operation) ?? OPERATIONS[0]

  const handleSelect = (next: Operation) => {
    setOperation(next)
    reset()
  }

  const handleChange = (index: number, value: string) => {
    setValues((current) => current.map((v, i) => (i === index ? value : v)))
  }

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const numbers: number[] = []
    for (const [index, label] of config.inputs.entries()) {
      const raw = values[index].trim()
      const parsed = Number(raw)
      if (raw === '' || !Number.isFinite(parsed)) {
        setError(`Please enter a valid number for "${label}".`)
        return
      }
      numbers.push(parsed)
    }

    const [a, b] = numbers
    void execute(operation, b === undefined ? { a } : { a, b })
  }

  return (
    <div className="calculator">
      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      <form className="calculator__card" onSubmit={handleSubmit} noValidate>
        <OperationTabs operations={OPERATIONS} selected={operation} onSelect={handleSelect} />

        <h2 className="calculator__title">{config.label}</h2>

        <div className={`calculator__inputs calculator__inputs--${config.inputs.length}`}>
          {config.inputs.map((label, index) => (
            <label key={label} className="calculator__field">
              <span>{label}</span>
              <input
                type="text"
                inputMode="decimal"
                autoComplete="off"
                placeholder="0"
                value={values[index]}
                onChange={(event) => handleChange(index, event.target.value)}
              />
            </label>
          ))}
        </div>

        <button type="submit" className="calculator__submit" disabled={isLoading}>
          {isLoading ? 'Calculating…' : 'Calculate'}
        </button>

        <output className="calculator__result" aria-live="polite">
          {result !== null && (
            <>
              <span>Result</span>
              <strong>{result}</strong>
            </>
          )}
        </output>
      </form>
    </div>
  )
}
