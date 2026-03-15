// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.285401+00:00
// agent: implementation-agent
import { useState } from 'react';
import { validateTodoTitle } from '../utils/validateTodoTitle';

export interface AddTodoFormProps {
  onAdd: (title: string) => void;
}

export function AddTodoForm({ onAdd }: AddTodoFormProps): JSX.Element {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateTodoTitle(input)) {
      onAdd(input.trim());
      setInput('');
    }
  };

  const isValid = validateTodoTitle(input);

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        maxLength={200}
        placeholder="Add a new todo"
      />
      <button type="submit" disabled={!isValid}>
        Add Todo
      </button>
    </form>
  );
}