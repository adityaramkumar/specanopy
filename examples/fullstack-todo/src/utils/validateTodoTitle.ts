// generated_from: contracts/ui/components
// spec_hash: bc79e30afe2aa54205d718240aef2c47fd0990937de675688ac674d7bdae57c0
// generated_at: 2026-03-15T02:28:11.258243+00:00
// agent: implementation-agent
/**
 * Validates a todo title.
 * @param title - The title to validate
 * @returns true if valid (non-empty after trim, <= 200 chars), false otherwise
 */
export function validateTodoTitle(title: string): boolean {
  const trimmed = title.trim();
  return trimmed.length > 0 && trimmed.length <= 200;
}