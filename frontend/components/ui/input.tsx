import React from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  /** Плейсхолдер поля */
  placeholder: string;
  /** Дополнительные классы Tailwind */
  className?: string;
}

export function Input({
  placeholder,
  className = "",
  ...props
}: InputProps) {
  const baseClasses =
    "w-full px-4 py-2 rounded-2xl border shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500";
  return (
    <input
      placeholder={placeholder}
      className={`${baseClasses} ${className}`}
      {...props}
    />
  );
}
