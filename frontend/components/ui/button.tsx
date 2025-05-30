import React from "react";

/**
 * ButtonProps расширяет все стандартные HTML-атрибуты кнопки, включая type, onClick и т.д.
 */
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Варианты кнопки: "default" (синяя) или "destructive" (красная)
   */
  variant?: "default" | "destructive";
}

export function Button({
  children,
  variant = "default",
  className = "",
  ...props
}: ButtonProps) {
  const baseClasses =
    "px-6 py-2 rounded-2xl text-lg shadow-md font-medium transition-transform duration-300";
  const variantClasses =
    variant === "destructive"
      ? "bg-red-600 hover:bg-red-700 text-white"
      : "bg-blue-600 hover:bg-blue-700 text-white";

  return (
    <button
      {...props}
      className={`${baseClasses} ${variantClasses} ${className}`}
    >
      {children}
    </button>
  );
}
