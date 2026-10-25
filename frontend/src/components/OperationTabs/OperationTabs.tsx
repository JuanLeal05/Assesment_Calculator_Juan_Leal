import type { Operation, OperationConfig } from '../../types/calculator'
import './OperationTabs.css'

interface OperationTabsProps {
  operations: OperationConfig[]
  selected: Operation
  onSelect: (operation: Operation) => void
}

export function OperationTabs({ operations, selected, onSelect }: OperationTabsProps) {
  return (
    <div className="operation-tabs" role="tablist" aria-label="Operation">
      {operations.map(({ id, label, symbol }) => (
        <button
          key={id}
          type="button"
          role="tab"
          aria-selected={id === selected}
          title={label}
          className="operation-tabs__tab"
          onClick={() => onSelect(id)}
        >
          {symbol}
        </button>
      ))}
    </div>
  )
}
