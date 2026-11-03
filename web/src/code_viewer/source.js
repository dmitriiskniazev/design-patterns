import { sourceHeader as sharedHeader } from "./header.js";

export function sourceHeader(options) {
  const label = options.common ? "Общий файл" : options.side === "before" ? "Без паттерна" : "С паттерном";
  return sharedHeader({ ...options, label });
}
