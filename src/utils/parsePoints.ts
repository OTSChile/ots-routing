export function parsePoint(pointStr: string) {
  const [x, y] = pointStr.split(',').map(Number);
  return { x, y };
}
