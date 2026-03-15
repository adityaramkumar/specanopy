// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.286951+00:00
// agent: implementation-agent
export type TodoFilter = 'all' | 'active' | 'completed';

export interface TodoFilterProps {
  filter: TodoFilter;
  onChange: (filter: TodoFilter) => void;
}

export function TodoFilter({ filter, onChange }: TodoFilterProps): JSX.Element {
  const buttons = [
    { key: 'all', label: 'All' },
    { key: 'active', label: 'Active' },
    { key: 'completed', label: 'Completed' },
  ];

  return (
    <div>
      {buttons.map(({ key, label }) => (
        <button
          key={key}
          data-active={filter === key}
          onClick={() => onChange(key as TodoFilter)}
          style={{
            fontWeight: filter === key ? 'bold' : 'normal',
          }}
        >
          {label}
        </button>
      ))}
    </div>
  );
}