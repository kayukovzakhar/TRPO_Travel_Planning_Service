// components/ui/input.tsx
import React from 'react'

export const Input = ({ placeholder, className }: { placeholder: string, className: string }) => (
  <input
    placeholder={placeholder}
    className={`p-3 rounded-md border ${className}`}
  />
)
